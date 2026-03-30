from flask import Flask, render_template, request, session, redirect, url_for
import requests
import random
import html

app = Flask(__name__)

def fetch_questions():
    url = "https://opentdb.com/api.php?amount=10&category=18&type=multiple"
    response = requests.get(url).json()
    formatted_questions = []
    
    for item in response.get('results', []):
        correct = html.unescape(item['correct_answer'])
        incorrect = [html.unescape(ans) for ans in item['incorrect_answers']]
        options = incorrect + [correct]
        random.shuffle(options)
        
        formatted_questions.append({
            "text": html.unescape(item['question']),
            "options": options,
            "answer": correct,
            "explanation": "External APIs do not provide explanations for their questions."
        })
    return formatted_questions

@app.route('/')
def home():
    session['score'] = 0
    session['q_index'] = 0
    session['user_answers'] = []
    session['questions'] = fetch_questions()
    return render_template('home.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'q_index' not in session or 'questions' not in session:
        return redirect(url_for('home'))
        
    questions = session['questions']
    index = session['q_index']
    
    if index >= len(questions):
        return redirect(url_for('result'))
        
    current_q = questions[index]

    if request.method == 'POST':
        user_answer = request.form.get('answer')
        
        answers = session.get('user_answers', [])
        answers.append(user_answer)
        session['user_answers'] = answers
        
        if user_answer == current_q['answer']:
            session['score'] += 1
            
        session['q_index'] += 1
        return redirect(url_for('quiz'))
        
    return render_template('quiz.html', question=current_q, q_num=index+1, total=len(questions))

@app.route('/result')
def result():
    if 'score' not in session or 'questions' not in session:
        return redirect(url_for('home'))
    
    score = session['score']
    questions = session['questions']
    total = len(questions)
    user_answers = session.get('user_answers', [])
    
    return render_template('result.html', score=score, total=total, questions=questions, user_answers=user_answers)

if __name__ == '__main__':
    app.run(debug=True)
