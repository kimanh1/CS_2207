import joblib


def predict(data):
    cb = joblib.load("cb_model.sav")
    return cb.predict(data)