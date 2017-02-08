import ga4gh.client as client
c = client.HttpClient("http://1kgenomes.ga4gh.org")

dataset = c.search_datasets().next()

for variant_set in c.search_variant_sets(dataset_id=dataset.id):
    if variant_set.name == "phase3-release":
        var_set_id = variant_set
    print("Variant Set: "+variant_set.name)
    print("id: "+variant_set.id)
    print("dataset_id: "+variant_set.dataset_id)
    print("reference_set_id: "+variant_set.reference_set_id)


variant_set = c.get_variant_set(variant_set_id=var_set_id.id)
print("name: "+variant_set.name)
print("dataset_id: "+variant_set.dataset_id)
print("reference_set_id: "+variant_set.reference_set_id)
for metadata in variant_set.metadata[0:3]:
    print(metadata)


myRequest = '''c.search_variants(variant_set_id=var_set_id.id, reference_name="1", start=10176, end= 40176)'''
counter = 0

for variant in c.search_variants(variant_set_id=var_set_id.id, reference_name="1", start=10176, end= 40176):
    if counter > 5:
        break
    counter += 1
    print ("Variant id: "+variant.id[0:10])
    print ("Variant Set Id: "+variant.variant_set_id)
    print ("Names: "+variant.names)
    print ("Reference Chromosome: "+variant.reference_name)
    print ("Start: , End: "+variant.start, variant.end)
    print ("Reference Bases: "+variant.reference_bases)
    print ("Alternate Bases: "+variant.alternate_bases)

