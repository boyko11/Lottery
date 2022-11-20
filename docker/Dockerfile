FROM python:3.9-alpine

RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev

COPY docker/requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]
ENV PYTHONPATH /app
CMD ["main/web.py" ]