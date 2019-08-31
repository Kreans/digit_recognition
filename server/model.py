import numpy as np
import base64
from PIL import Image
import io
from keras.models import load_model


class Model:
    model = None
    debug = True  # save images to files

    def __init__(self, model_path):

        # load compiled keras model
        self.model = load_model(model_path)
        self.model._make_predict_function()

    def predict(self, image_str):

        if self.model is not None:

            data = self.parse_image(image_str)  # convert string to image (with resize )
            data = np.asarray(data)     # convert image to numpy array
            data = np.invert(data)      # invert pixels (model requirements)
            data = data / 256        # normalize data (model requirements)
            data = data.reshape(1, 28, 28, 1)   # reshape data (model requirements)

            prediction = self.model.predict_proba([data])[0]
            print(prediction)
            return prediction

        else:
            raise RuntimeError

    def parse_image(self, image_str):

        image_str = image_str.replace("data:image/png;base64,", "")
        png = base64.b64decode(image_str)   # decode base64 string

        if self.debug:
            with open('input.png', 'wb') as output:
                output.write(png)

        img = Image.open(io.BytesIO(png))
        img = img.convert('L')      # convert to light scale

        if img.size != (28, 28):        # resize image
            img = img.resize((28, 28), 1)

        if self.debug:
            img.save("input28x28.png")

        return img
