#!/usr/bin/env bash


echo "***************************************************************************************"
echo ""
echo "This bot performs some automation with DataHub"
echo ""
echo "Basically it does:"
echo "- Registers new Data Quality Suites in DataHub"
echo "- Prevents a PR of removing Data Quality Suites already registered in DataHub"
echo ""
echo "Please, contact Yotta team in case of any issue because of this in slack #yotta-team"
echo ""
echo "***************************************************************************************"

if [ "${TRAVIS_EVENT_TYPE}" == "pull_request" -o "${TRAVIS_BRANCH}" != master ]
then
    python bin/dqs-sync.py -m review -v
else
    python bin/dqs-sync.py -m sync -v
fi
