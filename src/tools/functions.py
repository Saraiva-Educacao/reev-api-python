# Useful working functions
from re import sub
from unidecode import unidecode


def format_string(field_name) -> object:
    """Remove special characters, remove whitespaces and lowercase the string.

    Args:
        field_name (str): Original field name. Eg: `Data de criação`.

    Returns:
        str: formatted field name. Eg: `data_de_criacao`.

    Examples:
        >>> format_string('Tags RD ')
        'tags_rd'

        >>> format_string('Razões de Perda ')
        'razoes_de_perda'

        >>> format_string('Ciências Contábeis ')
        'ciencias_contabeis'

        >>> format_string('Diretores/ Reitores')
        'diretores_reitores'
    """

    new_field_name = field_name.strip().lower().replace(' ', '_').replace('[', '')
    new_field_name = unidecode(new_field_name)
    new_field_name = sub('[^A-Za-z0-9]+', '_', new_field_name)

    return new_field_name
