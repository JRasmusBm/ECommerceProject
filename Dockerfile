FROM python:3.7

RUN mkdir -p /opt/services/djangoapp/src
WORKDIR /opt/services/djangoapp/src

COPY Pipfile Pipfile.lock /opt/services/djangoapp/src/
RUN pip install pipenv && pipenv install --dev --system --deploy --ignore-pipfile

COPY . /opt/services/djangoapp/src

RUN cd berriesandgoods && python manage.py collectstatic --no-input 

EXPOSE 8000
