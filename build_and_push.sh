#!/bin/bash
REVISION=`git rev-parse HEAD`
docker build -t seandavi/omidicx-fastapi .
docker tag seandavi/omidicx-fastapi gcr.io/isb-cgc-01-0006/omicidx-fastapi:latest
docker tag seandavi/omidicx-fastapi gcr.io/isb-cgc-01-0006/omicidx-fastapi:$REVISION
docker push gcr.io/isb-cgc-01-0006/omicidx-fastapi:latest
docker push gcr.io/isb-cgc-01-0006/omicidx-fastapi:$REVISION
#kubectl get pods | grep omicidx-fastapi | awk '{print $1}' | xargs kubectl delete pod
gcloud run deploy omicidx-fastapi --image gcr.io/isb-cgc-01-0006/omicidx-fastapi:$REVISION

