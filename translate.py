import ga4gh.schemas.ga4gh.variant_service_pb2 as v
import lol_file as gc

myRequest = gc.myRequest

# Initialize 23andMe parameters
base_api = 'https://api.23andme.com/3/profile/'
profile_id = ""
accession_id = ""
start = ""
end = ""

# Convert GA4GH chromosome to NC ID
accessionToChrome = {'1':'NC_000001.10'}

# Sample GA4GH request
# '''c.search_variants(variant_set_id=var_set_id.id, reference_name="1", start=10176, end=40176)'''


twRequest = v.SearchVariantsRequest(variant_set_id="abc", reference_name="1", start=123, end=456)

# Fill in 23andMe parameters
accession_id = accessionToChrome[twRequest.reference_name]
start = twRequest.start
end = twRequest.end

print(twRequest)

# Sample 23andMe request
# "https://api.23andme.com/3/profile/'+profile_id+'/variant/?accession_id=NC_012920.1"


'''
accessionToChrome = {'1':'NC_000001.10', '2':'NC_000002.11', '3':'NC_000003.11', '4':'NC_000004.11', '5':'NC_000005.9', '6':'NC_000006.11', 
					 '7':'NC_000007.13', '8':'NC_000008.10', '9':'NC_000009.11', '10':'NC_000010.10', '11':'NC_000011.9', '12':'NC_000012.11', 
					 '13':'NC_000013.10', '14':'NC_000014.8', '15':'NC_000015.9', '16':'NC_000016.9', '17':'NC_000017.10', '18':'NC_000018.9', 
					 '19':'NC_000019.9', '20':'NC_000020.10', '21':'NC_000021.8', '22':'NC_000022.10', 'X':'NC_000023.10', 'Y':'NC_000024.9'}
'''