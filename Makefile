postgres:
	docker run --name postgres_contentcritic_container -p 8005:5432 \
	-e POSTGRES_USER=postgres \
	-e POSTGRES_PASSWORD=postgres \
	-v postgres_data:/var/lib/postgresql/data \
	--rm \
	-d postgres:latest

redis:
	docker run --name redis_contentcritic_container -p 8006:6379 \
	-v redis_data:/var/lib/redis/data \
	--rm \
	-d redis:latest

createdb:
	docker exec -it postgres_contentcritic_container createdb --username=postgres --owner=postgres content

dropdb:
	docker exec -it postgres_contentcritic_container dropdb --username_
