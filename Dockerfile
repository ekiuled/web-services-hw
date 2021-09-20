FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY app ./app
COPY setup.py .
RUN python setup.py install