#!/usr/bin/env bash

# CRON Frequency recommendation * 1 * * * *
# Usage: this_script.sh /path/to/pyjobs /var/log/pyjobs /path/to/production.ini

SOURCE_DIR="$1"
LOG_DIR="$2"
CONFIG="$3"

echo SOURCE_DIR: ${SOURCE_DIR}, LOG_DIR: ${LOG_DIR}, CONFIG: ${CONFIG}

cd ${SOURCE_DIR} && . ./venv2.7/bin/activate
cd pyjobs_web
# Run the Github bot
gearbox bots github -c "$CONFIG" >> "$LOG_DIR"/github_bot.log 2>1&
echo ALGOO-MONITORABLE-CRON __ $(date +\"%Y-%m-%dT%H:%M:%S\") __  >> "$LOG_DIR"/elasticsearch_sync_jobs.log
# Run the Twitter bot - Maximum 250 Tweets
gearbox bots twitter -n 250 -c twitter_credentials.json -c "$CONFIG" >> "$LOG_DIR"/twitter_bot.log 2>1&
echo ALGOO-MONITORABLE-CRON __ $(date +\"%Y-%m-%dT%H:%M:%S\") __  >> "$LOG_DIR"/elasticsearch_sync_companies.log
