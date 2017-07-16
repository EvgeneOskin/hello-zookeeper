FROM python:3.6-alpine

RUN pip install pipenv
ADD Pipfile Pipfile.lock ./

RUN apk --update --no-cache add \
        gcc musl-dev python-dev libev-dev \
    && pipenv install --system
ADD main.py .

CMD python -u main.py
