# readme

## pm

### 2024.9.25 数据流

* 飞行器消失条件：speed==-1 or 5分钟没有数据

```json
{
    "time": 1724867624200,
    "participants": [
        {
            "id": 12345679077,
            "location": {
                "longitude": 113.2456341,
                "latitude": 23.0217575,
                "height": 147.54
            },
            "speed": 6.49
        }
    ]
}
```

#### 制作数据

```bash
cat data/track_Lshape_0828.jsonl | awk '{print $0"\n"$1"100"$2$3($4+0.00001)$5}'

cat data/track_Lshape_0828.jsonl | awk '{printf "%s\n%s100%s%s%.7f%s\n", $0, $1, $2, $3, ($4 - 0.00004), $5}' > data/track_Lshape_0828.dual.jsonl

cat data/track_Lshape_0828.jsonl | awk '{printf "%s\n%s100%s%s%.7f%s\n%s%d%s%.7f%s\n", $0, $1, $2, $3, ($4 - 0.0001), $5, $1, int($2)+1, $3, ($4 +0.0004), $5}' > data/track_Lshape_0828.dual.jsonl
```

### old

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
apt-get install -y default-libmysqlclient-dev


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
