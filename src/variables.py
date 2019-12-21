import os

# gnome's gitlab server
GITLAB_SERVER = 'https://gitlab.gnome.org'

# gitlab private token to access the gitlab api
GITLAB_PRIVATE_TOKEN = os.environ.get('GITLAB_PRIVATE_TOKEN')

# actions and targets that count as actual contributions
NOTEABLE_ACTIONS = ['opened', 'closed', 'pushed to', 'pushed new']
NOTEABLE_TARGETS = ['MergeRequest', 'Issue']
