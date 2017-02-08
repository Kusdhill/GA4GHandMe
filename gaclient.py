import ga4gh.client as client
c = client.HttpClient("http://1kgenomes.ga4gh.org")

dataset = c.search_datasets().next()

for functionalVariantSet in c.search_variant_sets(dataset.id):
	if functionalVariantSet.name == "functional-annotation":
		functionalAnnotation = functionalVariantSet

functionalAnnotationSet = c.search_variant_annotation_sets(variant_set_id=functionalAnnotation.id).next()



searchedVarAnns = c.search_variant_annotations(variant_annotation_set_id=functionalAnnotationSet.id,
 start='43044295', end='43170245', reference_name='17', effects='SO:0001630')


myRequest = '''c.search_variant_annotations(variant_annotation_set_id=functionalAnnotationSet.id, start='43044295', end='43170245', reference_name='17', effects='SO:0001630')'''