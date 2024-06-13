ps axuf | grep appuav.asgi:appuav | grep 9701 | awk '{print $2}' | xargs -n 1 kill -9  #-TERM
echo "killed main"
sleep 1

pids=$(ps axuf | grep uavadmin2 | grep -v grep | grep -v celery | awk '{print $2}')
echo $pids
for pid in $pids; do
    kill -9 "$pid"
done
echo "killed sub"
sleep 1

nohup python -m uvicorn appuav.asgi:appuav --port 9701 --host 0.0.0.0 --workers 2  >>logs/server.log 2>&1 &
