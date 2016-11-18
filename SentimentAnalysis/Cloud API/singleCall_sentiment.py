import argparse
from googleapiclient import discovery
import httplib2
import json
from oauth2client.client import GoogleCredentials
import csv
import ntpath

# Credentials environment variable
GOOGLE_APPLICATION_CREDENTIALS = "GOOGLE_APPLICATION_CREDENTIALS"
DISCOVERY_URL = ('https://{api}.googleapis.com/'
                 '$discovery/rest?version={apiVersion}')

def main(calltext_file):
  '''
  cd to \Desktop\Dropbox\CT\GGL\curly-octo-tribble\curly-octo-tribble\SentimentAnalysis\Cloud API
  Before first run, run csvinit.py to initialize csv file.
  
  Then run:
  
  singleCall_sentiment.py FILENAME 
        in command line'''

  http = httplib2.Http()

  credentials = GoogleCredentials.get_application_default().create_scoped(
    ['https://www.googleapis.com/auth/cloud-platform'])
  # credentials = GoogleCredentials.get_application_default()
  http=httplib2.Http()
  credentials.authorize(http)

  service = discovery.build('language', 'v1beta1',
                            http=http, discoveryServiceUrl=DISCOVERY_URL)

  # Open file that was parsed as cmd line argument
  call_text = open(calltext_file, 'r')
  customertext = []

  for line in call_text:
    if line[:9] == 'Customer:':
	    customertext.append(line[9:])
  customertext = ''.join(map(str, customertext))
  
  # Length of text is used to normalize magnitude sentiment measurement
  textlength = len(customertext)
  
  
  # First char of filename is call number, and will be used to store results in csv.
  fname = ntpath.basename(calltext_file)
  callnum = int(fname[0])
  
  # Format of API request:
  service_request = service.documents().analyzeSentiment(
    body={
      'document': {
         'type': 'PLAIN_TEXT',
         'content': customertext,
      }
    })

  # Execute request
  response = service_request.execute()
  polarity = response['documentSentiment']['polarity']
  magnitude = response['documentSentiment']['magnitude']
  sentmeas = 1000*polarity*magnitude/textlength
  
  # Storing results in csv file
  r = csv.reader(open('CallsToProcess/output.csv')) # Here your csv file
  csvrows = [l for l in r]
  csvrows[callnum-1][0] = callnum
  csvrows[callnum-1][1] = polarity
  csvrows[callnum-1][2] = magnitude
  csvrows[callnum-1][3] = sentmeas
  writer = csv.writer(open('CallsToProcess/output.csv', 'wb'))
  writer.writerows(csvrows)
  
  print('Sentiment: polarity of %s with magnitude of %s. Final measurement is %s' % (polarity, magnitude, sentmeas))
  return 0

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument(
    'calltext_file', help='The filename of the call transcript you\'d like to analyze.')
# parser.add_argument("--fname", "-f", type=str, required=True)
  args = parser.parse_args()
  main(args.calltext_file)