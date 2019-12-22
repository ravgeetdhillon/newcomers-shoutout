from datetime import datetime, timedelta
from variables import PROJECT_ID
import dateutil.parser
import pytz
import json
import os


def days_from_now(date):
    '''
    Calculate the days from today to a past date.
    '''

    date = dateutil.parser.parse(date)
    now = pytz.utc.localize(datetime.utcnow())
    days = (now - date).days

    return days


def load_data(file_name, directory='data'):
    '''
    Load the specified file from the given directory(optional).
    '''

    with open('{}/{}'.format(directory, file_name), 'r') as f:
        data = json.load(f)

    return data


def save_data(data, file_name, directory='data'):
    '''
    Save the data to the specified file.
    '''

    if not os.path.exists(directory):
        os.mkdir(directory)

    with open('{}/{}'.format(directory, file_name), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=True, indent=2)


def get_project_details(projects, project_id):
    """
    Returns the details about the given project_id.
    """

    for project in projects:
        if project['id'] == project_id:
            namespace = project['path_with_namespace']
            link = project['web_url']
            description = project['description'] if project['description'] is not None else ''
            issues_link = '{}/issues'.format(link)
            merge_requests_link = '{}/merge_requests'.format(link)
            break

    return namespace, link, description, issues_link, merge_requests_link
