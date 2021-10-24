from json import load
from os import environ as env
import requests
from src.data.api import ReevAPI
from src.tools.exceptions import HTTPError
from unittest import mock, TestCase


env['REEV_TOKEN'] = 'REEV_TOKEN'


def mock_requests(*args, **kwargs):
    class MockResponse:
        def __init__(self, status_code, json_content=None):
            self.status_code = status_code
            self.json_content = json_content

        def content(self):
            return self.content

        def json(self):
            return self.json_content

    api_url = 'http://api.reev.co/v1'

    print(args[0])

    if args[0] == f"{api_url}/contacts?page=1":
        with open('tests/mocks/mock_contacts_response_page_1.json', 'r') as file:
            contacts_response = load(file)

        return MockResponse(200, contacts_response)

    if args[0] == f"{api_url}/contacts?page=2":
        with open('tests/mocks/mock_contacts_response_page_2.json', 'r') as file:
            contacts_response = load(file)

        return MockResponse(200, contacts_response)

    if args[0] == f"{api_url}/flows?page=1":
        with open('tests/mocks/mock_flows_response_page_1.json', 'r') as file:
            flows_response = load(file)

        return MockResponse(200, flows_response)

    if args[0] == f"{api_url}/flows?page=2":
        with open('tests/mocks/mock_flows_response_page_2.json', 'r') as file:
            flows_response = load(file)

        return MockResponse(200, flows_response)

    if args[0] == f"{api_url}/custom_fields":
        with open('tests/mocks/mock_custom_fields_response.json', 'r') as file:
            custom_fields_response = load(file)

        return MockResponse(200, custom_fields_response)

    if args[0] == f"{api_url}/users?page=1":
        with open('tests/mocks/mock_users_response.json', 'r') as file:
            users_response = load(file)

        return MockResponse(200, users_response)

    return MockResponse(404)


