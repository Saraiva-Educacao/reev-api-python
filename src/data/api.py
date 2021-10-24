from copy import deepcopy
from os import environ as env
import requests
from src.tools.exceptions import HTTPError
from src.tools.functions import format_string


class ReevAPI:
    def __init__(self, test=True):
        self.token = env.get('REEV_TOKEN')
        self._raw_contacts = []
        self.test = test

    def _get_raw_contacts(self):
        """Get all contacts information.

        Gather contact data from all the pages.
        Note that the data is presented in pages with a max of 15 contacts per page.
        The API is slow, therefore it takes a relatively long time to extract all data.

        Call with test=True to load only one page of data, in case you need to perform tests
        or develop new transformations.

        Returns:
            list[dict]: All the raw information about every contact in Reev.
        """

        if self._raw_contacts:
            return self._raw_contacts

        list_contacts_url = 'http://api.reev.co/v1/contacts?page={}'
        page = 1

        while page is not None:
            response = requests.get(list_contacts_url.format(page), params={'api_token': self.token})
            if response.status_code == 200:
                response_json = response.json()
                contacts = response_json['contacts']
                self._raw_contacts += contacts

                if page == 1:
                    total_contacts = response_json['meta']['total_count']
                    print('Total: ', total_contacts)

                print('Fetched: ', len(self._raw_contacts))

                page = response_json['meta']['next_page']
            else:
                raise HTTPError(f"The request returned the {response.status_code} error code")

            if self.test:
                break

        return self._raw_contacts

    def get_contacts(self):
        """Process contacts data.

        Unnest fields and perform data transformation on contact fields.

        Returns:
            list[dict]: Cleaned and processed contacts information, ready to be inserted into BQ
        """

        # Change to test=False to collect all data
        all_contacts = deepcopy(self._get_raw_contacts())

        for contact in all_contacts:
            # Unnesting custom fields
            for custom_field in contact['custom_fields']:
                contact[custom_field['field']] = custom_field['value']

            contact['responsible'] = contact.pop('user')['name']

            contact['flow_id'] = contact['flow'].get('id') if contact['flow'] else None

            contact['contact_group'] = contact.pop('contact_group')['name'] if contact['contact_group'] else None

            contact['created_at'] = contact['created_at'][:19]
            contact['updated_at'] = contact['updated_at'][:19]

            contact['product'] = contact.pop('variable1')

            del contact['tags']
            del contact['custom_fields']
            del contact['flow']

            # Cleaning key names
            keys = list(contact.keys())
            for key in keys:
                new_key = format_string(key)
                contact[new_key] = contact.pop(key)

        return all_contacts

    def _get_raw_flows(self):
        """Get all flows.

        Get all flows information raw data, to be processed in the get_flows function.

        Returns:
            list[dict]: Raw, unprocessed flows data.
        """
        flows_url = 'http://api.reev.co/v1/flows?page={}'
        page = 1
        next_page = 2
        all_flows = []

        while next_page is not None:
            response = requests.get(flows_url.format(page), params={'api_token': self.token})
            if response.status_code == 200:
                response = response.json()
                flows = response['flows']
                all_flows += flows

                next_page = response['meta']['next_page']
                page += 1
            else:
                raise HTTPError(f"The request returned the {response.status_code} error code")

        return all_flows

    def get_flows(self):
        """Transforms raw flows data.

        Basically, this function does two kinds of transformations:
            - Unnest email data (sent, open and reply)
            - Get flow count (total, by status and by stage)

        Returns:
            list[dict]: Processed flows data, ready to insert in BQ.
        """
        all_flows = self._get_raw_flows()

        for flow in all_flows:
            # Unnesting every element in the "email_statistic" section
            email_statistic = flow.pop('email_statistic')
            for key, value in email_statistic.items():
                flow[f'email_{key}'] = email_statistic[key]

            # Creator user_id
            flow['creator_id'] = flow.pop('user')['id']

            # Total number of contacts in the flow
            recipients_statistics = flow.pop('recipients_statistics')
            flow['total_contacts'] = recipients_statistics['total']['count']

            # Unnesting every element in the "by_stage" section
            for key, value in recipients_statistics['by_stage'].items():
                if key != 'conversion':
                    flow['stage_{}'.format(key)] = value['count']
                else:
                    flow[key] = value['value']

            # Unnesting every element in the "by_status" section
            for key, value in recipients_statistics['by_status'].items():
                flow['status_{}'.format(key)] = value['count']
                # Assure no column is named with "status_blacklisted"
                if key == 'blacklisted':
                    flow['status_blocklisted'] = flow.pop('status_blacklisted')

        return all_flows
