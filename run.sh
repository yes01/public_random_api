docker stop flask
docker rm flask
docker rmi flask/api:v2.0
docker build -t flask/api:v2.0 .
docker run -d -uroot -p 5000:5000 --name flask  flask/api:v2.0