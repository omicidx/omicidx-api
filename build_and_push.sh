#!/bin/bash
docker build --build-arg SSH_PRIVATE_KEY="$( cat ~/.ssh/id_rsa )" -t seandavi/omidicx-fastapi .
docker tag seandavi/omidicx-fastapi gcr.io/isb-cgc-01-0006/omicidx-fastapi
docker push gcr.io/isb-cgc-01-0006/omicidx-fastapi
kubectl get pods | grep omicidx-fastapi | awk '{print $1}' | xargs kubectl delete pod
