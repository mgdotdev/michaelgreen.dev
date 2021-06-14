start:
	docker-compose up -d

stop:
	docker-compose down

base:
	docker build -t michaelgreendev_server -f _docker/Dockerfile.server --build-arg CACHEBUST_APP=$(date +%s) .
	docker build -t michaelgreendev_api -f _docker/Dockerfile.api --build-arg CACHEBUST_APP=$(date +%s) .
	docker build -t michaelgreendev_blog -f _docker/Dockerfile.blog --build-arg CACHEBUST_APP=$(date +%s) .

dev:
	docker build -t michaelgreendev_server_test -f _docker/Dockerfile.test.server --build-arg CACHEBUST_APP=$(date +%s) .
	docker build -t michaelgreendev_api_test -f _docker/Dockerfile.test.api --build-arg CACHEBUST_APP=$(date +%s) .
	docker build -t michaelgreendev_blog_test -f _docker/Dockerfile.test.blog --build-arg CACHEBUST_APP=$(date +%s) . 

reset:
	docker-compose down
	docker build -t michaelgreendev_server -f _docker/Dockerfile.server --build-arg CACHEBUST_APP=$(date +%s) .
	docker build -t michaelgreendev_api -f _docker/Dockerfile.api --build-arg CACHEBUST_APP=$(date +%s) .
	docker build -t michaelgreendev_blog -f _docker/Dockerfile.blog --build-arg CACHEBUST_APP=$(date +%s) .
	docker-compose build --build-arg CACHEBUST_APP=$(date +%s)
	docker-compose up -d

reset-blog:
	docker kill michaelgreendev_blog_1
	docker rm -f michaelgreendev_blog_1
	docker build -t michaelgreendev_blog -f _docker/Dockerfile.blog --build-arg CACHEBUST_APP=$(date +%s) .
	docker build -t michaelgreendev_blog -f _docker/Dockerfile.test.blog --build-arg CACHEBUST_APP=$(date +%s) .
	docker run -d -p "8081:8080" --name michaelgreendev_blog_1 michaelgreendev_blog

blog-pdb:
	# docker kill michaelgreendev_blog_1
	docker rm -f michaelgreendev_blog_1
	docker build -t michaelgreendev_blog -f _docker/Dockerfile.blog --build-arg CACHEBUST_APP=$(date +%s) .
	docker build -t michaelgreendev_blog -f _docker/Dockerfile.test.blog --build-arg CACHEBUST_APP=$(date +%s) .
	docker run -it -p "8081:8080" --name michaelgreendev_blog_1 michaelgreendev_blog

gdeploy:
	gsutil cp -r server/client/static/ gs://michaelgreendev/server/client/
	gsutil cp -r blog/client/static/ gs://michaelgreendev/blog/client/
	docker build -f _docker/Dockerfile.api -t gcr.io/michaelgreendev/mgdev-api .
	docker push gcr.io/michaelgreendev/mgdev-api
	gcloud run deploy --image gcr.io/michaelgreendev/mgdev-api --platform managed
	docker build -f _docker/Dockerfile.server -t gcr.io/michaelgreendev/mgdev-server .
	docker push gcr.io/michaelgreendev/mgdev-server
	gcloud run deploy --image gcr.io/michaelgreendev/mgdev-server --platform managed
	docker build -f _docker/Dockerfile.blog -t gcr.io/michaelgreendev/mgdev-blog .
	docker push gcr.io/michaelgreendev/mgdev-blog
	gcloud run deploy --image gcr.io/michaelgreendev/mgdev-blog --platform managed