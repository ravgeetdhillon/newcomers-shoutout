from helpers import save_data, load_data, days_from_now
import os


noteable_actions = ['created', 'updated', 'closed',
                    'reopened', 'merged', 'pushed']

noteable_targets = ['issue', 'merge_requests']


def combine_user_events_data():
    """
    Collect all the user_events_files and combine them into one.
    """

    user_data = []
    for file in os.listdir('new_data/user_events'):
        data = load_data(file, directory='new_data/user_events')
        user_data += data

    return user_data


def process_regular_users(user_data):
    """
    Process those users who are regular contributors to the projects hosted by GNOME.
    """
    
    projects = load_data('projects.json', 'new_data')
    
    regular_users = []
    
    for user in user_data:
        if len(user['events']) != 0:
            for event in user['events']:
                if days_from_now( event['created_at'] ) > 30:
                    if event['project_id'] in projects:
                        user = event['author']
                        if user not in regular_users:
                            regular_users.append(user)
                        break

    return regular_users


user_data = combine_user_events_data()
regular_users = process_regular_users(user_data)

save_data(regular_users, 'regular_users.json', 'new_data')
