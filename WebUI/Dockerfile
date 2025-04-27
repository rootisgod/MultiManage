FROM python:alpine

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN apk -U upgrade
RUN apk add --no-cache libpq-dev python3-dev gcc musl-dev
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]