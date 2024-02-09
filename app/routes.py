from flask import render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import  login_user, login_required, logout_user, current_user
from app.forms import LoginForm,UserForm
from app.models import Articles, Category, Room, Message, User, Product
from app import app, db,login_manager,bcrypt
from datetime import datetime
import urllib.parse  # Ajout de l'importation nécessaire
from .models import db, Articles, Room, Message  # Assurez-vous d'ajuster l'importation en fonction de votre structure de projet





@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    user_form = UserForm()
    if user_form.validate_on_submit():
        username = user_form.username.data
        email = user_form.email.data
        password = user_form.password.data
        psw_hach = bcrypt.generate_password_hash(password).decode('utf8')
    
        user =User(username=username,email=email,password=psw_hach)
        print(user)
        db.session.add(user)
        db.session.commit()
        
        flash("Utilisateur enregistré avec succès! ")
        return redirect(url_for('connexion'))
    return render_template('inscription.html',form=user_form)

@app.route('/', methods=['GET', 'POST'])
def connexion():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data

        user = User.query.filter_by(email=email).first()
        if user is None:
          flash("Ce mail n'a pas été enregistré")
          print("ERREUR : MAIL INEXISTANT")
          return render_template("connexion.html", login_form=login_form)

        
        pswd_unhashed = bcrypt.check_password_hash(user.password, password)

        if not user :
            flash("Ce mail n'a pas été enregistré")
            print("ERREUR : MAIL INEXISTANT")
            return render_template("connexion.html", login_form=login_form)
        
       
       

        if pswd_unhashed:
            login_user(user)
            flash("Vous êtes connecté")
            return redirect(url_for('accueil'))
        else:
           # Mot de passe incorrect
           flash("Mot de passe incorrect")
           print("ERREUR : MOT DE PASSE INCORRECT")
           return redirect(url_for('connexion'))
            

      
    
    # Si le formulaire n'est pas valide ou les informations sont incorrectes,
    # afficher la page de connexion avec le formulaire et les messages d'erreur.
    return render_template('connexion.html', login_form=login_form)






@app.route('/deconnexion')
@login_required
def deconnexion():
    logout_user()
    return redirect(url_for('connexion'))

@app.route('/accueil')
@login_required
def accueil():
    return render_template('accueil.html')

from werkzeug.utils import secure_filename



@app.route('/article', methods=['GET', 'POST'])
@login_required
def article():
    message = ''
    categories = Category.query.all()
    photos = Articles.query.all()

    if request.method == 'POST':
        image = request.files.get('image')
        text = request.form.get('text', '')
        titre = request.form.get('titre', '')
        categorie_id = request.form.get('categorie', '')

        if image and text and titre and categorie_id:
            try:
                # Validation du type de fichier (exemple : uniquement des images)
                allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
                if '.' in image.filename and image.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
                    # Assurer des noms de fichiers uniques
                    filename = secure_filename(image.filename)
                    
                    categorie = Category.query.get(categorie_id)
                    article = Articles(image=filename, text=text, titre=titre, date=datetime.utcnow(), categorie=categorie, user=current_user)
                    db.session.add(article)
                    db.session.commit()
                    
                    flash('Article ajouté avec succès.', 'success')
                    return redirect(url_for('liste'))
                else:
                    message = "Type de fichier non autorisé. Veuillez télécharger une image (png, jpg, jpeg, gif)."
            except Exception as e:
                # Gestion des erreurs, par exemple si la catégorie n'est pas trouvée
                db.session.rollback()
                message = f"Erreur lors de l'ajout de l'article : {str(e)}"
        else:
            message = "Veuillez remplir tous les champs !"

    return render_template('Article.html', message=message, categories=categories, photos=photos)


@login_required
@app.route('/liste')
def liste():
    photos = Articles.query.order_by(Articles.date.desc()).all()
    return render_template('Liste.html', photos=photos)

@login_required
@app.route('/delete_photo/<int:photo_id>')
def delete_photo(photo_id):
    photo = Articles.query.get_or_404(photo_id)

    if photo.user == current_user:
        db.session.delete(photo)
        db.session.commit()
        flash('Photo supprimée avec succès.', 'success')
    else:
        flash('Vous n\'avez pas la permission de supprimer cette photo.', 'danger')

    return redirect(url_for('liste'))


