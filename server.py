from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(80), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()

            data_db = Contact(email=data['email'], message=data['message'], subject=data['subject'])
            db.session.add(data_db)
            db.session.commit()

            return redirect('thankyou.html')
        except:
            return 'Did not save to the database...'
    else:
        return 'Something went wrong. Try again!'


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/<string:url>')
def page(url):
    return render_template(url)


if __name__ == "__main__":
    app.run(debug=True)
