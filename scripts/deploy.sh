#! /usr/bin/env bash

gcloud functions deploy little-talks \
  --trigger-http \
  --runtime python39 \
  --entry-point=send_messages \
  --memory=512MB \
  --timeout=300s \
  --env-vars-file=production.env.yml \
