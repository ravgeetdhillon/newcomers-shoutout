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
            newcomer_profile = newcomer['author']['web_url']
            event_action = event['action_name']
            project_name, project_link, project_description, project_issues_link, project_merge_requests_link = get_project_details(projects, event['project_id'])
            
            if event['target_type'] == 'MergeRequest':
                merge_request_link = '{}/{}'.format(project_merge_requests_link, event['target_iid'])
                sentence = '{} {} a merge request in {}. Merge Request link is {}. User profile is {}.'.format(newcomer_name, event_action, project_name, merge_request_link, newcomer_profile)

            elif event['target_type'] == 'Issue':
                issue_link = '{}/{}'.format(project_issues_link, event['target_iid'])
                sentence = '{} {} an issue in {}. Issue link is {}. User profile is {}.'.format(newcomer_name, event_action, project_name, issue_link, newcomer_profile)

            elif event['target_type'] is None:
                branch_name = event['push_data']['ref']
                commit_count = event['push_data']['commit_count']
                sentence = '{} {} `{}` branch with {} commits in {}. User profile is {}.'.format(newcomer_name, event_action, branch_name, commit_count, project_name, newcomer_profile)
            
            user_contributions.append(sentence)

        contributions.append(user_contributions)

    return contributions


def process():
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
    process()
