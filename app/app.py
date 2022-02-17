from fastapi import FastAPI
from pydantic import BaseModel
from pydantic.typing import Literal
import pickle
# Overhead
app = FastAPI()
# load
clf = pickle.load(open('../model_training/telco_default_model.json', "rb"))


#Defining the request body format
class request_body(BaseModel):
    gender: Literal[0,1] # 0 is female, 1 is male
    seniorcitizen: Literal[0,1] # 0 is no, 1 is yes
    partner: Literal[0,1] # 0 is no, 1 is yes
    dependents: Literal[0,1] # 0 is no, 1 is yes
    tenure: float # divide by 72
    phoneservice: Literal[0,1] # 0 is no, 1 is yes
    paperlessbilling: Literal[0,1] # 0 is no, 1 is yes
    monthlycharges: float # divide by 118.75
    totalcharges: float # divide by 8684.80
    multiplelines: Literal[0,1,2] # 0 is no, 1 is no phone service, 2 is yes
    internetservice: Literal[0,1,2] # 0 is DSL, 1 is Fibre optic, 2 is no
    onlinesecurity: Literal[0,1,2] # 0 is no, 1 is no internet service, 2 is yes
    onlinebackup: Literal[0,1,2] # 0 is no, 1 is no internet service, 2 is yes
    deviceprotection: Literal[0,1,2] # 0 is no, 1 is no internet service, 2 is yes
    techsupport: Literal[0,1,2] # 0 is no, 1 is no internet service, 2 is yes
    streamingtv: Literal[0,1,2] # 0 is no, 1 is no internet service, 2 is yes
    streamingmovies: Literal[0,1,2] # 0 is no, 1 is no internet service, 2 is yes
    contract: Literal[0,1,2] # 0 is month-to month, 1 is one year, 2 is two years
    paymentmethod: Literal[0,1,2,3] # 0 is bank transfer(automatic), 1 is credit card(automatic), 2 is electronic check, 3 is mailed check
     
# Defining path operation for root endpoint
@app.get('/')
def main():
    return {'message': """Welcome to the telco defaulter predictor! Send a POST request to the /predict endpoint for your prediction.
            Otherwise, check out the /docs endpoint to have a look at the speicifications - you can also attempt to call the /predict endpoint from there!"""}
 
def one_hot_encoder(data, num):
    return [0]*data + [1] + [0]*(num-data-1)

@app.post('/predict')
def predict(data : request_body):
    test_data = [
        [data.gender,
        data.seniorcitizen,
        data.partner,
        data.dependents,
        data.tenure / 72.0,
        data.phoneservice,
        data.paperlessbilling,
        data.monthlycharges / 118.75,
        data.totalcharges / 8684.80] + \
        one_hot_encoder(data.multiplelines,3)+ \
        one_hot_encoder(data.internetservice,3) + \
        one_hot_encoder(data.onlinesecurity,3) + \
        one_hot_encoder(data.onlinebackup,3) + \
        one_hot_encoder(data.deviceprotection,3) + \
        one_hot_encoder(data.techsupport,3) + \
        one_hot_encoder(data.streamingtv,3) + \
        one_hot_encoder(data.streamingmovies,3) + \
        one_hot_encoder(data.contract,3) + \
        one_hot_encoder(data.paymentmethod, 4)
    ]
    print(test_data)
    pred = int(clf.predict(test_data)[0])
    return { 'default' : pred}