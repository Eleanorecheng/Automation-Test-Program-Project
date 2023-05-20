#! /bin/sh

python3 -m venv env
source env/bin/activate
pip3 install allure-pytest
pip3 install -r requirements.txt
rm -rf ./report
pytest ./tests_web/test_sample.py --alluredir ./report
allure serve report
