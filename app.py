from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# Define shopping cart class for database
class cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return '<item %r>' % self.id 


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        item = request.form['item']
        price = request.form['price']

        new_item = cart(item=item, price=price)

        try:
            db.session.add(new_item)
            db.session.commit()
            return redirect('/')

        except:
            return 'There was an issue adding your item to cart'
    else:
        return render_template('index.html')

#Remove item from cart
@app.route('/delete/<int:id>')
def delete(id):
    item_to_delete = cart.query.get_or_404(id)

    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect('checkout.html')
    except:
        return 'There was a problem removing your item'

@app.route('/cart', methods=['GET', 'POST'])
def view_cart():
    items = cart.query.with_entries(cart.item).all()
    #prices = db.session.query.with_entires(cart.price).all()

    return render_template('checkout.html', items=items, prices=prices)

#CHECKOUT
@app.route('/cart', methods=['GET', 'POST'])
def checkout():
    items = cart.query.get_or_404.all(items)
    if request.method == 'POST':

        try:
            db.session.delete.all()
            db.session.commit()
            return "Your order has been submitted successfully"
        except:
            return "There was an issue submitting your order"
    else:
        return render_template('checkout.html', items=items)

if __name__ == "__main__":
    app.run(debug=True)