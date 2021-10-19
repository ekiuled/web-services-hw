FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY app ./app
COPY setup.py .
COPY db_setup.py .

RUN python setup.py install
RUN python db_setup.py