class TestReevApiTestFalse(TestCase):

    def setUp(self):
        self.reev_api = ReevAPI(test=False)

    def test_if__get_raw_contacts_raises_403_error_when_using_wrong_token(self):
        with self.assertRaisesRegex(HTTPError, 'The request returned the 403 error code'):
            self.reev_api._get_raw_contacts()

    @mock.patch.object(requests, 'get', side_effect=mock_requests)
    def test__get_raw_contacts(self, mock_contacts_requests):
        raw_contacts = self.reev_api._get_raw_contacts()
        self.assertIsInstance(raw_contacts, list)
        self.assertEqual(len(raw_contacts), 3)
        expected_keys = [
            'id',
            'first_name',
            'last_name',
            'email',
            'business',
            'position',
            'telephone',
            'cellphone',
            'address',
            'url',
            'linkedin',
            'stage',
            'custom_fields',
            'tags',
            'user',
            'flow',
            'contact_group',
            'recipient_status',
            'lost_reason_title',
            'created_at',
            'updated_at',
            'variable1',
            'variable2',
            'variable3'
        ]
        assert list(raw_contacts[0]) == expected_keys

    def test_if__get_raw_contacts_not_call_api_if_raw_contacts_is_not_empty(self):
        mock_contacts_requests = mock.patch.object(requests, 'get', side_effect=mock_requests)
        with mock_contacts_requests:
            raw_contacts_1 = self.reev_api._get_raw_contacts()
            self.assertIsInstance(raw_contacts_1, list)
            self.assertEqual(len(raw_contacts_1), 3)

        raw_contacts_2 = self.reev_api._get_raw_contacts()
        expected_keys = [
            'id',
            'first_name',
            'last_name',
            'email',
            'business',
            'position',
            'telephone',
            'cellphone',
            'address',
            'url',
            'linkedin',
            'stage',
            'custom_fields',
            'tags',
            'user',
            'flow',
            'contact_group',
            'recipient_status',
            'lost_reason_title',
            'created_at',
            'updated_at',
            'variable1',
            'variable2',
            'variable3'
        ]
        assert list(raw_contacts_2[0]) == expected_keys
        assert raw_contacts_1 == raw_contacts_2

    @mock.patch.object(ReevAPI, '_get_raw_contacts')
    def test_get_contacts(self, mock_raw_contacts):
        with open('tests/mocks/mock_raw_contacts.json', 'r') as file:
            mock_raw_contacts.return_value = load(file)
        with open('tests/expected_values/expected_contacts.json', 'r') as file:
            expected_contacts = load(file)
        contacts = self.reev_api.get_contacts()
        assert contacts == expected_contacts

    def test_if_get_flows_raises_403_error_when_using_wrong_token(self):
        with self.assertRaisesRegex(HTTPError, 'The request returned the 403 error code'):
            self.reev_api.get_flows()

    @mock.patch.object(requests, 'get', side_effect=mock_requests)
    def test_get_flows(self, mock_flows_response):
        flows = self.reev_api.get_flows()
        with open('tests/expected_values/expected_flows.json', 'r') as file:
            expected_flows = load(file)
        assert flows == expected_flows

    def test_if_get_custom_fields_raises_403_error_when_using_wrong_token(self):
        with self.assertRaisesRegex(HTTPError, 'The request returned the 403 error code'):
            self.reev_api.get_custom_fields()

    @mock.patch.object(requests, 'get', side_effect=mock_requests)
    def test_get_custom_fields(self, mock_custom_fields_response):
        custom_fields = self.reev_api.get_custom_fields()
        with open('tests/expected_values/expected_custom_fields.json', 'r') as file:
            expected_custom_fields = load(file)
        assert custom_fields == expected_custom_fields

    def test_if_get_users_raises_403_error_when_using_wrong_token(self):
        with self.assertRaisesRegex(HTTPError, 'The request returned the 403 error code'):
            self.reev_api.get_users()

    @mock.patch.object(requests, 'get', side_effect=mock_requests)
    def test_get_users(self, mock_users_response):
        users = self.reev_api.get_users()
        with open('tests/expected_values/expected_users.json', 'r') as file:
            expected_users = load(file)
        assert users == expected_users

    def test_if_get_contact_tags_raises_403_error_when_using_wrong_token(self):
        with self.assertRaisesRegex(HTTPError, 'The request returned the 403 error code'):
            self.reev_api.get_contact_tags()

    @mock.patch.object(requests, 'get', side_effect=mock_requests)
    def test_get_contact_tags(self, mock_contact_tags):
        contact_tags = self.reev_api.get_contact_tags()
        with open('tests/expected_values/expected_contact_tags.json', 'r') as file:
            expected_contact_tags = load(file)
        assert contact_tags == expected_contact_tags


class TestReevApiTesteTrue(TestCase):

    def setUp(self):
        self.reev_api = ReevAPI(test=True)

    def test_if__get_raw_contacts_raises_403_error_when_using_wrong_token(self):
        with self.assertRaises(HTTPError):
            self.reev_api._get_raw_contacts()

    @mock.patch.object(requests, 'get', side_effect=mock_requests)
    def test__get_raw_contacts(self, mock_contacts_requests):
        raw_contacts = self.reev_api._get_raw_contacts()
        self.assertIsInstance(raw_contacts, list)
        self.assertEqual(len(raw_contacts), 2)
        expected_keys = [
            'id',
            'first_name',
            'last_name',
            'email',
            'business',
            'position',
            'telephone',
            'cellphone',
            'address',
            'url',
            'linkedin',
            'stage',
            'custom_fields',
            'tags',
            'user',
            'flow',
            'contact_group',
            'recipient_status',
            'lost_reason_title',
            'created_at',
            'updated_at',
            'variable1',
            'variable2',
            'variable3'
        ]
        assert list(raw_contacts[0]) == expected_keys
        mock_contacts_requests.assert_called_once()
