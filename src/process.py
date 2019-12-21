from helpers import load_data, save_data, days_from_now, get_project_details
from variables import NOTEABLE_ACTIONS
import json
import requests
import os


def get_projects_ids():
    """
    Creates a list of project_ids.
    """

    projects = load_data('projects.json')

    project_ids = []
    for project in projects:
        project_ids.append(project['id'])

    return project_ids


def combine_user_events_data():
    """
    Collect all the users' events files and combine them into one.
    """

    user_data = []
    for file in os.listdir('data/user_events'):
        data = load_data(file, directory='data/user_events')
        user_data += data

    user_data = sorted(user_data, key=lambda k: k['id'])
    save_data(user_data, 'user_events_data.json')

    return
    

def process_regular_users(user_data):
    """
    Process those users who are regular contributors to the projects hosted by GNOME.
    """
    
    projects = get_projects_ids()
    
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
    
    projects = get_projects_ids()
    
    newcomers = []
    
    for user in user_data:
        if len(user['events']) > 0:

            newcomer = {}
            newcomer['author'] = user['events'][0]['author']
            newcomer['events'] = []
            
            for event in user['events']:
                if event['project_id'] in projects:
                    if days_from_now( event['created_at'] ) >= 15:
                        break

                    elif days_from_now( event['created_at'] ) < 15:
                        newcomer['events'].append(event)
        
            if len(newcomer['events']) > 0:
                newcomers.append(newcomer)

    return newcomers


def filter_newcomers(newcomers):
    """
    Filter the newcomers according to their contributions.
    """

    for newcomer in newcomers:
        newcomer['events'] = [event for event in newcomer['events']
                              if event['action_name'] in NOTEABLE_ACTIONS]

    newcomers = [newcomer for newcomer in newcomers
                 if len(newcomer['events']) > 0]

    return newcomers


def process_contributions(newcomers):
    """
    Process the contributions made by the newcomers and create a detailed report.
    """

    projects = load_data('projects.json')
    contributions = []

    for newcomer in newcomers:

        user_contributions = []
        
        for event in newcomer['events']:
            
            newcomer_name = newcomer['author']['name']
            event_action = event['action_name']
            project_name, project_link, project_description = get_project_details(projects, event['project_id'])
            
            if event['target_type'] == 'MergeRequest':
                sentence = "{} {} a merge request in {}.".format(newcomer_name, event_action, project_name)

            elif event['target_type'] == 'Issue':
                sentence = "{} {} an issue in {}.".format(newcomer_name, event_action, project_name)
            
            user_contributions.append(sentence)

        contributions.append(user_contributions)

    return contributions


def main():
    '''
    Main function for the process.py.
    '''

    combine_user_events_data()

    # load the data
    user_data = load_data('user_events_data.json')

    # process the users into regular users
    regular_users = process_regular_users(user_data)
    save_data(regular_users, 'regular_users.json')

    # process the users into newcomers
    newcomers = process_newcomers(user_data)
    save_data(newcomers, 'newcomers.json')

    # filter the newcomers
    filtered_newcomers = filter_newcomers(newcomers)
    save_data(filtered_newcomers, 'filtered_newcomers.json')

    # process the contributions made by newcomers
    contributions = process_contributions(filtered_newcomers)
    save_data(contributions, 'contributions.json')


if __name__ == '__main__':
    main()
