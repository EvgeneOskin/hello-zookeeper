.PHONY: build
build:
	docker-compose build

.PHONY: up
up:
	docker-compose up -d app1 app2 app3
