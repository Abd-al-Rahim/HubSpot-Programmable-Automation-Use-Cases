import os
import requests
from hubspot import HubSpot
from hubspot.crm.deals import ApiException

def main(event):
    hubspot = HubSpot(api_key=os.getenv('HAPIKEY'))

    results = hubspot.crm.deals.associations_api.get_all(
        event.get('object').get('objectId'), 'task')

    results = results.results

    for task in results:
        url = 'https://api.hubapi.com/engagements/v1/engagements/' + task.id
        headers = { 'Content-Type': 'application/json' }
        body = {
                engagement: {},
                metadata: {
                  status: 'COMPLETED'
                }
              }
        auth = os.getenv('HAPIKEY')
        requests.patch(url=url, headers=headers, body=body, auth=auth)
