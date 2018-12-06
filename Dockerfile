FROM python:3.7

RUN mkdir -p /opt/services/djangoapp/src
RUN mkdir -p /opt/services/djangoapp/static
WORKDIR /opt/services/djangoapp/src

COPY Pipfile Pipfile.lock /opt/services/djangoapp/src/
RUN pip install pipenv && pipenv install --dev --system --deploy --ignore-pipfile

COPY . /opt/services/djangoapp/src

EXPOSE 80
