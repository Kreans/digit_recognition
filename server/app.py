import numpy as np
from flask import Flask, jsonify, render_template, request
import base64
from PIL import Image
import io


app = Flask(__name__)
app.secret_key = '35jt34dfsj!hw234@44[1].et1r9'


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('digit_recognition.html')


@app.route('/api/predict', methods=['GET', 'POST'])
def predict():

    data = parse_image(request.values.get('image'))

    res = np.random.randn(10, 1)

    return jsonify({"prediction": res.tolist(),
                    "passed_values": "ss"})


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


def parse_image(image_str):

    image_str = image_str.replace("data:image/png;base64,", "")
    png = base64.b64decode(image_str)

    with open('output.png', 'wb') as output:
        output.write(png)

    img = Image.open(io.BytesIO(png))
    img = img.convert('L')

    if img.size != (28, 28):
        img = img.resize((28, 28), 1)

    img.save("te_predict.png")
    return img


if __name__ == '__main__':
    try:
       # model = Model("model/model.pkl", "model/scaler.pkl")
        print("Model loaded.")
    except RuntimeError:
        print("Model doesn't exist!")

    app.run(debug=True)
