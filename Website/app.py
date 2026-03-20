from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/pricing')
def pricing():
    return render_template('pricing.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        email = request.form.get('email')
        message = request.form.get('message')

        print(f"--- NEW MESSAGE RECEIVED ---")
        print(f"Email: {email}")
        print(f"Message: {message}")
        print(f"----------------------------")

        return render_template('contact.html', success=True)

    return render_template('contact.html', success=False)


if __name__ == '__main__':
    app.run(debug=True)
