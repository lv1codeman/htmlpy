from flask import Flask, render_template
import render
app = Flask(__name__)


@app.route('/')
# def index():
#     # 在这个例子中，我们将向HTML传递一个Python列表
#     items = ["Apple", "Banana", "Orange", "Mango"]
#     return render_template('index.html', items=items)
def index():
    # username = 'John'
    # date = '2022-01-01'
    # items = ["Apple", "Banana", "Orange", "Mango"]
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
