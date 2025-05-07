from . import db
from datetime import datetime, UTC

class Paste(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paste_id = db.Column(db.String(8), unique=True, nullable=False)
    uploader_ip = db.Column(db.String(15), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    expired_at = db.Column(db.DateTime(timezone=True), nullable=False)
    password = db.Column(db.String(100), nullable=True)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Paste {self.paste_id}>'
    
    def to_dict(self):
        if self.is_expired():
            return {'content': "Expired"}
        return {'content': self.content}

    def is_expired(self):
        return datetime.now(UTC) > self.expired_at.replace(tzinfo=UTC)