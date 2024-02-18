FROM python:3.11-alpine

WORKDIR /code

COPY requierments.txt /code/requierments.txt
RUN pip install --no-cache-dir --upgrade -r /code/requierments.txt

COPY ./app /code/app

ENTRYPOINT ["python","app/main.py"]