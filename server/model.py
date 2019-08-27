import keras
import numpy as np
from sklearn.externals import joblib
from sklearn import preprocessing


class Model:

    model = None
    scaler = None

    def __init__(self, model_path, scaler_path):
        # load compiled keras model
        # or whatever, just load some things
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)

    def predict(self, features):
    
        if self.model is not None and self.scaler is not None:
          
            features = self.scaler.transform([features]) 
            prediction = np.exp( self.model.predict(features) )

            return prediction

        # Jak model nie taki to wyjatek
        raise RuntimeError
