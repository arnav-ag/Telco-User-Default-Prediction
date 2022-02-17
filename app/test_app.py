from fastapi.testclient import TestClient
import json
from app import app

client = TestClient(app)


def test_empty_predict():
    response = client.post("/predict", data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": [
                    "body",
                    "gender"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": [
                    "body",
                    "seniorcitizen"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": [
                    "body",
                    "partner"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": [
                    "body",
                    "dependents"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": [
                    "body",
                    "tenure"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": [
                    "body",
                    "phoneservice"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": [
                    "body",
                    "paperlessbilling"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": [
                    "body",
                    "monthlycharges"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": [
                    "body",
                    "totalcharges"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": [
                    "body",
                    "multiplelines"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": [
                    "body",
                    "internetservice"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": [
                    "body",
                    "onlinesecurity"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": [
                    "body",
                    "onlinebackup"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": [
                    "body",
                    "deviceprotection"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": [
                    "body",
                    "techsupport"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": [
                    "body",
                    "streamingtv"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": [
                    "body",
                    "streamingmovies"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": [
                    "body",
                    "contract"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": [
                    "body",
                    "paymentmethod"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }


def test_predict_get():
    response = client.get("/predict")
    assert response.status_code == 405
    assert response.json() == {'detail': 'Method Not Allowed'}


def test_predict_missing_field():
    data = {
        "gender": 0,
        "seniorcitizen": 0,
        "partner": 0,
        "dependents": 0,
        "tenure": 0,
        "phoneservice": 0,
        "paperlessbilling": 0,
        "monthlycharges": 0,
        "totalcharges": 0,
        "multiplelines": 0,
        "internetservice": 0,
        "onlinesecurity": 0,
        "onlinebackup": 0,
        "deviceprotection": 0,
        "techsupport": 0,
        "streamingtv": 0,
        "streamingmovies": 0,
        "contract": 0  # missing field paymentmethod
    }
    response = client.post("/predict", data=json.dumps(data))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": [
                    "body",
                    "paymentmethod"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }


def test_predict_value_out_of_range():
    data = {
        "gender": 0,
        "seniorcitizen": 0,
        "partner": 0,
        "dependents": 0,
        "tenure": 0,
        "phoneservice": 0,
        "paperlessbilling": 0,
        "monthlycharges": 0,
        "totalcharges": 0,
        "multiplelines": 0,
        "internetservice": 0,
        "onlinesecurity": 0,
        "onlinebackup": 0,
        "deviceprotection": 0,
        "techsupport": 0,
        "streamingtv": 0,
        "streamingmovies": 0,
        "contract": 0,
        "paymentmethod": 4  # paymentmethod not in [0,1,2,3]
    }

    response = client.post("/predict", data=json.dumps(data))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": [
                    "body",
                    "paymentmethod"
                ],
                "msg": "unexpected value; permitted: 0, 1, 2, 3",
                "type": "value_error.const",
                "ctx": {
                    "given": 4,
                    "permitted": [
                        0,
                        1,
                        2,
                        3
                    ]
                }
            }
        ]
    }


def test_predict_value_floats():
    data = {
        "gender": 0,
        "seniorcitizen": 0,
        "partner": 0,
        "dependents": 0,
        "tenure": 0.5,
        "phoneservice": 0,
        "paperlessbilling": 0,
        "monthlycharges": 0.5,
        "totalcharges": 0.5,
        "multiplelines": 0,
        "internetservice": 0,
        "onlinesecurity": 0,
        "onlinebackup": 0,
        "deviceprotection": 0,
        "techsupport": 0,
        "streamingtv": 0,
        "streamingmovies": 0,
        "contract": 0,
        "paymentmethod": 0 
    }

    response = client.post('/predict', data=json.dumps(data))
    assert response.status_code == 200
    assert 'default' in response.json().keys()

def test_predict_valid_onehotencoded():
    data = {
        "gender": 1,
        "seniorcitizen": 1,
        "partner": 1,
        "dependents": 1,
        "tenure": 0.5,
        "phoneservice": 1,
        "paperlessbilling": 1,
        "monthlycharges": 0.5,
        "totalcharges": 0.5,
        "multiplelines": 2,
        "internetservice": 2,
        "onlinesecurity": 2,
        "onlinebackup": 2,
        "deviceprotection": 2,
        "techsupport": 2,
        "streamingtv": 2,
        "streamingmovies": 2,
        "contract": 2,
        "paymentmethod": 3
    }

    response = client.post('/predict', data=json.dumps(data))
    assert response.status_code == 200
    assert 'default' in response.json().keys()