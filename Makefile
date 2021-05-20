.PHONY: requirements deploy

requirements:
	pip install -r requirements.txt


deploy:
	sls deploy
