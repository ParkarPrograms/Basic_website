from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import *
from database import cursor, db
import smtplib


def send(message, to_address):
    your_email = "your_email"
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()

    connection.login(user=f"{your_email}",password="Password")
    connection.sendmail(from_addr=f"{your_email}", to_addrs=f"{to_address}",
                        msg=message)


class OrderForm(FlaskForm):
    name = StringField("Name:", validators = [validators.DataRequired()])

    number = StringField("Number:", validators = [validators.DataRequired(), validators.Length(min=8, max=8, message="Please enter an eight digit Kuwait number")])
    email = EmailField("Email:", validators=[validators.data_required(), validators.Email()])
    Address = StringField("Address: ", validators=[validators.DataRequired(), validators.Length(min= 20, message= "Your address is too short. Make sure to include street number, block number, area name and landmark")])
    Order = SelectField("What would you like?", choices=["Cupcake", "Tall cake", "Cheesecake", "Loaves"], validators = [validators.DataRequired()])
    Specifications = StringField("How would you like your order? (Specify colour, addition of macarons/flowers or "
                                 "other preferences)")
    OrderType = SelectField("would you pick up your food ?", choices=["pickup", "delivery"])
    DateOfFood = DateField("When would you like your cakes?", format = 'dd/mm/yyyy', validators = [validators.DataRequired()])
    submit = SubmitField("submit")




app = Flask(__name__)
app.config['SECRET_KEY'] = "SECRET_KEY"
Bootstrap(app)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/Menu")
def menu():
    return render_template("menu.html")


@app.route("/Order", methods=['GET', 'POST'])
def order():
    form = OrderForm()
    if form.validate_on_submit():
        return redirect(url_for('thanks'))
    return render_template('order.html', form=form)



@app.route('/Thanks', methods=['POST'])
def form_submission():

    name = request.form['name']
    number = request.form['number']
    email = request.form['email']
    address = request.form['Address']
    specifications = request.form['Specifications']
    order_type = request.form['OrderType']
    date_of_food = request.form['DateOfFood']
    cakes = request.form.getlist('cakes')
    quantities = request.form.getlist('field2')
    cake_order = {cakes[i]:quantities[i] for i in range(len(cakes))}
    cake_order = str(cake_order)
    cursor.execute(f"INSERT INTO Cake_Orders VALUES(?,?,?,?,?,?,?,?)", (name, number, email, address, cake_order, specifications, order_type, date_of_food))
    db.commit()

    def message(subject):
        send_message = 'Subject: {}\n\n{}'.format(f"{subject}",  f"Name: {name}\n"
                                                                   f"Number: {number}\n"
                                                                   f"Email: {email}\n"
                                                                   f"Address: {address}\n"
                                                                   f"Order: {cake_order}\n"
                                                                   f"Specifications: {specifications}\n"
                                                                   f"order_type: {order_type}\n"
                                                                   f"Date of delivery/pickup: {date_of_food}")
        return send_message
    send(message("You have a new order!!"), "Your_email")
    send(message("Thank you for ordering!"), f"{email}")

    return render_template('thanks.html')


@app.route('/add_line')
def add_line():
    line_number = request.args.get('line_number')
    return render_template('form_line.html', line_number=line_number)


if __name__ == "__main__":
     app.run(debug=True)