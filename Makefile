.PHONY: build run run-prod clean

build:
	@sudo docker-compose build

run:
	@sudo docker-compose build
	@sudo docker-compose up

run-prod:
	@sudo docker-compose -f docker-compose.yaml -f docker-compose.prod.yaml up -d

clean:
	@sudo docker-compose down