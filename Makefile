start:
	docker-compose up -d

stop:
	docker-compose down
	
reset:
	docker-compose down
	docker-compose build --build-arg CACHEBUST_APP=$(date +%s)
	docker-compose up -d
