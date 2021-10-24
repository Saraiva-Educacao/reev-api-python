import json
from src.reev import Reev
from src.tools.exceptions import PipelineError


def main(tables=None):

    if not tables:
        tables = [
            'contacts',
            'flows',
            'contact_tags',
            'users'
        ]

    reev = Reev()

    error_messages = []
    for table in tables:
        try:
            records = reev.get_records(table_name=table)
            print(f'Extracted {len(records)} {table}')

            print('Saving records...')
            with open(f'exported_data/{table}.json', 'w') as outfile:
                json.dump(records, outfile)

        except Exception as error:
            print(f'Could not transform or load all records for table {table}, giving up.')
            error_messages.append(f'Error in table {table}: {str(error)}')

    if error_messages:
        raise PipelineError(', '.join(error_messages))
    else:
        return 'OK'


if __name__ == '__main__':
    main()
