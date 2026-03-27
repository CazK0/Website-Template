from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'super_secret_python_key'

QUESTIONS = [
    {
        "text": "What is the output of this code?\n\ndef add_item(item, lst=[]):\n    lst.append(item)\n    return lst\n\nprint(add_item(1))\nprint(add_item(2))",
        "options": ["[1], [2]", "[1], [1, 2]", "[1], Error", "Error, [2]"],
        "answer": "[1], [1, 2]",
        "explanation": "Default arguments are evaluated ONCE when the function is defined, not each time it's called. Both calls share the exact same list in memory."
    },
    {
        "text": "What is the primary purpose of the Global Interpreter Lock (GIL) in CPython?",
        "options": ["To make multithreading faster", "To prevent multiple threads from executing Python bytecodes at once", "To lock the database during writes", "To manage memory leaks"],
        "answer": "To prevent multiple threads from executing Python bytecodes at once",
        "explanation": "The GIL is a lock that protects access to Python objects. It prevents multiple threads from executing Python bytecodes at once, which limits true parallel multithreading but keeps memory safe."
    },
    {
        "text": "Which of these is a Generator Expression?",
        "options": ["[x for x in range(10)]", "{x: x*2 for x in range(10)}", "(x for x in range(10))", "{x for x in range(10)}"],
        "answer": "(x for x in range(10))",
        "explanation": "Parentheses create a generator expression, which evaluates lazily (one item at a time) to save memory. Brackets make a list, and braces make a dictionary or set."
    },
    {
        "text": "What does @functools.wraps do when writing a custom decorator?",
        "options": ["Speeds up execution", "Preserves the original function's metadata (like __name__)", "Automatically caches return values", "Prevents the function from throwing exceptions"],
        "answer": "Preserves the original function's metadata (like __name__)",
        "explanation": "Without @wraps, a decorated function loses its original name and docstring. @wraps copies that metadata over so debugging remains easy."
    }
]

@app.route('/')
def home():
    session['score'] = 0
    session['q_index'] = 0
    session['user_answers'] = []
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
        
        answers = session.get('user_answers', [])
        answers.append(user_answer)
        session['user_answers'] = answers
        
        if user_answer == current_q['answer']:
            session['score'] += 1
            
        session['q_index'] += 1
        return redirect(url_for('quiz'))
        
    return render_template('quiz.html', question=current_q, q_num=index+1, total=len(QUESTIONS))

@app.route('/result')
def result():
    if 'score' not in session:
        return redirect(url_for('home'))
    
    score = session['score']
    total = len(QUESTIONS)
    user_answers = session.get('user_answers', [])
    
    return render_template('result.html', score=score, total=total, questions=QUESTIONS, user_answers=user_answers)

if __name__ == '__main__':
    app.run(debug=True)
