#!/bin/bash

if [[ $1 == celery ]]
then
	celery --app=src.tasks.celery_config:celery_app worker -l INFO
elif [[ $1 == flower ]]
then
	celery --app=src.tasks.celery_config:celery_app flower
fi