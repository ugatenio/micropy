.PHONY: build-rabbit
build-rabbit:
	docker run -d --hostname rabbit --name rabbit -p 5672:5672 -e RABBITMQ_DEFAULT_USER=admin -e RABBITMQ_DEFAULT_PASS=admin rabbitmq:3
	docker run -d --hostname rabbitui --name rabbitui -p 15672:15672 rabbitmq:3-management

.PHONY: destroy-rabbit
destroy-rabbit:
	docker rm -f rabbit rabbitui || true
