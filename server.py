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
import ga4gh.schemas.ga4gh.variants_pb2 as v

PORT = 5000
API_SERVER = "api.23andme.com"
BASE_CLIENT_URL = "http://localhost:%s/" % PORT
DEFAULT_REDIRECT_URI = "%soauth" % BASE_CLIENT_URL

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

DEFAULT_SNPS = ["rs12913832"]
DEFAULT_SCOPES = ["names", "basic","email", "genomes"]


client_secret = keys.client_secret

parser = OptionParser(usage="usage: %prog -i CLIENT_ID [options]")
parser.add_option("-s", "--scopes", dest="scopes", action="append", default=[],
				  help="Your requested scopes. Eg: -s basic -s rs12913832")
parser.add_option("-r", "--redirect_uri", dest="redirect_uri", default=DEFAULT_REDIRECT_URI,
				  help="Your clients redirect_uri [%s]" % DEFAULT_REDIRECT_URI)
parser.add_option("-a", "--api_server", dest="api_server", default=API_SERVER,
				  help="Almost always: [api.23andme.com]")
parser.add_option("-p", "--select-profile", dest="select_profile", action="store_true", default=False,
				  help="If present, the auth screen will show a profile select screen")

(options, args) = parser.parse_args()
BASE_API_URL = "https://%s" % options.api_server
API_AUTH_URL = "%s/authorize" % BASE_API_URL
API_TOKEN_URL = "%s/token/" % BASE_API_URL

if options.select_profile:
	API_AUTH_URL += "?select_profile=true"

redirect_uri = options.redirect_uri
client_id = keys.client_id

scopes = options.scopes or DEFAULT_SCOPES

if not client_secret:
	print "Please navigate to your developer dashboard [%s/dev/] to retrieve your client_secret." % BASE_API_URL
	client_secret = getpass.getpass("Please enter your client_secret:")


# GA4GH chromosome value to NC ID
chromeToAccession = {"1":"NC_000001.10", "2":"NC_000002.11", "3":"NC_000003.11", "4":"NC_000004.11", "5":"NC_000005.9", "6":"NC_000006.11", 
					 "7":"NC_000007.13", "8":"NC_000008.10", "9":"NC_000009.11", "10":"NC_000010.10", "11":"NC_000011.9", "12":"NC_000012.11", 
					 "13":"NC_000013.10", "14":"NC_000014.8", "15":"NC_000015.9", "16":"NC_000016.9", "17":"NC_000017.10", "18":"NC_000018.9", 
					 "19":"NC_000019.9", "20":"NC_000020.10", "21":"NC_000021.8", "22":"NC_000022.10", "X":"NC_000023.10", "Y":"NC_000024.9"}

app = flask.Flask(__name__)



### Show index page, begin oauth process
### Go to api callback /oauth
@app.route("/")
def index():
	print("in index")
	print(DEFAULT_REDIRECT_URI)
	ttam_oauth = OAuth2Session(client_id,
							   redirect_uri=redirect_uri,
							   scope=scopes)
	auth_url, state = ttam_oauth.authorization_url(API_AUTH_URL)

	return flask.render_template("index.html", auth_url=auth_url)



### Retrieve access token and complete oauth process
### Retrieve user profile id
### Call ga4gh() to begin parameter entry
@app.route("/oauth")
def oauth():

	print("authenticating...")

	# authentification information
	ttam_oauth = OAuth2Session(client_id,
							   redirect_uri=redirect_uri)
	token_dict = ttam_oauth.fetch_token(API_TOKEN_URL,
										client_secret=client_secret,
										authorization_response=request.url)

	access_token = token_dict["access_token"]

	headers = {"Authorization": "Bearer %s" % access_token}
	account_response = requests.get("https://api.23andme.com/3/account/",headers=headers, verify=False)
	account_response_json = account_response.json()
	profile_id = account_response_json["data"][0]["profiles"][0]["id"]

	# store headers and profile_id in session so that we can use it in the flask portion of the application
	session["headers"] = headers
	session["profile_id"] = profile_id

	# after oauth has completed, begin actual request
	return(ga4gh())




### Prompt user for search_variants_request parameters using ga4gh.html
def ga4gh():
	print("input data...")
	submit_ga4gh = "http://localhost:5000/variants/search"
	return flask.render_template("user_input.html", auth_url=submit_ga4gh)



### Post users entered parameters
### Store parameters in protocol buffer
### Send off protocol buffer to translate()
@app.route("/variants/search", methods=["POST"])
def search_variants():

	print("converting request to GA4GH")
	start_pos = request.form["start_pos"]
	end_pos = request.form["end_pos"]
	chrome = request.form["chrome"]
	session["chrome"] = chrome

	aRequest = {"start": start_pos, "end": end_pos, "referenceName": chrome, "variantSetId": "abc"}

	# using ga4gh protocol buffer, stuff parameters into SearchVariantsRequest
	proto_request = p.fromJson(json.dumps(aRequest), p.SearchVariantsRequest)

	return(translate(proto_request))




### Convert GA4GH request into 23andMe request
### Send off converted GA4GH -> 23andMe request
@app.route("/translate")
def translate(ga4gh_request):

	# using ga4gh protocol buffer, stuff SearchVariantsRequest parameters into 23andMe request
	print("creating 23andMe request from GA4GH protobuf")
	profile_id = session.get("profile_id")
	ttam_request = "https://api.23andme.com/3/profile/"+profile_id+"/variant/?accession_id="+chromeToAccession[ga4gh_request.reference_name]+"&start="+str(ga4gh_request.start)+"&end="+str(ga4gh_request.end)

	headers = session.get("headers")

	print("sending request to 23andMe")
	profile_variant_response = requests.get(ttam_request,headers=headers, verify=False)
	profile_variant_response_json = profile_variant_response.json()


	print("converting response to GA4GH SearchVariantResponse")
	ttam_response = profile_variant_response_json["data"]
	# using the GA4GH schemas, stuff in 23andMe response into SearchVariantsResponse parameters
	# have to return like this ("data":[]) because flask doesn't allow otherwise for security purposes
	ga4gh_response = {"data":[]}
	for i in range(0,len(ttam_response),2):
		# had to switch from p.Variant to something else due to json serialization errors. this took hours of head banging :(

		response = {"reference_name":session["chrome"].encode('ascii'), "alternate_bases":[ttam_response[i+1]["allele"].encode('ascii')], "reference_bases":ttam_response[i]["allele"].encode('ascii'), "start":ttam_response[i]["start"], "end":ttam_response[i]["end"], "variant_set_id":"1"}

		proto_response = p.fromJson(json.dumps(response), v.Variant)
		ga4gh_response["data"].append(response)
	
	if profile_variant_response.status_code == 200:
		# ga4gh_response is ths JSON we want, push it to results.html so the user can see their data
		return flask.render_template("results.html", ga4gh_response=ga4gh_response)

	else:
		profile_variant_response.raise_for_status()


app.secret_key = keys.sessions_key

if __name__ == "__main__":
	print "A local client for GA4GHandMe is now initialized."
	app.run(debug=False, port=PORT)