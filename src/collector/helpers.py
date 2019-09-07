import re


def normalize_path(path: str) -> str:
    # Add a separator to the end of the specified path if one doesn't exist
    if not path.endswith('/') and not path.endswith('\\'):

        # Ensure OS specific path separator is used (Windows = '\', Mac & Linux = '/')
        if re.search('(/)', path):
            path += '/'
        else:
            path += '\\'

    return path.replace('\"', '')
