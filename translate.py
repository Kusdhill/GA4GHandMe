from gaclient import myRequest

print(str(myRequest[2:len(myRequest)]))


if(str(myRequest[2:29])=='search_variant_annotations('):
	requestBase = 'abc'
	start = '123'
	end = '456'


print(requestBase+'('+start+end+')')