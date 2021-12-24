from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

main = Flask(__name__)
main.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bug.db'
db = SQLAlchemy(main)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique = False, nullable=False)
    text = db.Column(db.String(120), unique = False, nullable=False)
    price = db.Column(db.Integer, unique = False, nullable = False)
    img = db.Column(db.Text, unique = False, default = "default.jpg")

    def __repr__(self):
        return '<Product %r>' % self.id

@main.route('/')
def index():
    products = Product.query.order_by(Product.title).all()
    return render_template("index.html", products=products)

@main.route('/about')
def about():
    return render_template("about.html")

@main.route('/products/<int:id>')
def products(id):
    product = Product.query.get(id)
    return render_template("products.html", product=product)

@main.route('/products/<int:id>/del')
def products_del(id):
    product = Product.query.get_or_404(id)

    try:
        db.session.delete(product)
        db.session.commit()
        return redirect('/')
    except:
        return "Ошибка"


@main.route('/createproduct', methods=['POST', 'GET'])
def createproduct():
    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']
        price = request.form['price']
        
        img = request.files['img']
        if img.filename is not '':
            filename = secure_filename(img.filename)
            img.save(os.path.join(main.root_path, "static/img", img.filename))
        else:
            filename = "default.jpg"
        
        product = Product(title=title, text=text, price=price, img=filename)
        try:
            db.session.add(product)
            db.session.commit()
            return redirect('/')
        except:
            return "Ошибка"
    else:
        return render_template("createproduct.html")


if __name__ == "__main__":
    main.run(debug=True)