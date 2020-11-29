.PHONY: build run run-prod clean

build:
	@sudo docker-compose build

run:
	@sudo docker-compose build
	@sudo docker-compose up

run-prod:
	@docker-compose --context discord build
	@docker-compose --context discord -f docker-compose.yaml -f docker-compose.prod.yaml up -d

clean:
	@sudo docker-compose down

clean-prod:
	@docker-compose --context discord down