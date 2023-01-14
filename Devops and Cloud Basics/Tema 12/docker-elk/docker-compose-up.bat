@ECHO OFF
mkdir .\logstash\output\
aws s3 sync s3://path/to/tweets/ .\logstash\output\
docker-compose up