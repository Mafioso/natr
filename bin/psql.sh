#!/bin/bash
cur_dir=$PWD

(PROFILE=${PROFILE} docker-compose -f ${cur_dir}/docker-compose.yml -f ${cur_dir}/docker-compose.${PROFILE}.yml run --rm db sh -c 'exec psql -h "$DB_PORT_5432_TCP_ADDR" -p 5432  -U mars -d natr_dev')