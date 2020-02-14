# awspds-mosaic

Create Cloud Optimized GeoTIFF [mosaics](https://github.com/developmentseed/mosaicjson-spec) from AWS Public datasets.

![landsatlive](https://user-images.githubusercontent.com/10407788/53614981-299ec800-3bb2-11e9-959e-367c973299f8.png)

The repo host all the code for [landsatlive.live](https://landsatlive.live) website and APIs. Most of the code is a custom fork of [developmentseed/cogeo-mosaic-tiler](https://github.com/developmentseed/cogeo-mosaic-tiler).


## Deploy your own

### Create the AWS Lambda package

We first need to create the python lambda package using Docker container.

```bash
$ make package
```

### Deploy to AWS

**Landsat**

This project uses [Serverless](https://serverless.com) to manage deploy on AWS.

```bash
# Install and Configure serverless (https://serverless.com/framework/docs/providers/aws/guide/credentials/)
$ npm install serverless -g 

$ cd services/landsat && sls deploy --region us-east-1 --bucket a-bucket-where-you-store-data --token {OPTIONAL MAPBOX TOKEN}
```
