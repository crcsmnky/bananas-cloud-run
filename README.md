# Bananas for Cloud Run

This is a simple demo app for use with Cloud Run, Cloud Run on GKE, and Knative. The app uses the Cloud Vision API label detection to annotate uploaded images, and detects whether there are any bananas in the image.

## Setup

- Install the [Google Cloud SDK](https://cloud.google.com/sdk)
- Create a [Google Cloud](https://console.cloud.google.com) project (with billing)
- Enable the following [APIs](https://console.cloud.google.com/apis/library):
  - Cloud Build
  - Container Registry
  - Cloud Run
  - Kubernetes Engine
  - Vision API

```
gcloud services enable \ 
  container.googleapis.com \
  containerregistry.googleapis.com \
  cloudbuild.googleapis.com \
  run.googleapis.com \
  vision.googleapis.com
```

- Then build the `bananas-cloud-run` image using [Cloud Build](https://cloud.google.com/cloud-build/docs/):

```
gcloud builds submit --tag gcr.io/[PROJECT-ID]/bananas-cloud-run
```

## Deploying to Cloud Run

```
gcloud beta run deploy [SERVICE_NAME] \
  --image gcr.io/[PROJECT_ID]/bananas-cloud-run:latest \
  --region [REGION] \
  --set-env-vars PLATFORM="Cloud Run"
```

## Deploying to Cloud Run on GKE

- [Setting up Cloud Run on GKE](https://cloud.google.com/run/docs/gke/setup)
- [Change the GKE default domain for testing](https://cloud.google.com/run/docs/gke/default-domain)
- Create a cluster:

```
gcloud beta container clusters create [CLUSTER_NAME] \
--addons=HorizontalPodAutoscaling,HttpLoadBalancing,Istio,CloudRun \
--machine-type=n1-standard-4 \
--cluster-version=latest --zone=[ZONE] \
--enable-stackdriver-kubernetes --enable-ip-alias \
--scopes cloud-platform
```

- Deploy to Cloud Run on GKE:

```
gcloud beta run deploy [SERVICE_NAME] \
  --image gcr.io/[PROJECT_ID]/bananas-cloud-run:latest \
  --cluster [CLUSTER_NAME] --cluster-location [CLUSTER_LOCATION] \
  --set-env-vars PLATFORM="Cloud Run on GKE"
```

## Deploying to Knative

Coming soon

## Cleanup

Cloud Run:
```
gcloud beta run services delete [SERVICE_NAME] --region [REGION]
```

Cloud Run on GKE:
```
gcloud beta run services delete [SERVICE_NAME] \ 
  --cluster [CLUSTER_NAME] --cluster-location [CLUSTER_LOCATION]
```