from flask import Flask, render_template, request
from underthesea import classify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Lấy dữ liệu từ ô nhập
        input_text = request.form['input_text']
        # Xử lý dữ liệu và lấy kết quả
        result = process_data(input_text)
        # Trả về template với kết quả
        return render_template('index.html', result=result)
    # Mở trang chủ với form nhập dữ liệu
    return render_template('index.html')

def process_data(input_text):
    # Xử lý dữ liệu ở đây và trả về kết quả
    # Ví dụ:
    result = 'Phân loại: '+ str(classify(input_text))
    return result

if __name__ == '__main__':
    app.run(debug=True)
