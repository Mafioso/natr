#!/bin/bash
cur_dir=$PWD

(PROFILE=${PROFILE} docker-compose -f ${cur_dir}/docker-compose.yml -f ${cur_dir}/docker-compose.${PROFILE}.yml up -d)