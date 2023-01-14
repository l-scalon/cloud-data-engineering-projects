FROM python:3

RUN mkdir /tema11/
WORKDIR /tema11/
COPY . /tema11/

RUN pip3 install -r requirements.txt

CMD ["python", "./scripts/main.py"]