from gaclient import myRequest

print(myRequest[2:len(myRequest)])


if(myRequest[2:29]=='search_variant_annotations('):
	requestBase = 'abc'
	start = '123'
	end = '456'


print(requestBase+'('+start+end+')')