@login_required
@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    if user.username == current_user:
        db.session.delete(user)
        db.session.commit()
        flash('Utilisateur supprimé avec succès.', 'success')
    else:
        flash('Vous n\'avez pas la permission de supprimer cet utilisateur', 'danger')

    return redirect(url_for('user'))


@login_required
@app.route('/user')
def user():
    users = User.query.all()
    return render_template('user.html', users=users)


@login_required
@app.route('/update/<int:photo_id>', methods=['GET', 'POST'])
def update(photo_id):
    message = ''
    categories = Category.query.all()
    photo = Articles.query.get_or_404(photo_id)

    if photo.user == current_user:
        if request.method == 'POST':
            image = request.files.get('image')
            text = request.form.get('text', '')
            titre = request.form.get('titre', '')
            categorie_id = request.form.get('categorie', '')

            if image and text and titre and categorie_id:
                categorie = Category.query.get(categorie_id)
                photo.image = image.filename
                photo.text = text
                photo.titre = titre
                photo.categorie = categorie
                db.session.commit()
                flash('Article modifié avec succès.', 'success')
                return redirect(url_for('liste'))
                
            else:
                flash('Veuillez remplir tous les champs !', 'danger')
    else:
        flash('Vous n\'avez pas la permission de modifier cette photo.', 'danger')

    return render_template('update.html', message=message, categories=categories, photo=photo)

@login_required
@app.route('/index')
def index():
    photos = Articles.query.all()
    ajouts = Category.query.all()
    return render_template('index.html', photos=photos, ajouts=ajouts, user=current_user)

@login_required
@app.route('/categorie', methods=['GET', 'POST'])
def categorie():
    message = ''
    ajouts = Category.query.all()

    if request.method == 'POST':
        name_categorie = request.form.get('name_categorie', '')

        if name_categorie:
            categorie = Category(name_categorie=name_categorie)
            db.session.add(categorie)
            db.session.commit()
            flash('La catégorie a été ajoutée avec succès !', 'success')
            return redirect(url_for('index'))
        else:
            message = "Veuillez remplir tous les champs !"

    return render_template('categorie.html', message=message, ajouts=ajouts)




@login_required
@app.route('/home')
def home():
    photos = Articles.query.all()
    return render_template('home.html', photos=photos, user=current_user)


@app.route('/room/<room>')
@login_required  # Déplacez la décoration au-dessus de la fonction
def room(room):
    # username = request.args.get('username')  # Pas nécessaire ici, à moins que vous ne prévoyiez de l'utiliser
    room_details = Room.query.filter_by(name=room).first()
    return render_template('room.html', user=current_user, room=room, room_details=room_details)


@app.route('/checkview', methods=['POST'])
@login_required
def checkview():
    room = request.form['room_name']
    username = request.form['username']

    if Room.query.filter_by(name=room).first():
        return redirect(url_for('room', room=room))  # Supprimer l'argument 'username'
    else:
        new_room = Room(name=room)
        db.session.add(new_room)
        db.session.commit()
        return redirect(url_for('room', room=room))  # Supprimer l'argument 'username'


@app.route('/send', methods=['POST'])
@login_required
def send():
    message = request.form.get('message')
    room_id = request.form.get('room_id')

    # Utilisez directement current_user au lieu de récupérer l'utilisateur depuis la base de données
    new_message = Message(value=message, user=current_user, room_id=room_id)

    db.session.add(new_message)
    db.session.commit()
    return redirect(url_for('room', room=room_id))  # Utilisez room_id au lieu de username


@app.route('/getCommentaires/<room>/', methods=['GET'])
@login_required
def get_messages(room):

    room_details = Room.query.filter_by(name=room).first()

    if room_details:
        messages = Message.query.filter_by(room_id=room_details.id).order_by(Message.date).all()

        messages_data = [
            {
                'user': message.user.username,
                'value': message.value,
                'date': message.date.strftime('%Y-%m-%dT%H:%M:%S')  # Assurez-vous du format de date approprié
            }
            for message in messages
        ]
        return jsonify({"messages": messages_data})
    else:
        # Gérez le cas où la salle n'existe pas
        return jsonify({"messages": []})
        

