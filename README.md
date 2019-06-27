# resale-global-rest

docker-compose build

docker-compose up 

sudo docker-compose run web ./manage.py makemigrations ${app}

sudo docker-compose run web ./manage.py migrate

curl -X POST -d 'email=kevyn@resaleglobal.com&password=test' http://0.0.0.0:8000/account/v1/register
curl -X POST -d 'email=carolyn@resaleglobal.com&password=test' http://0.0.0.0:8000/account/v1/register


curl -X POST -d 'email=got@gmail.com&password=test' http://0.0.0.0:8000/account/v1/auth/login


curl -X POST -d 'shopifyKey=asdfasdfasdfasdfasdfadf' 'http://localhost:8000/admin/v1/1/shopify-key' -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoia2V2eW5AcmVzYWxlZ2xvYmFsLmNvbSIsInVzZXJuYW1lIjoia2V2eW5AcmVzYWxlZ2xvYmFsLmNvbSIsImV4cCI6MTU2MTYxMDgxOCwiZW1haWwiOiJrZXZ5bkByZXNhbGVnbG9iYWwuY29tIn0.KbWmjkRnBM04pUG6VpNLDiEWfT2n85XJxoA4wumGwto'

curl -X POST -d '[{"name":"test6","name":"test12","name":"test15"}]' 'http://localhost:8000/reseller/v1/1/categories' -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoia2V2eW5AcmVzYWxlZ2xvYmFsLmNvbSIsInVzZXJuYW1lIjoia2V2eW5AcmVzYWxlZ2xvYmFsLmNvbSIsImV4cCI6MTU2MTYxMDgxOCwiZW1haWwiOiJrZXZ5bkByZXNhbGVnbG9iYWwuY29tIn0.KbWmjkRnBM04pUG6VpNLDiEWfT2n85XJxoA4wumGwto'

curl 'http://localhost:8000/reseller/v1/1/categories' -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoia2V2eW5AcmVzYWxlZ2xvYmFsLmNvbSIsInVzZXJuYW1lIjoia2V2eW5AcmVzYWxlZ2xvYmFsLmNvbSIsImV4cCI6MTU2MTYxMDgxOCwiZW1haWwiOiJrZXZ5bkByZXNhbGVnbG9iYWwuY29tIn0.KbWmjkRnBM04pUG6VpNLDiEWfT2n85XJxoA4wumGwto'

