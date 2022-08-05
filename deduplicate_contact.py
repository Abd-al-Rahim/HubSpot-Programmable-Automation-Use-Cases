import os
import requests
from hubspot import HubSpot
from hubspot.crm.contacts import PublicObjectSearchRequest, ApiException

dedupeProperty = 'phone'

def main(event):
    hubspot = HubSpot(api_key=os.getenv('HAPIKEY'))

    contactResult = hubspot.crm.contacts.basic_api.get_by_id(
        event.get('object').get('objectId'), properties=[dedupeProperty])
    dedupePropValue = contactResult.properties.get(dedupeProperty)

    print(f'looking for duplicates based on {dedupeProperty} = {dedupePropValue}')

    public_object_search_request = PublicObjectSearchRequest(
        filter_groups=[
            {
                "filters": [
                    {
                        "value": dedupePropValue,
                        "propertyName": dedupeProperty,
                        "operator": "EQ",
                    }
                ]
            }
        ])

    try:
        searchResults = hubspot.crm.contacts.search_api.do_search(public_object_search_request=public_object_search_request)
        #print(searchResults)
    except ApiException as e:
        print("Exception when calling search_api->do_search: %s\n" % e)
        
    idsToMerge = list(filter(lambda vid: int(vid) != event.get('object').get('objectId'),
                        map(lambda object: object.id, searchResults.results)))
    
    if len(idsToMerge) == 0:
        print("No matching contact, nothing to merge")
        return
    elif len(idsToMerge) > 1:
      	print(f"Found multiple potential contact IDs {idsToMerge.join(', ')} to merge")
      	raise ValueError("Ambiguous merge, more than one matching contact")
              
    idToMerge = idsToMerge[0]
    print(f"Merging enrolled contact id={event.get('object').get('objectId')} into contact id={idToMerge}")

    header = "Content-Type: application/json"
    body = {
        "vidToMerge": event.get('object').get('objectId')
        }
    #Unable to POST request [401 response] or maybe I am doing something wrong
    mergeResult = requests.post(
        url = 'https://api.hubapi.com/contacts/v1/contact/merge-vids/{idToMerge}', data=body)
    print("Contacts merged!")
