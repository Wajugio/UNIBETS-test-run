# UNIBETS-test-run
Need google cloud shell terminal 

Step #1:
Clone repository into cloud shell

Step #2: 
In terminal run gcloud config set project unibets-457019

Step #3:
Enable Cloud APIs ----> gcloud services enable run cloudbuild.googleapis.com artifactregistry.googleapis.com

Step #4:
type ls to make sure you're in UNIBETS file
run gcloud builds submit --tag gcr.io/$(gcloud config get-value project)/unibets
this will package everything into docker file

Step #5:
Last step is to deploy to cloud run copy and paste below
gcloud run deploy unibets \
  --image gcr.io/$(gcloud config get-value project)/unibets \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
  this will give you a live https link.
