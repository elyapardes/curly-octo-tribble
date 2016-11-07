import argparse
from googleapiclient import discovery
import httplib2
import json
from oauth2client.client import GoogleCredentials

# Credentials environment variable
GOOGLE_APPLICATION_CREDENTIALS = "GOOGLE_APPLICATION_CREDENTIALS"
DISCOVERY_URL = ('https://{api}.googleapis.com/'
                 '$discovery/rest?version={apiVersion}')

def main(calltext_file):
  '''Run:
	
	tut_example.py tmp.txt 
				in command line'''

  http = httplib2.Http()

  credentials = GoogleCredentials.get_application_default().create_scoped(
    ['https://www.googleapis.com/auth/cloud-platform'])
#  credentials = GoogleCredentials.get_application_default()
  http=httplib2.Http()
  credentials.authorize(http)

  service = discovery.build('language', 'v1beta1',
                            http=http, discoveryServiceUrl=DISCOVERY_URL)

  call_text = open(calltext_file, 'r')
  service_request = service.documents().analyzeSentiment(
    body={
      'document': {
         'type': 'PLAIN_TEXT',
         'content': call_text.read(),
      }
    })

	# Save results into variables polarity and magnitude
  response = service_request.execute()
  polarity = response['documentSentiment']['polarity']
  magnitude = response['documentSentiment']['magnitude']
  print('Sentiment: polarity of %s with magnitude of %s' % (polarity, magnitude))
  return 0

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument(
    'calltext_file', help='The filename of the call transcript you\'d like to analyze.')
  args = parser.parse_args()
  main(args.calltext_file)