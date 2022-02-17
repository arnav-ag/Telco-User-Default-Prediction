<img src = "https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white"><img src = "https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white"> <img src = "https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue"> <img src = "https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white"> <img src = "https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white"> 

This repo holds a FastAPI webapp that is able to predict if a user will default on their telco payments. The data used to train and the [ `.ipynb`](./model_training/telco_model_training.ipynb) files are also provided. The model was trained using the recent [XGBoost](https://github.com/dmlc/xgboost) gradient boosting library.

# Contents

- [Running FastAPI server](#running-fastapi-server)
- [API Endpoint Docs](#api-endpoint-docs)
- [Running Python Notebook](#running-the-notebook)
- [Unit tests](#running-unit-tests)

# Running FastAPI server

You have two options - you may choose to run the code locally on your computer natively, build the docker image locally or pull the docker image from dockerhub. To run the `.ipynb` file used to train the model, jump here.

## Running locally

Firstly, `git clone` this repository or download it as a zip file from above to save it locally.

Next, move into the downloaded folder and install the prerequisite python modules:

```bash
cd <folder-name> && pip install -r requirements.txt
```

Next, we move into our app folder and run our app:

```bash
cd app/
uvicorn app:app --reload
```

Now, the page will be accessible on [`http://127.0.0.1:8000`](http://127.0.0.1:8000), where you will be greeted with a welcome message. Proceed to the [`/docs`](http://127.0.0.1:8000/docs) endpoint to look at the available endpoints along with the required request type and parameters. You may also wish to try the prediction endpoint from here.

## Running using docker

The [`Dockerfile`](./Dockerfile) is provided in this repo. To build the docker image locally, firstly `git clone` this repo. Next, move into the downloaded folder then run:

```bash
docker build -t <image-name> .
```

This will build the image. If you wish to run unit-tests, you may also do so:

```bash
docker build --target unit-tests -t <image-name> .
```

Next, to run the image we simply run

```bash
docker run -p 80:80 <image-name>
```

This will start the FastAPI application in the docker container, mapping port 80 over locally. With the docker instance, we have to access [`http://0.0.0.0:80`](http://0.0.0.0:80) instead of localhost. Similar to running the app locally, you may proceed to the [`/docs`](http://0.0.0.0:80/docs) endpoint to look at the available endpoints along with the required request type and parameters. You may also wish to try the prediction endpoint from here.

## Pulling the docker image

To pull the docker image, simply run:

```bash
docker pull arnavagg/defaultrateprediction:latest
```

Then, to run the image locally, run

```bash
docker run -p 80:80 arnavagg/defaultrateprediction
```

That's it! The app should now be running on [`http://0.0.0.0:80`](http://0.0.0.0:80). Suggestions on what can be done are given in the previous section.

# API Endpoint Docs



There is essentially only one endpoint available - `/predict`. A `POST` request has to be made to this endpoint with the following parameters included in the data section:

```python
gender: Literal[0,1] # 0 is female, 1 is male
seniorcitizen: Literal[0,1] # 0 is no, 1 is yes
partner: Literal[0,1] # 0 is no, 1 is yes
dependents: Literal[0,1] # 0 is no, 1 is yes
tenure: float 
phoneservice: Literal[0,1] # 0 is no, 1 is yes
paperlessbilling: Literal[0,1] # 0 is no, 1 is yes
monthlycharges: float 
totalcharges: float 
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
```

A description of what each parameter represents is given by the name, while the values it can take are given after the colon, further explained below. The comments specify what each integer means.

## Floats

The `tenure`, `monthlycharges` and `totalcharges` fields can take in any float values. While this does include negative numbers, it is not useful as negative numbers would not usually show up in real world situations.

## Literals

A Literal followed by an array means that the integer supplied to that field must be from the array, or will result in an erroneous response to your request. The meaning of each integer in the array is given next to the array, i.e. in the case of:

```python
techsupport: Literal[0,1,2] # 0 is no, 1 is no internet service, 2 is yes
```

The `techsupport`field can only take in values `1`, `2` or `3`, which represent no tech support, no internet service or the inclusion of tech support respectively.

# Running the notebook

You may run the notebook locally, using [jupyter notebook](https://jupyter.org/install) or on [Google Colab](https://colab.research.google.com/). If using Google Colab, remember to upload the `finantier_data_technical_test_dataset.csv` file so that the runtime instance can access it. Then, feel free to play with the individual cells! Run all the cells sequentially to see how I loaded the data, performed data cleaning, engineered a few features and performed encoding. Then, I built a preliminary model after which I performed grid search to seek out the best hyper-parameters for our model and came up with the final one that is in use for the API!

The [preliminary model `.json`](./model_training/preliminary_telco_default_model.json) file is also provided, just in case you value some of the metrics that were affected negatively in the optimised model more. Check out the notebook to learn more about what was affected in different ways and take your pick of model. Just remember to change the FastAPI [`app.py`](./app/app.py) file with the preliminary model JSON file should you choose to use that one instead. 

# Running Unit Tests

Lastly, unit tests are also provided. Should you choose to run them, install `pytest` and `requests` python modules then run the following command in the `app/` file:

```bash
pip install pytest requests
pytest
```

Alternatively, you may also choose to run the tests using docker. In the directory with the provided `Dockerfile`, run the following command:

```bash
docker build --target unit-tests -t <image-name> .
```

