import re
from . import db
from datetime import datetime, timezone


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    advertisements = db.relationship('Advertisement', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'


class Advertisement(db.Model):
    __tablename__ = 'advertisements'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    whatsapp_number = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    @property
    def whatsapp_link(self):
        if not self.contact_phone:
            return None
        cleaned_phone = re.sub(r'\D', '', self.contact_phone)
        return f"https://wa.me/{cleaned_phone}"

    def __repr__(self):
        return f"Advertisement('{self.title}', '{self.created_at}')"