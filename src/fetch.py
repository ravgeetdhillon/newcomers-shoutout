from helpers import save_data, load_data, get_date_30_days_now
from variables import GITLAB_SERVER, GITLAB_PRIVATE_TOKEN
import requests
import gitlab
import json
import os


def fetch_users_events(gl):
    """
    Download all the users on the https://gitlab.gnome.org and their first 10 events.
    """

    # get total number of users on the https://gitlab.gnome.org
    total_users = gl.users.list()[0].attributes['id']

    users = []
    for id in range(1, total_users + 1):

        # create a list of users
        # fetch their ids and their first 10 events
        try:
            user = gl.users.get(id=id, lazy=True)
            user_events = user.events.list(sort='asc', per_page=10)
            user_events = [event.attributes for event in user_events]
            user = {'id': id, 'events': user_events}
            users.append(user)
        except Exception as e:
            print(e)

        # after accessing 500 IDs, save them into a JSON file
        if id % 500 == 0:
            save_data(users, f'users_with_events_{id}.json')
            print(f'Downloaded and saved user events for {len(users)} users. Total completed = {id}.')
            users = []

    save_data(users, f'users_with_events_{id}.json')


def fetch_groups(gl):
    """
    Download all the groups on the https://gitlab.gnome.org.
    """

    # donot include the `Archive` group
    # id for `Archive` group is 4001
    blacklist = [4001]

    groups = requests.get(
        'https://gitlab.gnome.org/api/v4/groups', params={'per_page': 100}
    )
    groups = json.loads(groups.text)

    save_data(groups, 'groups.json')
    print(f'Downloaded and saved {len(groups)} groups.')

    # create a list of group_ids for downloading the projects in the each group
    group_ids = []
    for group in groups:
        if group['id'] not in blacklist:
            group_ids.append(group['id'])

    return group_ids


def fetch_projects(gl, group_ids):
    """
    Download all the projects on the https://gitlab.gnome.org.
    """

    # get the all the projects in each group
    projects = []
    for group_id in group_ids:
        group = gl.groups.get(id=group_id, lazy=True)
        group_projects = group.projects.list(all=True)
        projects += group_projects

    projects = [project.attributes for project in projects]

    save_data(projects, 'projects.json')
    print(f'Downloaded and saved {len(projects)} projects.')


def main():
    """
    Main function for the fetch.py.
    """

    # create a gitlab object and authenticate it
    gl = gitlab.Gitlab(GITLAB_SERVER, GITLAB_PRIVATE_TOKEN)
    gl.auth()

    # fetch the groups and get their group ids
    group_ids = fetch_groups(gl)

    # fetch the projects in each group and get their project ids
    fetch_projects(gl, group_ids)


if __name__ == '__main__':
    main()
