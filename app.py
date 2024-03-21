import flask
app = flask.Flask(__name__)


@app.route("/")
@app.route("/hello")
def hello():
    return "Hello, World2!"


@app.route('/data/appInfo/<name>', methods=['GET'])
def queryDataMessageByName(name):
    print("type(name) : ", type(name))
    return 'String => {}'.format(name)


@app.route('/data/appInfo/id/<int:id>', methods=['GET'])
def queryDataMessageById(id):
    print("type(id) : ", type(id))
    return 'int => {}'.format(id)


if __name__ == '__main__':
    app.run()
