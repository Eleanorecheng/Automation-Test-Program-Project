#! /bin/sh

python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
# rm -rf ./allure-results
pytest ./tests_web/test_sample.py --alluredir ./allure-results
# allure serve ./allure-report
