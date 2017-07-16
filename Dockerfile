FROM python:3.6-alpine

RUN pip install pipenv
ADD Pipfile Pipfile.lock ./

RUN pipenv install --system
ADD main.py .

CMD python -u main.py
