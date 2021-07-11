FROM python:3.9.6

LABEL MAINTAINER="Konstantin Gavrilov @konstgav"

ENV GROUP_ID=1000 \
    USER_ID=1000

WORKDIR /app

COPY . /app
RUN pip3 install -r requirements.txt

EXPOSE 5000
RUN ls
CMD ["python3", "api.py"]