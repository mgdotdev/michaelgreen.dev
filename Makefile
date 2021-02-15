start:
	docker-compose up -d

stop:
	docker-compose down
	
reset:
	docker-compose down
	docker-compose build --build-arg CACHEBUST_APP=$(date +%s)
	docker-compose up -d

gdeploy:
	gsutil cp client/ gs://michaelgreendev/
	docker build -f _docker/Dockerfile.api -t gcr.io/michaelgreendev/mgdev-api .
	docker push gcr.io/michaelgreendev/mgdev-api
	gcloud run deploy --image gcr.io/michaelgreendev/mgdev-api --platform managed
	docker build -f _docker/Dockerfile.server -t gcr.io/michaelgreendev/mgdev-server .
	docker push gcr.io/michaelgreendev/mgdev-server
	gcloud run deploy --image gcr.io/michaelgreendev/mgdev-server --platform managed