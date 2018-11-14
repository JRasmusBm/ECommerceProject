FROM python:3.7

WORKDIR /usr/src/app

COPY Pipfile ./
RUN pip install pipenv
RUN pipenv install --dev --ignore-pipfile

copy . .

EXPOSE 80
