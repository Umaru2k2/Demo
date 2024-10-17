from flask import Flask, render_template, request
import re

app = Flask(__name__)

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    câu_hỏi = []
    đáp_án = []

    question = ""
    answers = []

    for line in lines:
        line = line.strip()
        
        if line.startswith("Câu"):
            if question:
                câu_hỏi.append(question)
                đáp_án.append(answers)
            question = line
            answers = []

        elif re.match(r'[*]?[A-D][.](.*)', line):
            answers.append(line.strip())

    if question:
        câu_hỏi.append(question)
        đáp_án.append(answers)

    return câu_hỏi, đáp_án

# Khởi tạo câu hỏi và đáp án
câu_hỏi, đáp_án = process_file('quiz_app/tin.txt')

@app.route('/')
def index():
    return render_template('quiz.html', câu_hỏi=câu_hỏi, đáp_án=đáp_án)

@app.route('/submit', methods=['POST'])
def submit():
    score = 0
    user_answers = request.form.to_dict()  # Nhận đáp án từ form
    correct_answers = {i: next((ans[0] for ans in đáp_án[i] if ans.startswith('*')), None) for i in range(len(đáp_án))}

    # Danh sách để lưu đáp án sai
    incorrect_answers = []

    for question_id, user_answer in user_answers.items():
        if user_answer == correct_answers[int(question_id)]:
            score += 1
        else:
            # Nếu đáp án sai, lưu lại câu hỏi, đáp án của người dùng và đáp án đúng
            incorrect_answers.append({
                'question': câu_hỏi[int(question_id)],
                'user_answer': user_answer,
                'correct_answer': correct_answers[int(question_id)],
                'answers': đáp_án[int(question_id)]
            })

    return render_template('result.html', score=score, total=len(câu_hỏi), incorrect_answers=incorrect_answers)

if __name__ == '__main__':
    app.run(debug=True)
