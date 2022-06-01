.PHONY: requirements deploy
.ONESHELL:

help:
	@echo "start-proxy     to start the proxy instance"
	@echo "stop-proxy      to terminate the proxy instance"
	@echo "check-proxy     to get the public IP of the proxy instance, if running"
	@echo "check-instances to list the status of all EC2s in the account"

venv:
	python3 -m venv venv

requirements:
	pip install -r requirements.txt

deploy: export AWS_PROFILE := personal-admin
deploy:
	sls deploy

start-proxy: export AWS_PROFILE := personal-admin
start-proxy:
	sls invoke --function launch_proxy_ec2

stop-proxy: export AWS_PROFILE := personal-admin
stop-proxy:
	sls invoke --function terminate_proxy_ec2

check-proxy: export AWS_PROFILE := personal-admin
check-proxy:
	sls invoke --function check_proxy_ec2

check-proxy: export AWS_PROFILE := personal-admin
check-instances:
	aws ec2 describe-instances | jq ' .Reservations[] .Instances[] .State '

check-public-ip:
	curl checkip.amazonaws.com
check-public-ip-proxy:
	ALL_PROXY=socks5://localhost:4444 curl checkip.amazonaws.com
