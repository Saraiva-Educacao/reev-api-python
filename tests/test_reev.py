from src.reev import Reev
from unittest import mock, TestCase


class TestReev(TestCase):

    @mock.patch('src.reev.ReevAPI.get_custom_fields')
    def test_get_schema_for_table_contacts(self, mock_custom_fields):
        mock_custom_fields.return_value = ['tags_rd', 'razoes_de_perda', 'tipo_de_escritorio', 'segmento']
        contacts_schema = Reev().get_schema('contacts')

        mock_custom_fields.assert_called_once()
        assert contacts_schema == [
            {'column_name': 'id', 'column_type': 'INTEGER'},
            {'column_name': 'first_name', 'column_type': 'STRING'},
            {'column_name': 'last_name', 'column_type': 'STRING'},
            {'column_name': 'email', 'column_type': 'STRING'},
            {'column_name': 'business', 'column_type': 'STRING'},
            {'column_name': 'position', 'column_type': 'STRING'},
            {'column_name': 'address', 'column_type': 'STRING'},
            {'column_name': 'cellphone', 'column_type': 'STRING'},
            {'column_name': 'telephone', 'column_type': 'STRING'},
            {'column_name': 'url', 'column_type': 'STRING'},
            {'column_name': 'linkedin', 'column_type': 'STRING'},
            {'column_name': 'stage', 'column_type': 'STRING'},
            {'column_name': 'flow_id', 'column_type': 'INTEGER'},
            {'column_name': 'contact_group', 'column_type': 'STRING'},
            {'column_name': 'responsible', 'column_type': 'STRING'},
            {"column_name": "recipient_status", "column_type": "STRING"},
            {"column_name": "lost_reason_title", "column_type": "STRING"},
            {"column_name": "created_at", "column_type": "DATETIME"},
            {"column_name": "updated_at", "column_type": "DATETIME"},
            {"column_name": "product", "column_type": "STRING"},
            {"column_name": "variable2", "column_type": "STRING"},
            {"column_name": "variable3", "column_type": "STRING"},
            {'column_name': 'tags_rd', 'column_type': 'STRING'},
            {'column_name': 'razoes_de_perda', 'column_type': 'STRING'},
            {'column_name': 'tipo_de_escritorio', 'column_type': 'STRING'},
            {'column_name': 'segmento', 'column_type': 'STRING'}
        ]
