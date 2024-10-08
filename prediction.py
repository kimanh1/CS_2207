import joblib


def predictForSale(data):
    cb = joblib.load("cb_model_sale.sav")
    return cb.predict(data)
def predictForLease(data):
    cb = joblib.load("cb_model_lease.sav")
    return cb.predict(data)