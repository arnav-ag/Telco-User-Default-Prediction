FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9 as unit-tests

COPY requirements.txt /app
RUN pip install -r requirements.txt
RUN pip install pytest requests

ADD app /app/
COPY model_training/telco_default_model.json /model_training/

WORKDIR /app
RUN pytest

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9 as serve

COPY requirements.txt /app
RUN pip install -r requirements.txt


COPY app/app.py /app/
COPY model_training/telco_default_model.json /model_training/

WORKDIR /app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]