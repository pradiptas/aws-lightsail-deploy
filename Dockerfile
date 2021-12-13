FROM python:3.8-alpine

RUN apk update && apk upgrade && \
    apk add --no-cache bash git openssh

RUN mkdir /app
WORKDIR /app
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
RUN python -m pip install requests 
RUN python -m pip install python-dotenv
RUN python -m pip install pytz 

COPY . .

EXPOSE 8080

CMD ["python", "app.py"]