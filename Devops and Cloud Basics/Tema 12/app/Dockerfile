FROM python:3

RUN mkdir /tema12/
WORKDIR /tema12/
COPY . /tema12/

RUN pip3 install -r requirements.txt

CMD ["python", "./scripts/main.py"]