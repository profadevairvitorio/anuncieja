import os
import re
import uuid

from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, jsonify, send_from_directory

from app import db
from app.models import Advertisement, Category

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
    search_query = request.args.get('q', '')
    category_id = request.args.get('category', '')

    query = Advertisement.query

    if search_query:
        query = query.filter(Advertisement.title.ilike(f'%{search_query}%'))

    if category_id:
        query = query.filter(Advertisement.category_id == category_id)

    ads = query.order_by(Advertisement.created_at.desc()).all()
    categories = Category.query.order_by(Category.name).all()

    return render_template(
        'index.html',
        advertisements=ads,
        categories=categories,
        search_query=search_query,
        selected_category_id=category_id
    )



@bp.route('/anuncio/novo', methods=['GET', 'POST'])
def new_advertisement():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        price = request.form.get('price')
        category_id = request.form.get('category')
        whatsapp_number = request.form.get('whatsapp_number')

        if not all([title, description, price, category_id, whatsapp_number]):
            flash('Por favor, preencha todos os campos obrigatórios.', 'danger')
            categories = Category.query.order_by(Category.name).all()
            return render_template('cadanuncio.html', title='Criar Novo Anúncio', categories=categories)

        cleaned_phone = re.sub(r'\D', '', whatsapp_number)

        category_object = Category.query.get(category_id)
        if not category_object:
            flash('Categoria inválida selecionada.', 'danger')
            categories = Category.query.order_by(Category.name).all()
            return render_template('cadanuncio.html', title='Criar Novo Anúncio', categories=categories)

        picture_file = 'default.jpg'
        if 'picture' in request.files and request.files['picture'].filename != '':
            form_picture = request.files['picture']

        advertisement = Advertisement(
            title=title,
            description=description,
            price=float(price),
            category=category_object,
            whatsapp_number=cleaned_phone,
            image_url=picture_file
        )
        db.session.add(advertisement)
        db.session.commit()

        flash('Seu anúncio foi criado com sucesso!', 'success')
        return redirect(url_for('main.index'))

    categories = Category.query.order_by(Category.name).all()
    return render_template('cadanuncio.html', title='Criar Novo Anúncio', categories=categories)


@bp.route('/categorias', methods=['GET', 'POST'])
def manage_categories():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()

        if not name:
            flash('O nome da categoria não pode ser vazio.', 'danger')
        else:
            existing_category = Category.query.filter(db.func.lower(Category.name) == db.func.lower(name)).first()
            if existing_category:
                flash('Essa categoria já existe.', 'warning')
            else:
                new_category = Category(name=name)
                db.session.add(new_category)
                db.session.commit()
                flash('Categoria adicionada com sucesso!', 'success')

        return redirect(url_for('main.manage_categories'))

    all_categories = Category.query.order_by(Category.name).all()
    return render_template('category_form.html', categories=all_categories, title='Gerenciar Categorias')
