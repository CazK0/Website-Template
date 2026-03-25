from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'super_secret_python_key'

QUESTIONS = [
    {
        "text": "What is the output of this code?\n\ndef add_item(item, lst=[]):\n    lst.append(item)\n    return lst\n\nprint(add_item(1))\nprint(add_item(2))",
        "options": ["[1], [2]", "[1], [1, 2]", "[1], Error", "Error, [2]"],
        "answer": "[1], [1, 2]"
    },
    {
        "text": "What is the primary purpose of the Global Interpreter Lock (GIL) in CPython?",
        "options": ["To make multithreading faster",
                    "To prevent multiple threads from executing Python bytecodes at once",
                    "To lock the database during writes", "To manage memory leaks"],
        "answer": "To prevent multiple threads from executing Python bytecodes at once"
    },
    {
        "text": "Which of these is a Generator Expression?",
        "options": ["[x for x in range(10)]", "{x: x*2 for x in range(10)}", "(x for x in range(10))",
                    "{x for x in range(10)}"],
        "answer": "(x for x in range(10))"
    },
    {
        "text": "What does @functools.wraps do when writing a custom decorator?",
        "options": ["Speeds up execution", "Preserves the original function's metadata (like __name__)",
                    "Automatically caches return values", "Prevents the function from throwing exceptions"],
        "answer": "Preserves the original function's metadata (like __name__)"
    }
]


@app.route('/')
def home():
    session['score'] = 0
    session['q_index'] = 0
    return render_template('home.html')


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'q_index' not in session:
        return redirect(url_for('home'))

    index = session['q_index']

    if index >= len(QUESTIONS):
        return redirect(url_for('result'))

    current_q = QUESTIONS[index]

    if request.method == 'POST':
        user_answer = request.form.get('answer')
        if user_answer == current_q['answer']:
            session['score'] += 1

        session['q_index'] += 1
        return redirect(url_for('quiz'))

    return render_template('quiz.html', question=current_q, q_num=index + 1, total=len(QUESTIONS))


@app.route('/result')
def result():
    if 'score' not in session:
        return redirect(url_for('home'))

    score = session['score']
    total = len(QUESTIONS)
    return render_template('result.html', score=score, total=total)


if __name__ == '__main__':
    app.run(debug=True)
