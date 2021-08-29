.PHONY: requirements deploy
.ONESHELL:

venv:
	python3 -m venv venv

requirements:
	pip install -r requirements.txt

deploy:
	sls deploy

start-proxy:
	sls invoke --function launch_proxy_ec2

stop-proxy:
	sls invoke --function terminate_proxy_ec2
