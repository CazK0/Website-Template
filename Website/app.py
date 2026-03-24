from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_lumina'
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'admin' and password == 'password123':
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', error=True)
            
    return render_template('login.html', error=False)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    all_messages = ContactMessage.query.all()
    return render_template('admin.html', messages=all_messages)

if __name__ == '__main__':
    app.run(debug=True)
