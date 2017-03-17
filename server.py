#!/usr/bin/python

import getpass
import requests
import flask
import json
from flask import request
from flask import session
import os
from optparse import OptionParser
from requests_oauthlib import OAuth2Session
import keys
from ga4gh.schemas import protocol as p

PORT = 5000
API_SERVER = 'api.23andme.com'
BASE_CLIENT_URL = 'http://localhost:%s/' % PORT
DEFAULT_REDIRECT_URI = '%soauth' % BASE_CLIENT_URL

# so we don't get errors if the redirect uri is not https
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = '1'

#
# you can pass in more scopes through the command line, or change these
#
DEFAULT_SNPS = ['rs12913832']
DEFAULT_SCOPES = ['names', 'basic','email', 'genomes'] #+DEFAULT_SNPS#

#
# the command line will ask for a client_secret if you choose to not hardcode the app's client_secret here
#
client_secret = keys.client_secret

parser = OptionParser(usage="usage: %prog -i CLIENT_ID [options]")
parser.add_option('-s', '--scopes', dest='scopes', action='append', default=[],
				  help='Your requested scopes. Eg: -s basic -s rs12913832')
parser.add_option("-r", "--redirect_uri", dest="redirect_uri", default=DEFAULT_REDIRECT_URI,
				  help="Your client's redirect_uri [%s]" % DEFAULT_REDIRECT_URI)
parser.add_option("-a", "--api_server", dest="api_server", default=API_SERVER,
				  help="Almost always: [api.23andme.com]")
parser.add_option("-p", "--select-profile", dest='select_profile', action='store_true', default=False,
				  help='If present, the auth screen will show a profile select screen')

(options, args) = parser.parse_args()
BASE_API_URL = "https://%s" % options.api_server
API_AUTH_URL = '%s/authorize' % BASE_API_URL
API_TOKEN_URL = '%s/token/' % BASE_API_URL

if options.select_profile:
	API_AUTH_URL += '?select_profile=true'

redirect_uri = options.redirect_uri
client_id = keys.client_id

scopes = options.scopes or DEFAULT_SCOPES

if not client_secret:
	print "Please navigate to your developer dashboard [%s/dev/] to retrieve your client_secret." % BASE_API_URL
	client_secret = getpass.getpass("Please enter your client_secret:")


# GA4GH chromosome value to NC ID
chromeToAccession = {'1':'NC_000001.10', '2':'NC_000002.11', '3':'NC_000003.11', '4':'NC_000004.11', '5':'NC_000005.9', '6':'NC_000006.11', 
					 '7':'NC_000007.13', '8':'NC_000008.10', '9':'NC_000009.11', '10':'NC_000010.10', '11':'NC_000011.9', '12':'NC_000012.11', 
					 '13':'NC_000013.10', '14':'NC_000014.8', '15':'NC_000015.9', '16':'NC_000016.9', '17':'NC_000017.10', '18':'NC_000018.9', 
					 '19':'NC_000019.9', '20':'NC_000020.10', '21':'NC_000021.8', '22':'NC_000022.10', 'X':'NC_000023.10', 'Y':'NC_000024.9'}

app = flask.Flask(__name__)



### Show index page, begin oauth process
### Go to api callback /oauth
@app.route('/')
def index():
	print("\nIn index")
	print(DEFAULT_REDIRECT_URI)
	ttam_oauth = OAuth2Session(client_id,
							   redirect_uri=redirect_uri,
							   scope=scopes)
	auth_url, state = ttam_oauth.authorization_url(API_AUTH_URL)

	print("redirect= "+redirect_uri)
	print("api auth url= "+API_AUTH_URL)
	print("auth url= "+auth_url)
	return flask.render_template('index.html', auth_url=auth_url)



### Retrieve access token and complete oauth process
### Retrieve user profile id
### Call ga4gh() to begin parameter entry
@app.route('/oauth')
def oauth():

	print("\nin oauth")
	print(redirect_uri)
	print(request.url)

	#
	# now we hit the /token endpoint to get the access_token
	#
	ttam_oauth = OAuth2Session(client_id,
							   redirect_uri=redirect_uri)
	token_dict = ttam_oauth.fetch_token(API_TOKEN_URL,
										client_secret=client_secret,
										authorization_response=request.url)

	#
	# the response token_dict is of the form
	# {
	#     'token_type': 'bearer',
	#     'refresh_token': '7cb92495fe515f0bfe94775e2b06b46b',
	#     'access_token': 'ad7ace51ad19732b3f9ef778dc766fce',
	#     'scope': ['rs12913832', 'names', 'basic'],
	#     'expires_in': 86400, 'expires_at': 1475283697.571757
	# }
	#

	print(token_dict)
	access_token = token_dict['access_token']

	headers = {'Authorization': 'Bearer %s' % access_token}
	account_response = requests.get('https://api.23andme.com/3/account/',headers=headers, verify=False)
	account_response_json = account_response.json()
	profile_id = account_response_json['data'][0]['profiles'][0]['id']

	session['headers'] = headers
	session['profile_id'] = profile_id

	return(ga4gh())




### Prompt user for search_variants_request parameters using ga4gh.html
def ga4gh():
	print("\nin ga4gh")
	submit_ga4gh = "http://localhost:5000/variants/search"
	return flask.render_template('ga4gh.html', auth_url=submit_ga4gh)



### Post users entered parameters
### Store parameters in protocol buffer
### Send off protocol buffer to translate()
@app.route('/variants/search', methods=['POST'])
def search_variants():
	print("\nin search_variants")

	#aRequest = flask.request.get_json(force=True)
	start_pos = request.form['start_pos']
	end_pos = request.form['end_pos']
	chrome = request.form['chrome']

	aRequest = {"start": start_pos, "end": end_pos, "referenceName": chrome, "variantSetId": "abc"}


	print(aRequest)
	proto_request = p.fromJson(json.dumps(aRequest), p.SearchVariantsRequest)
	
	return(translate_request(proto_request))




### Convert ga4gh request into 23andMe request
### Send off converted ga4gh -> 23andMe request
@app.route('/translate/request')
def translate_request(ga4gh_request):
	print("\nin translate")

	print("translation process")

	print(ga4gh_request)

	profile_id = session.get('profile_id')
	#chromeToAccession[ga4gh_request.reference_name]
	ttam_request = 'https://api.23andme.com/3/profile/'+profile_id+'/variant/?accession_id='+'NC_012920.1'+'&start='+str(ga4gh_request.start)+'&end='+str(ga4gh_request.end)

	print(ttam_request)

	# make a 23andMe request template
	# oauth
	# fill in the 23andMe template
	# do request

	# https://api.23andme.com/3/profile/'+profile_id+'/variant/?accession_id=NC_012920.1


	headers = session.get('headers')

	print('sending request')
	profile_variant_response = requests.get(ttam_request,headers=headers, verify=False)
	profile_variant_response_json = profile_variant_response.json()

	if profile_variant_response.status_code == 200:
		return flask.jsonify(profile_variant_response_json)
	else:
		# print 'response text = ', genotype_response.text
		profile_variant_response.raise_for_status()

	#return(request(ttam_request))
	return(flask.jsonify({}))





app.secret_key = keys.sessions_key

if __name__ == '__main__':
	print "A local client for the Personal Genome API is now initialized."
	app.run(debug=True, port=PORT)