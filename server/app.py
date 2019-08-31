from flask import Flask, jsonify, render_template, request
from model import Model

app = Flask(__name__)
app.secret_key = '35jt34dfsj!hw234@44[1].et1r9'


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('digit_recognition.html')


@app.route('/api/predict', methods=['GET', 'POST'])
def predict():
    request_data = request.values.get('image')
    result = model.predict(request_data)  # make prediction

    return jsonify({"prediction": result.tolist()})


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


if __name__ == '__main__':
    try:
        model = Model("model/model.h5")
        print("Model loaded.")
    except RuntimeError:
        print("Model doesn't exist!")

    app.run(host='0.0.0.0', debug=False, port=5000) # flag debug must be set as False (keras requirements)
