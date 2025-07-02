

docker network create myNetwork

docker run -d \
    --name booking_db \
    -p 2345:5432 \
    -e POSTGRES_PASSWORD=Xitem.b00kingX \
    -e POSTGRES_USER=booking \
    -e POSTGRES_DB=booking \
    --network=myNetwork \
    --volume pg-booking-data:/var/lib/postgresql/data \
    postgres:16

docker run -d \
    --name booking_cache \
    --network=myNetwork \
    -p 9736:6379 \
    redis:7.4 

docker run \
    --name booking_nginx \
    --volume .\nginx.conf:/etc/nginx/nginx.conf\
    --network=myNetwork \
    --rm \
    -p 80:80 \
    nginx

docker build -t booking_image .

docker run \
    --name booking_back \
    --network=myNetwork \
    -p 8000:8000 \
    booking_image

docker run \
    --name booking_celery \
    --network=myNetwork \
    booking_image \
    celery --app=src.tasks.tasks:celery_instance worker -l INFO
    

docker run \
    --name booking_celery_beat \
    --network=myNetwork \
    booking_image \
    celery --app=src.tasks.tasks:celery_instance worker -l INFO -B