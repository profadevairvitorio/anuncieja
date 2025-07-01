import os
import re
import uuid

from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, jsonify

from app import db
from app.models import Advertisement

bp = Blueprint('main', __name__)

def save_picture(form_picture):
    random_hex = uuid.uuid4().hex
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/uploads', picture_fn)
    os.makedirs(os.path.dirname(picture_path), exist_ok=True)
    form_picture.save(picture_path)
    return picture_fn

@bp.route('/')
def index():
    ads = Advertisement.query.order_by(Advertisement.created_at.desc()).all()
    return render_template('index.html', advertisements=ads)


@bp.route('/anuncio/novo', methods=['GET', 'POST'])
def new_advertisement():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        price = request.form.get('price')
        category = request.form.get('category')
        phone_number = request.form.get('contact_phone')
        cleaned_phone = re.sub(r'\D', '', phone_number)

        picture_file = 'default.jpg'
        if 'picture' in request.files and request.files['picture'].filename != '':
            form_picture = request.files['picture']
            picture_file = save_picture(form_picture)

        advertisement = Advertisement(
            title=title,
            description=description,
            price=float(price),
            category=category,
            contact_phone=cleaned_phone,
            image_file=picture_file
        )
        db.session.add(advertisement)
        db.session.commit()

        flash('Seu anúncio foi criado com sucesso!', 'success')
        return redirect(url_for('main.index'))

    return render_template('cadanuncio.html', title='Criar Novo Anúncio')


