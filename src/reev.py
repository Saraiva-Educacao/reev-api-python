from src.data.api import ReevAPI


class Reev:

    def __init__(self):
        self.reev_api = ReevAPI()

    def get_records(self, table_name):
        if table_name == 'contacts':
            print('Getting contacts...')
            return self.reev_api.get_contacts()
        elif table_name == 'flows':
            print('Getting flows...')
            return self.reev_api.get_flows()

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

        elif table == 'flows':
            flows_schema = [
                {"column_name": "id", "column_type": "INTEGER"},
                {"column_name": "name", "column_type": "STRING"},
                {"column_name": "duration_in_days", "column_type": "INTEGER"},
                {"column_name": "actions_count", "column_type": "INTEGER"},
                {"column_name": "status", "column_type": "STRING"},
                {"column_name": "conversion", "column_type": "FLOAT"},
                {"column_name": "semi_automatic", "column_type": "BOOLEAN"},
                {"column_name": "email_sent", "column_type": "INTEGER"},
                {"column_name": "email_accepted", "column_type": "INTEGER"},
                {"column_name": "email_rejected", "column_type": "INTEGER"},
                {"column_name": "email_delivery", "column_type": "INTEGER"},
                {"column_name": "email_bounce", "column_type": "INTEGER"},
                {"column_name": "email_open", "column_type": "INTEGER"},
                {"column_name": "email_reply", "column_type": "INTEGER"},
                {"column_name": "email_soft_bounce", "column_type": "INTEGER"},
                {"column_name": "creator_id", "column_type": "INTEGER"},
                {"column_name": "total_contacts", "column_type": "INTEGER"},
                {"column_name": "stage_mql", "column_type": "INTEGER"},
                {"column_name": "stage_sql", "column_type": "INTEGER"},
                {"column_name": "stage_lead", "column_type": "INTEGER"},
                {"column_name": "stage_lost", "column_type": "INTEGER"},
                {"column_name": "stage_client", "column_type": "INTEGER"},
                {"column_name": "stage_prospect", "column_type": "INTEGER"},
                {"column_name": "stage_smart_lead", "column_type": "INTEGER"},
                {"column_name": "stage_opportunity", "column_type": "INTEGER"},
                {"column_name": "status_active", "column_type": "INTEGER"},
                {"column_name": "status_paused", "column_type": "INTEGER"},
                {"column_name": "status_bounced", "column_type": "INTEGER"},
                {"column_name": "status_finished", "column_type": "INTEGER"},
                {"column_name": "status_connected", "column_type": "INTEGER"},
                {"column_name": "status_converting", "column_type": "INTEGER"},
                {"column_name": "status_blocklisted", "column_type": "INTEGER"},
                {"column_name": "status_interrupted", "column_type": "INTEGER"},
                {"column_name": "status_disqualified", "column_type": "INTEGER"},
                {"column_name": "status_not_connected", "column_type": "INTEGER"},
                {"column_name": "status_uninitialized", "column_type": "INTEGER"}
            ]
            return flows_schema

        elif table == 'users':
            users_schema = [
                {"column_name": "id", "column_type": "INTEGER"},
                {"column_name": "email", "column_type": "STRING"},
                {"column_name": "name", "column_type": "STRING"},
                {"column_name": "picture_url", "column_type": "STRING"},
                {"column_name": "role", "column_type": "STRING"},
            ]
            return users_schema

        elif table == 'contact_tags':
            contact_tags_schema = [
                {"column_name": "contact_id", "column_type": "INTEGER"},
                {"column_name": "tag_name", "column_type": "STRING"},
            ]
            return contact_tags_schema

        else:
            raise KeyError(f"Table {table} not available.")
