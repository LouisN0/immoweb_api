
def predict(data, model):
    result = model.predict(data).tolist()
    result = result[0]
    return result