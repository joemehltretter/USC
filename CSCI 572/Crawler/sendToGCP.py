import os
import google.cloud.storage

def main():
  path = input('Enter path to credentials: ')
  client = google.cloud.storage.Client.from_service_account_json(path)
  bucket = client.get_bucket('tcrawler')
  pathToFiles = '/home/mehltret/Desktop/USC/CSCI 572/Crawler/files'
  for fileName in os.listdir(pathToFiles):
    pathToFile = pathToFiles + '/' + fileName
    blob = bucket.blob(os.path.basename(pathToFile))
    blob.upload_from_filename(pathToFile)
    print("{fileN} uploaded to {bucket}".format(fileN = fileName, bucket = bucket))

if __name__ == "__main__":
  main()

