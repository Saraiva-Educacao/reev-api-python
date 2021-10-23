from src.data.api import ReevAPI


class Reev:

    def __init__(self):
        self.reev_api = ReevAPI()

    def get_records(self, table_name):
        if table_name == 'contacts':
            print('Getting contacts...')
            return self.reev_api.get_contacts()
        else:
            return "The table name you provided is not valid."

    def get_schema(self, table):

        if table == 'contacts':
            contacts_schema = [
                {"column_name": "id", "column_type": "INTEGER"},
                {"column_name": "first_name", "column_type": "STRING"},
                {"column_name": "last_name", "column_type": "STRING"},
                {"column_name": "email", "column_type": "STRING"},
                {"column_name": "business", "column_type": "STRING"},
                {"column_name": "position", "column_type": "STRING"},
                {"column_name": "address", "column_type": "STRING"},
                {"column_name": "cellphone", "column_type": "STRING"},
                {"column_name": "telephone", "column_type": "STRING"},
                {"column_name": "url", "column_type": "STRING"},
                {"column_name": "linkedin", "column_type": "STRING"},
                {"column_name": "stage", "column_type": "STRING"},
                {"column_name": "flow_id", "column_type": "INTEGER"},
                {"column_name": "contact_group", "column_type": "STRING"},
                {"column_name": "responsible", "column_type": "STRING"},
                {"column_name": "recipient_status", "column_type": "STRING"},
                {"column_name": "lost_reason_title", "column_type": "STRING"},
                {"column_name": "created_at", "column_type": "DATETIME"},
                {"column_name": "updated_at", "column_type": "DATETIME"},
                {"column_name": "product", "column_type": "STRING"},
                {"column_name": "variable2", "column_type": "STRING"},
                {"column_name": "variable3", "column_type": "STRING"},
            ]
            custom_fields = self.reev_api.get_custom_fields()
            print(custom_fields)
            for field in custom_fields:
                contacts_schema.append({"column_name": field, "column_type": "STRING"})

            return contacts_schema

        else:
            raise KeyError(f"Table {table} not available.")
