
SHELL = /bin/bash

all: package deploy

package:
	docker build --tag awspds-mosaic:latest .
	docker run --name awspds-mosaic --volume $(shell pwd)/:/local -itd awspds-mosaic:latest bash
	docker exec -it awspds-mosaic bash '/local/bin/package.sh'
	docker stop awspds-mosaic
	docker rm awspds-mosaic

STAGENAME=production
BUCKET=MYBUCKET
MAPBOX_TOKEN=pk.....
deploy:
	cd services/landsat && sls deploy --stage ${STAGENAME} --bucket ${BUCKET} --token ${MAPBOX_TOKEN}

