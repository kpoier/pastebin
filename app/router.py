import os
import random
from datetime import datetime, timedelta, UTC
from flask import Blueprint, render_template, request, redirect, url_for, abort, current_app, send_file, Response
from werkzeug.utils import secure_filename
from sqlalchemy import or_, and_
from . import db
from .model import Paste

main_bp = Blueprint('main', __name__, template_folder='templates')

@main_bp.app_errorhandler(404)
def page_not_found(e):
    # Render the paste template with no paste_id to trigger the error style
    return render_template('paste.html'), 404

@main_bp.route('/')
def index():
    paste_id = request.args.get('paste_id')
    password = request.args.get('password')
    return render_template('index.html', paste_id=paste_id, password=password)

@main_bp.route('/time')
def time():
    return render_template('time_picker.html', default_hour=8, default_minute=30)

@main_bp.route('/paste', methods=['POST'])
def create_paste():
    file = request.files.get('file')
    content = request.form.get('content')
    
    if not file and not content:
        return "Content or File cannot be empty", 400

    paste_id = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=4))
    while db.session.query(Paste).filter_by(paste_id=paste_id).first():
        paste_id = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=4))
    
    if request.headers.get('X-Forwarded-For'):
        uploader_ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
    else:
        uploader_ip = request.headers.get('X-Real-IP', request.remote_addr)
    
    created_at = datetime.now(UTC)
    d = int(request.form.get('days', 1))
    h = int(request.form.get('hours', 0))
    m = int(request.form.get('minutes', 0))
    s = int(request.form.get('seconds', 0))
    if timedelta(days = d, hours = h, minutes = m, seconds = s) >= timedelta(days = 14):
        h = m = s = 0
        d = 14
    expired_at = (created_at + timedelta(days=d, hours=h, minutes=m, seconds=s))
    password = request.form.get('password', None)

    filename = None
    mimetype = None

    if file and file.filename:
        filename = secure_filename(file.filename)
        mimetype = file.mimetype
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], paste_id))
        content = None
        
    new_paste = Paste(
        paste_id=paste_id,
        uploader_ip=uploader_ip,
        created_at=created_at,
        expired_at=expired_at,
        password=password,
        content=content,
        filename=filename,
        mimetype=mimetype
    )
    db.session.add(new_paste)
    db.session.commit()

    return redirect(url_for('main.index', paste_id=paste_id, password=password))

def cleanup_expired():
    now = datetime.now(UTC)
    week_ago = now - timedelta(days=7)
    to_delete = Paste.query.filter(
        or_(
            Paste.expired_at < week_ago,
            and_(Paste.deleted_at != None, Paste.deleted_at < week_ago)
        )
    ).all()
    
    for expired in to_delete:
        if expired.filename:
            path = os.path.join(current_app.config['UPLOAD_FOLDER'], expired.paste_id)
            if os.path.exists(path):
                os.remove(path)
        db.session.delete(expired)
    db.session.commit()

@main_bp.route('/<paste_id>', methods=['GET', 'POST'])
def paste(paste_id):
    paste = db.session.query(Paste).filter_by(paste_id=paste_id).first()
    if not paste:
        cleanup_expired()
        abort(404)

    if paste.is_expired() or paste.is_deleted():
        cleanup_expired()
        abort(404)

    if paste.password:
        password = request.form.get('password') if request.method == 'POST' else request.args.get('password')
        if password:
            if password == paste.password:
                if paste.filename:
                    path = os.path.join(current_app.config['UPLOAD_FOLDER'], paste.paste_id)
                    return send_file(path, download_name=paste.filename, mimetype=paste.mimetype)
                else:
                    return Response(paste.content, mimetype='text/plain', content_type='text/plain; charset=utf-8')
            else:
                return render_template('paste.html', paste_id=paste_id, error="WRONG ACCESS KEY")
        
        return render_template('paste.html', paste_id=paste_id)

    if paste.filename:
        path = os.path.join(current_app.config['UPLOAD_FOLDER'], paste.paste_id)
        return send_file(path, download_name=paste.filename, mimetype=paste.mimetype)
    else:
        return Response(paste.content, mimetype='text/plain', content_type='text/plain; charset=utf-8')

@main_bp.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='img/favicon.ico'), code=302)