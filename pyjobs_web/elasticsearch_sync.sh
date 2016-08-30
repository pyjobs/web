#!/usr/bin/env bash

# CRON Frequency recommendation 30 * * * * *
# Usage: this_script.sh /path/to/pyjobs /var/log/pyjobs /path/to/production.ini

SOURCE_DIR="$1"
LOG_DIR="$2"
CONFIG="$3"

echo SOURCE_DIR: ${SOURCE_DIR}, LOG_DIR: ${LOG_DIR}, CONFIG: ${CONFIG}

cd ${SOURCE_DIR} && . ./venv2.7/bin/activate
# Job offers synchronization
gearbox -c "$CONFIG" populate-es -j >> "$LOG_DIR"/elasticsearch_sync_jobs.log
echo ALGOO-MONITORABLE-CRON __ $(date +\"%Y-%m-%dT%H:%M:%S\") __  >> "$LOG_DIR"/elasticsearch_sync_jobs.log
# Companies synchronization
gearbox -c "$CONFIG" populate-es -co >> "$LOG_DIR"/elasticsearch_sync_companies.log
echo ALGOO-MONITORABLE-CRON __ $(date +\"%Y-%m-%dT%H:%M:%S\") __  >> "$LOG_DIR"/elasticsearch_sync_companies.log
