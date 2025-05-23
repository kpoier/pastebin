import random
from datetime import datetime, timedelta, UTC
from flask import Blueprint, render_template, request, redirect, url_for, abort
from . import db
from .model import Paste

main_bp = Blueprint('main', __name__, template_folder='templates')

@main_bp.route('/')
def index():
    paste_id = request.args.get('paste_id')
    password = request.args.get('password')
    return render_template('index.html', paste_id=paste_id, password=password)

@main_bp.route('/paste', methods=['POST'])
def create_paste():
    content = request.form.get('content')
    if not content:
        return "Content cannot be empty", 400

    paste_id = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=4))
    while db.session.query(Paste).filter_by(paste_id=paste_id).first():
        paste_id = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=4))
    
    if request.headers.get('X-Forwarded-For'):
        uploader_ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
    else:
        uploader_ip = request.headers.get('X-Real-IP', request.remote_addr)
    
    created_at = datetime.now(UTC)
    d = int(request.form.get('days', 0))
    h = int(request.form.get('hours', 0))
    m = int(request.form.get('minutes', 10))
    s = int(request.form.get('seconds', 0))
    if timedelta(days = d, hours = h, minutes = m, seconds = s) >= timedelta(days = 365):
        h = m = s = 0
        d = 365
    expired_at = (created_at + timedelta(days=d, hours=h, minutes=m, seconds=s))
    password = request.form.get('password', None)

    new_paste = Paste(
        paste_id=paste_id,
        uploader_ip=uploader_ip,
        created_at=created_at,
        expired_at=expired_at,
        password=password,
        content=content
    )
    db.session.add(new_paste)
    db.session.commit()

    return redirect(url_for('main.index', paste_id=paste_id, password=password))


@main_bp.route('/<paste_id>', methods=['GET', 'POST'])
def paste(paste_id):
    paste = db.session.query(Paste).filter_by(paste_id=paste_id).first()
    if not paste:
        abort(404)

    if paste.is_expired():
        now = datetime.now(UTC)
        expired_pastes = Paste.query.filter(Paste.expired_at < now).all()
        for expired in expired_pastes:
            db.session.delete(expired)
        db.session.commit()
        print(f"Deleted {len(expired_pastes)} expired pastes.")
        return "Expired"

    if paste.password:
        if request.method == 'POST':
            password = request.form.get('password')
            if password == paste.password:
                return render_template('paste.html', content=paste.content)
            else:
                return render_template('paste.html', paste_id=paste_id, error="Wrong password")
        return render_template('paste.html', paste_id=paste_id)

    return render_template('paste.html', content=paste.content)


@main_bp.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='img/favicon.ico'), code=302)