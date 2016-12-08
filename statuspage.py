#!/usr/bin/env python

# Description:
#   Create/update/delete incidnet on statuspage.io
#   https://yelpstatus.statuspage.io/
#

import argparse
import json
import re
import requests
import time


# statuspage fqdn
statuspage_url = 'https://api.statuspage.io/v1/pages/'
# Api token
api_token = 'd307d7d7-aad3-4259-b836-740c9ede43bb'
# Api header
api_header = {'Authorization': 'OAuth ' + api_token}
# statuspage.io page #
statuspage_id = '9xftmss2g1f9'

class Incident(object):

    def __init__(self, args):

        self.args = args

    def create_realtime(self):
        data = {
            'incident': {
                'name': self.args.name,
                'status': self.args.status,
                'message': self.args.message
            }

        }
        try:
            api_fqdn = statuspage_url + statuspage_id + '/incidents.json'
            response = requests.request("POST", api_fqdn, data=json.dumps(data), headers=api_header)
            response_formated = json.loads(response.text)
        except requests.exceptions.RequestException as e:
            print 'error:' + e
            sys.exit(1)
        return response_formated['incident_updates'][0]['incident_id']

    def update_realtime(self):
        data = {
            'incident': {
                'status': self.args.status,
                'message': self.args.message
            }

        }
        try:
            api_fqdn = statuspage_url + statuspage_id + '/incidents/' + self.args.incident_id + '.json'
            response = json.loads(requests.request("PATCH", api_fqdn, data=json.dumps(data), headers=api_header))
        except:
            raise Exception('problem creating an incident')
        return response

    def delete(self):
        try:
            api_fqdn = statuspage_url + statuspage_id + '/incidents/' + self.args.incident_id + '.json'
            response = requests.request("DELETE", api_fqdn, data='', headers=api_header)
        except requests.exceptions.RequestException as e:
            print 'error:' + e
            sys.exit(1)
        return json.loads(response.text)

    def search(self):
        try:
            api_fqdn = statuspage_url + statuspage_id + '/incidents.json?q=' + self.args.search
            response = requests.request("GET", api_fqdn, data='', headers=api_header)
            response_formated = json.loads(response.text)
            incident_list = [[incident['incident_updates'][0]['incident_id']] for incident in response_formated]

#            incident_list['data'] = {{
#                'incident_id': incident[0]['incident_updates'][0]['incident_id'],
#                'message': incident[0]['incident_updates'][0]['body']
#            } for incident in response_formated}
        except requests.exceptions.RequestException as e:
            print 'error:' + e
            sys.exit(1)
        return incident_list


def arguments_to_functions(args):
    incident = Incident(args)
    if args.create:
        print(incident.create_realtime())
    elif args.delete:
        print(incident.delete())
    elif args.update:
        print(incident.update_realtime())
    elif args.search:
        print(incident.search())
    else:
        raise Exception('please create, delete or update an incident')


def main():

    app_caption = 'Statuspage.io incident management'
    arg_caption_create = 'Create an real time incident: investigating|identified|monitoring|resolved'
    arg_caption_delete = 'Delete an incident'
    arg_caption_update = 'Update an incident'
    arg_caption_name = 'Real time incident name'
    arg_caption_status = 'Real time incident status: investigating|identified|monitoring|resolved '
    arg_caption_message = 'Real time incident core message'
    arg_caption_incident_id = 'Real time incident id'
    arg_caption_search = 'Search incident'

    parser = argparse.ArgumentParser(description=app_caption)
    parser.add_argument('--create', action='store_true',
                        help=arg_caption_create)
    parser.add_argument('--delete', action='store_true',
                        help=arg_caption_delete)
    parser.add_argument('--update', action='store_true',
                        help=arg_caption_update)
    parser.add_argument('--status', type=str,
                        help=arg_caption_status)
    parser.add_argument('--message', type=str,
                        help=arg_caption_message)
    parser.add_argument('--incident_id', type=str,
                        help=arg_caption_incident_id)
    parser.add_argument('--name', type=str,
                        help=arg_caption_name)
    parser.add_argument('--search', type=str,
                        help=arg_caption_search)

    args = parser.parse_args()
    arguments_to_functions(args)

if __name__ == '__main__':
    main()