@login_required 
@app.route('/welcome')
def welcome():
    return render_template('Welcome.html')

@login_required
@app.route('/contenu')
def contenu():
    photos = Articles.query.all()
    return render_template('Blog.html', photos=photos, user=current_user)


@login_required
@app.route('/contact')
def contact():
    return render_template('ContactUS.html')

@login_required
@app.route('/panier')
def panier():
    total = 0
    products = []
    session_panier = session.get('panier', {})
    if session_panier:
        ids = session_panier.keys()
        products_data = Product.query.filter(Product.id.in_(ids)).all()
        for product_data in products_data:
            quantity = session_panier.get(str(product_data.id), 0)  # Conversion en str pour l'utilisation comme clé
            subtotal = product_data.price * quantity
            total += subtotal
            # Ajout de la quantité au produit
            product = {
                'data': product_data,
                'quantity': quantity
            }
            products.append(product)
    return render_template('panier.html', products=products, total=total)


@login_required
@app.route('/gestion_panier', methods=['GET', 'POST'])
def gestion_panier():
    if request.method == 'GET' and 'del' in request.args:
        id_del = int(request.args['del'])
        session_panier = session.get('panier', {})
        if id_del in session_panier:
            del session_panier[str(id_del)]  # Conversion en str pour l'utilisation comme clé
            session['panier'] = session_panier

    elif request.method == 'POST' and 'valider' in request.form:
        session_panier = session.get('panier', {})
        total = sum(Product.query.get(int(product_id)).price * qty for product_id, qty in session_panier.items())  # Conversion en int pour la récupération du produit
        message = "Votre panier est vide !!!" if not session_panier else "!!! La Commande a été validée avec succès !!!"
        message += "<h5>*** le Montant à payer est {} €</h5>".format(total)

        return render_template('panier.html', message=message)

    return redirect(url_for('panier'))


@login_required
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    produit = Product.query.get(product_id)
    if produit is None:
        return "Ce produit n'existe ", 404

    session_panier = session.get('panier', {})
    session_panier[str(product_id)] = session_panier.get(str(product_id), 0) + 1  # Conversion en str pour l'utilisation comme clé
    session['panier'] = session_panier
    return redirect(url_for('panier'))


@login_required
@app.route('/delete_product/<int:product_id>')
def delete_product(product_id):
    session_panier = session.get('panier', {})
    if str(product_id) in session_panier:  # Conversion en str pour l'utilisation comme clé
        del session_panier[str(product_id)]
        session['panier'] = session_panier
    return redirect(url_for('panier'))


@login_required
@app.route('/shop')
def products_list():
    products = Product.query.all()
    return render_template('Shop.html', products=products)



@login_required
@app.route('/vitrine')
def vitrine():
    return render_template('vitrine.html')

@login_required
@app.route('/produit', methods=['GET', 'POST'])
def produit():
    message = ''
    products = Product.query.all()

    if request.method == 'POST':
        img = request.files.get('img')
        name = request.form.get('name', '')
        price = request.form.get('price', '')

        if img and name and price:
            try:
                # Validation du type de fichier (exemple : uniquement des images)
                allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
                if '.' in img.filename and img.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
                    # Assurer des noms de fichiers uniques
                    filename = secure_filename(img.filename)

                    produit = Product(img=filename, name=name, price=price, date=datetime.utcnow())
                    db.session.add(produit)
                    db.session.commit()

                    flash('Le produit a été ajouté avec succès.', 'success')
                    return redirect(url_for('stock'))
                else:
                    message = "Veuillez remplir convenablement tous les champs !"

            except Exception as e:
                message = "Une erreur s'est produite lors de l'ajout du produit."

    return render_template('Ajout.html', message=message, products=products)

@login_required
@app.route('/stock')
def stock():
    products = Product.query.order_by(Product.date.desc()).all()
    return render_template('Stock.html', products=products)

@login_required
@app.route('/delete_stock/<int:product_id>')
def delete_stock(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Produit supprimé avec succès.', 'success')
    return redirect(url_for('stock'))



@app.route('/master')
def master():
    return render_template('master.html')


@login_required
@app.route('/admin')
def admin():
    photos = Articles.query.order_by(Articles.date.desc()).all()
    return render_template('admin.html', photos=photos)
