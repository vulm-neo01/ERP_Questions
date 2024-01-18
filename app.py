from flask import Flask, render_template, request, redirect, url_for
import csv
import random

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Đọc dữ liệu từ file CSV
    data = read_csv('processed_data.csv')

    # Kiểm tra xem toàn bộ dữ liệu đã được nhập đầy đủ hay không
    if not all(data.values()):
        return "Dữ liệu không đầy đủ. Vui lòng kiểm tra lại."

    chapters = get_unique_chapters('processed_data.csv')
    chapter = data['Chương']
    question = data['Câu hỏi']
    options = [data['A'], data['B'], data['C'], data['D']]
    correct_answer = data['correct_answer']

    return render_template('index.html', chapters=chapters, chapter=chapter, question=question, options=options, correct_answer=correct_answer)

@app.route('/random_question')
def random_question():
    # Thực hiện logic random câu hỏi ở đây
    # Lấy danh sách tất cả các câu hỏi từ file CSV
    all_questions = read_all_questions('processed_data.csv')

    # Kiểm tra xem toàn bộ dữ liệu đã được nhập đầy đủ hay không
    if not all_questions:
        return "Dữ liệu không đầy đủ. Vui lòng kiểm tra lại."

    # Chọn ngẫu nhiên một câu hỏi mới
    random_question = random.choice(all_questions)

    # Lấy thông tin của câu hỏi mới
    chapters = get_unique_chapters('processed_data.csv')
    chapter = random_question['Chương']
    question = random_question['Câu hỏi']
    options = [random_question['A'], random_question['B'], random_question['C'], random_question['D']]
    correct_answer = random_question['correct_answer']

    # Chuyển hướng đến trang chính với câu hỏi mới
    return render_template('index.html', chapters=chapters, chapter=chapter, question=question, options=options, correct_answer=correct_answer)

def get_unique_chapters(file_path):
    # Đọc dữ liệu từ file CSV và trả về danh sách các chương duy nhất
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        unique_chapters = set(row['Chương'] for row in reader if row['Chương'])
        return sorted(unique_chapters)

def read_all_questions(file_path):
    # Đọc tất cả các câu hỏi từ file CSV và trả về dưới dạng danh sách
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

@app.route('/select_questions_by_chapter', methods=['GET'])
def select_questions_by_chapter():
    selected_chapter = request.args.get('chapter')

    if not selected_chapter:
        return "Vui lòng chọn một chương trước khi tiếp tục."

    # Lấy danh sách câu hỏi từ dữ liệu cho chương được chọn
    questions = get_questions_by_chapter('processed_data.csv', selected_chapter)

    # Kiểm tra xem có câu hỏi nào hay không
    if not questions:
        return f"Không có câu hỏi cho chương {selected_chapter}"

    # Chọn ngẫu nhiên một câu hỏi
    selected_question = random.choice(questions)

    chapters = get_unique_chapters('processed_data.csv')
    # Lấy thông tin của câu hỏi
    question = selected_question['Câu hỏi']
    options = [selected_question['A'], selected_question['B'], selected_question['C'], selected_question['D']]
    correct_answer = selected_question['correct_answer']

    return render_template('index.html', chapters=chapters, chapter=selected_chapter, question=question, options=options, correct_answer=correct_answer)

def get_questions_by_chapter(file_path, chapter):
    # Đọc tất cả các câu hỏi từ file CSV và trả về danh sách câu hỏi cho chương được chọn
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        chapter_questions = [row for row in reader if row['Chương'] == chapter]
        return chapter_questions

def read_csv(file_path):
    # Hàm đọc dữ liệu từ file CSV và trả về dưới dạng từ điển
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return next(reader)
    


if __name__ == '__main__':
    app.run(debug=True)
