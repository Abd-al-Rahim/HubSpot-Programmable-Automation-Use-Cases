import os
from hubspot import HubSpot

def main(event):

  hubspot = HubSpot(api_key=os.getenv('HAPIKEY'))
  
  #getting values from properties
  address = event.get('inputFields').get('address')
  city = event.get('inputFields').get('city')
  state = event.get('inputFields').get('state')
  country = event.get('inputFields').get('country')
  zip = event.get('inputFields').get('zip')
  
  #concatenating the above properties into one property
  completeAddress = (address + ", " + city + ", " + state + ", " + country + ", " + zip)

  return {
    "outputFields": {
      'completeAddress': completeAddress
    }
  }
