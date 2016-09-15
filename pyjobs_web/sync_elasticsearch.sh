#!/usr/bin/env bash

# CRON Frequency recommendation 30 * * * * *
# Usage: this_script.sh /path/to/pyjobs /var/log/pyjobs /path/to/production.ini

SOURCE_DIR="$1"
LOG_DIR="$2"
CONFIG="$3"

echo SOURCE_DIR: ${SOURCE_DIR}, LOG_DIR: ${LOG_DIR}, CONFIG: ${CONFIG}

cd ${SOURCE_DIR} && . ./venv2.7/bin/activate
cd pyjobs_web
# Job offers synchronization
gearbox populate-elasticsearch -j -c "$CONFIG" &>> "$LOG_DIR"/sync_elasticsearch_jobs.log
echo ALGOO-MONITORABLE-CRON __ $(date +\"%Y-%m-%dT%H:%M:%S\") __  >> "$LOG_DIR"/sync_elasticsearch_jobs.log
# Companies synchronization
gearbox populate-elasticsearch -co -c "$CONFIG" &>> "$LOG_DIR"/sync_elasticsearch_companies.log
echo ALGOO-MONITORABLE-CRON __ $(date +\"%Y-%m-%dT%H:%M:%S\") __  >> "$LOG_DIR"/sync_elasticsearch_companies.log
