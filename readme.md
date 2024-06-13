# readme

## pm

```json
[
{
"TrackAlive":1,
"speed":"0.04",
"Pos":[1.06,1.52,50.81],
"time":"15:46:56.2"
},
{
"TrackAlive":0,
"speed":"NaN",
"Pos":"NaN",
"time":"15:46:56.2"
}
]
```

## opt

```bash
#4. install pip dependence
pip install -r requirements.txt
#8. start backend
python manage.py runserver 0.0.0.0:9701
#or uvicorn :
python -m uvicorn appuav.asgi:appuav --port 9701 --host 0.0.0.0 --reload --workers 8

#celery:
celery -A appuav worker -l info -P gevent -c 1

#test
python manage.py test uavadmin.adverse.tests
```

### for ubuntu

```bash
apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config
apt-get install postgresql libpq-dev python-dev
```


### docker

```bash
docker build -t py:3.12 .
docker run -d \
        --name=uavadmin_py \
        --hostname=75e2382fd748 \
        --mac-address=02:42:ac:11:00:0a \
        --env=TZ=Asia/Shanghai \
        --env=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
        --env=LANG=C.UTF-8 \
        --log-opt max-size=10m --log-opt max-file=3 \
        --volume=/app \
        --volume=/mnt/f:/mnt/f \
        --volume=/mnt/d:/mnt/d \
        --network=my-net \
        --restart=no \
        --runtime=runc \
        --detach=true \
        py:3.12
```

### pwd

pwd123456
