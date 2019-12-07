#!/bin/bash
docker build -t seandavi/omidicx-fastapi .
docker tag seandavi/omidicx-fastapi gcr.io/isb-cgc-01-0006/omicidx-fastapi:latest
docker tag seandavi/omidicx-fastapi gcr.io/isb-cgc-01-0006/omicidx-fastapi:`git rev-parse HEAD`
docker push gcr.io/isb-cgc-01-0006/omicidx-fastapi:latest
docker push gcr.io/isb-cgc-01-0006/omicidx-fastapi:`git rev-parse HEAD`
kubectl get pods | grep omicidx-fastapi | awk '{print $1}' | xargs kubectl delete pod
