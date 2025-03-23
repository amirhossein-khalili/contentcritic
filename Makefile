postgres:
	docker run --name postgres_content -p 8005:5432 \
	-e POSTGRES_USER=postgres \
	-e POSTGRES_PASSWORD=postgres \
	-v postgres_data:/var/lib/postgresql/data \
	--rm \
	-d postgres:latest

redis:
	docker run --name redis_content -p 8006:6379 \
	-v redis_data:/var/lib/redis/data \
	--rm \
	-d redis:latest

createdb:
	docker exec -it postgres_content createdb --username=postgres --owner=postgres content

dropdb:
	docker exec -it postgres_content dropdb --username_
