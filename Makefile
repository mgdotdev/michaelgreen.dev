gdeploy:
	gsutil cp -r server/client/static/ gs://michaelgreendev/server/client/
	gsutil cp -r blog/client/static/ gs://michaelgreendev/blog/client/
	docker build -f _docker/Dockerfile.api -t gcr.io/michaelgreendev/mgdev-api .
	docker push gcr.io/michaelgreendev/mgdev-api
	gcloud run deploy mgdev-api --image gcr.io/michaelgreendev/mgdev-api --platform managed --region us-west1
	docker build -f _docker/Dockerfile.server -t gcr.io/michaelgreendev/mgdev-server .
	docker push gcr.io/michaelgreendev/mgdev-server
	gcloud run deploy mgdev-server --image gcr.io/michaelgreendev/mgdev-server --platform managed --region us-west1
	docker build -f _docker/Dockerfile.blog -t gcr.io/michaelgreendev/mgdev-blog .
	docker push gcr.io/michaelgreendev/mgdev-blog
	gcloud run deploy mgdev-blog --image gcr.io/michaelgreendev/mgdev-blog --platform managed --region us-west1
