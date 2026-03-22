from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lumina.db'
db = SQLAlchemy(app)

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        user_email = request.form.get('email')
        user_message = request.form.get('message')
        
        new_inquiry = ContactMessage(email=user_email, message=user_message)
        db.session.add(new_inquiry)
        db.session.commit()
        
        return render_template('contact.html', success=True)
        
    return render_template('contact.html', success=False)

if __name__ == '__main__':
    app.run(debug=True)
