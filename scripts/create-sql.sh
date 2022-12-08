#! /usr/bin/env bash

gcloud sql instances create little-talks-production \
  --database-version=POSTGRES_14 \
  --zone=us-central1-a \
  --cpu=1 \
  --memory=3840MiB\
  --root-password=$PS_PASSWORD \
  --storage-type=SSD \
  --storage-size=20GB \
  --backup-start-time=02:00