# resale-global-rest

docker-compose build

docker-compose up 

sudo docker-compose run web ./manage.py makemigrations ${app}

sudo docker-compose run web ./manage.py migrate

curl -X POST -d 'email=got@gmail.com&password=test' http://0.0.0.0:8000/account/v1/register

curl -X POST -d 'email=got@gmail.com&password=test' http://0.0.0.0:8000/account/v1/auth/login