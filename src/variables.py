import os


GITLAB_SERVER = 'https://gitlab.gnome.org'
GITLAB_PRIVATE_TOKEN = os.environ.get('GITLAB_PRIVATE_TOKEN')

NOTEABLE_ACTIONS = ['opened', 'closed', 'pushed to', 'pushed new']
NOTEABLE_TARGETS = ['MergeRequests', 'Issue']
