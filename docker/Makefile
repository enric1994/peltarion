run:
	@docker-compose up -d --build
dev:
	@docker exec -it peltarion bash
build:
	@docker-compose build
down:
	@docker-compose down -v
status:
	@docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
logs:
	@docker logs peltarion -f