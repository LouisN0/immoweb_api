
import os

print(os.getcwd())
print(os.path.exists(('./preprocessing/data/zipcode_be.xlsx')))
from fastapi import FastAPI
from preprocessing.cleaning_data import preprocess
from predict.prediction import predict
from pydantic import BaseModel
import pickle


app = FastAPI()
model = pickle.load(open('model/finalized_model.sav','rb'))

class House(BaseModel):
    area: int
    proprety_type: str
    rooms_number:int
    zip_code: int
    land_area: int
    garden: bool
    garden_area: int
    equipped_kitchen: bool
    full_address: str
    swimming_pool: bool
    furnished: bool
    open_fire: bool
    terrace: bool
    terrace_area: int
    facades_number: int
    building_state: str

@app.get('/')
def is_connected():
    return {'alive'}

@app.get('/predict')
def prediction_result():
    return {
    "area": "int",
    "property-type": "APARTMENT | HOUSE | OTHERS",
    "rooms-number": "int",
    "zip-code": "int",
    "land-area": "Optional[int]",
    "garden": "Optional[bool]",
    "garden-area": "Optional[int]",
    "equipped-kitchen": "Optional[bool]",
    "full-address": "Optional[str]",
    "swimming-pool": "Optional[bool]",
    "furnished": "Optional[bool]",
    "open-fire": "Optional[bool]",
    "terrace": "Optional[bool]",
    "terrace-area": "Optional[int]",
    "facades-number": "Optional[int]",
    "building-state": "Optional[ NEW | GOOD | TO RENOVATE | JUST RENOVATED | TO REBUILD]"
    }

@app.post('/predict/')
def prediction(request: House):
    model_data = preprocess(request)
    prediction = predict(model_data, model)
    return {prediction}
