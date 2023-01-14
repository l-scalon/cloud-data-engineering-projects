@ECHO OFF
docker start tema11c
docker wait tema11c
docker cp tema11c:/tema11/scripts/output/ ..\docker-elk\logstash\
aws s3 ..\docker-elk\logstash\output\ s3://path/to/tweets/