from flask import Blueprint, render_template, request, session, redirect, url_for, current_app, abort
from datetime import datetime, UTC
import os
from . import db
from .model import Paste

admin_bp = Blueprint('admin', __name__)

def is_authenticated():
    return session.get('is_admin') == True

@admin_bp.route('/', methods=['GET'])
def index():
    if is_authenticated():
        return redirect(url_for('admin.dashboard'))
    return redirect(url_for('admin.login'))

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if is_authenticated():
        return redirect(url_for('admin.dashboard'))
        
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == current_app.config['ADMIN_USERNAME'] and password == current_app.config['ADMIN_PASSWORD']:
            session['is_admin'] = True
            return redirect(url_for('admin.dashboard'))
        else:
            error = "ACCESS DENIED"
            
    return render_template('admin_login.html', error=error)

@admin_bp.route('/logout', methods=['GET', 'POST', 'POST'])
def logout():
    session.pop('is_admin', None)
    return redirect(url_for('admin.login'))

@admin_bp.route('/dashboard', methods=['GET'])
def dashboard():
    if not is_authenticated():
        return redirect(url_for('admin.login'))
        
    pastes = Paste.query.order_by(Paste.created_at.desc()).all()
    # Ensure datetime parsing ignores timezone for simple display if needed
    return render_template('admin_dashboard.html', pastes=pastes, base_url=request.host_url)

@admin_bp.route('/delete/<paste_id>', methods=['POST'])
def delete_paste(paste_id):
    if not is_authenticated():
        abort(403)
        
    paste = Paste.query.filter_by(paste_id=paste_id).first()
    if paste:
        paste.deleted_at = datetime.now(UTC)
        db.session.commit()
        
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/batch_delete', methods=['POST'])
def batch_delete():
    if not is_authenticated():
        abort(403)
        
    paste_ids = request.form.getlist('paste_ids')
    if paste_ids:
        Paste.query.filter(Paste.paste_id.in_(paste_ids)).update({Paste.deleted_at: datetime.now(UTC)}, synchronize_session=False)
        db.session.commit()
        
    return redirect(url_for('admin.dashboard'))

from datetime import timedelta
from flask import send_file, Response

@admin_bp.route('/edit/<paste_id>', methods=['GET'])
def edit_paste(paste_id):
    if not is_authenticated():
        abort(403)
    paste = Paste.query.filter_by(paste_id=paste_id).first_or_404()
    return render_template('admin_edit.html', paste=paste)

@admin_bp.route('/update/<paste_id>', methods=['POST'])
def update_paste(paste_id):
    if not is_authenticated():
        abort(403)
        
    paste = Paste.query.filter_by(paste_id=paste_id).first_or_404()
    
    action = request.form.get('action')
    if action == 'restore':
        paste.deleted_at = None
    elif action == 'permanent':
        paste.expired_at = datetime(9999, 12, 31, 23, 59, 59, tzinfo=UTC)
    elif action == 'extend':
        d = int(request.form.get('days', 0))
        h = int(request.form.get('hours', 0))
        m = int(request.form.get('minutes', 0))
        
        if paste.is_expired():
            base_time = datetime.now(UTC)
        else:
            base_time = paste.expired_at.replace(tzinfo=UTC)
            
        paste.expired_at = base_time + timedelta(days=d, hours=h, minutes=m)
        
    db.session.commit()
    return redirect(url_for('admin.edit_paste', paste_id=paste_id))
    
@admin_bp.route('/view_raw/<paste_id>')
def view_raw(paste_id):
    if not is_authenticated():
        abort(403)
        
    paste = Paste.query.filter_by(paste_id=paste_id).first_or_404()
    
    if paste.filename:
        path = os.path.join(current_app.config['UPLOAD_FOLDER'], paste.paste_id)
        if os.path.exists(path):
            return send_file(path, as_attachment=False, mimetype=paste.mimetype)
        else:
            return "File physically missing from disk.", 404
    else:
        return Response(paste.content, mimetype='text/plain', content_type='text/plain; charset=utf-8')
