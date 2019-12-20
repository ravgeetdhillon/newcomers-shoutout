from helpers import load_data, save_data, days_from_now
import json
import requests
import os


def combine_user_events_data():
    """
    Collect all the users' events files and combine them into one.
    """

    user_data = []
    for file in os.listdir('new_data/user_events'):
        data = load_data(file, directory='new_data/user_events')
        user_data += data

    user_data = sorted(user_data, key=lambda k: k['id'])
    save_data(user_data, 'user_events_data.json', 'new_data')

    return
    

def process_regular_users(user_data):
    """
    Process those users who are regular contributors to the projects hosted by GNOME.
    """
    
    projects = load_data('projects.json', 'new_data')
    
    regular_users = []
    
    for user in user_data:
        if len(user['events']) > 0:

            regular_user = {}
            
            for event in user['events']:
                if days_from_now( event['created_at'] ) >= 15:                    
                    if event['project_id'] in projects:
                        regular_user['author'] = event['author']
                        regular_users.append(regular_user)
                        break

    return regular_users


def process_newcomers(user_data):
    """
    Process those users who are new contributors to the projects hosted by GNOME.
    """
    
    projects = load_data('projects.json', 'new_data')
    
    newcomers = []
    
    for user in user_data:
        if len(user['events']) > 0:

            newcomer = {}
            newcomer['author'] = user['events'][0]['author']
            newcomer['events'] = []
            
            for event in user['events']:
                if days_from_now( event['created_at'] ) < 15:
                    if event['project_id'] in projects:
                        newcomer['events'].append(event)
        
            if len(newcomer['events']) > 0:
                newcomers.append(newcomer)

    return newcomers


def main():
    '''
    Main function for the process.py.
    '''

    combine_user_events_data()

    # load the data
    user_data = load_data('user_events_data.json', 'new_data')

    # process the users into regular users
    regular_users = process_regular_users(user_data)
    save_data(regular_users, 'regular_users.json', 'new_data')

    # process the users into newcomers
    newcomers = process_newcomers(user_data)
    save_data(newcomers, 'newcomers.json', 'new_data')


if __name__ == '__main__':
    main()