import requests
import json
from dateutil.parser import parse

headers = {
    'accept': 'application/json',
    'X-API-KEY': 'supersecret!',
    'Content-Type': 'application/json',
}

credentialBoilerPlate = {
    'auto_remove': True,
    'credential_proposal': {
        '@type': 'issue-credential/1.0/credential-preview',
        'attributes': [
            {
                'mime-type': 'text/plain',
                'name': 'id',
                'value': 'F4 10 31 01 AC 57 01"',
            },
            {
                'mime-type': 'text/plain',
                'name': 'vin',
                'value': 'WBY11CF080CH47081',
            },
            {
                'mime-type': 'text/plain',
                'name': 'modelcode',
                'value': 'iX 40 xDrive',
            },
        ],
    },
    'cred_def_id': '54uCo3cqfvxy5anTHTCD2i:3:CL:60376:DigitalCarKey',
    'trace': True,
    'connection_id': '93268e93-c2f7-4c45-9efb-3249ed147028',
}


responseConnections = requests.get('http://108.142.175.70:8010/connections', headers=headers)
if responseConnections.status_code == 200:
    lastConnection = None
    connections = json.loads(responseConnections.text)['results']
    # Check for latest connection
    for connection in connections:
        if connection['state'] == "active":
            if lastConnection == None or (connection['updated_at'] > lastConnection['updated_at']):
                lastConnection = connection
    # Issue Credential
    credentialBoilerPlate['connection_id'] = lastConnection['connection_id']
    # print(credentialBoilerPlate)
    responseIssueCredential = requests.post('http://108.142.175.70:8010/issue-credential/send', headers=headers, json=credentialBoilerPlate)
    if responseConnections.status_code == 200:
        print("Credential Issued to Connection: " + lastConnection['connection_id'])
else:
    print("No valid statuscode")