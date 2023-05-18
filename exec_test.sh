#! /bin/sh

# python3 -m venv env
# source env/bin/activate
cd ./Automation-Test-Program-Batch2-Project/tests_web
pytest test_sample.py --alluredir ./report
allure serve report
