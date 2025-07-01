import re

from . import db
from datetime import datetime


class Advertisement(db.Model):
    __tablename__ = 'advertisements'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    contact_phone = db.Column(db.String(20), nullable=False)
    image_file = db.Column(db.String(255), nullable=False, default='default.jpg')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def whatsapp_link(self):
        if not self.contact_phone:
            return None
        cleaned_phone = re.sub(r'\D', '', self.contact_phone)
        return f"https://wa.me/{cleaned_phone}"

    def __repr__(self):
        return f"Advertisement('{self.title}', '{self.created_at}')"