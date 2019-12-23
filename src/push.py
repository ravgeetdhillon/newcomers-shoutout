from variables import GITLAB_SERVER, GITLAB_PRIVATE_TOKEN, PROJECT_ID
import os
import gitlab


def get_push_actions(directory, push_path):
    """
    Prepares the files for commit and returns the desired actions.
    """

    files = [file for file in os.listdir(directory) 
             if os.path.isfile(os.path.join(directory, file))]

    create_actions, update_actions = [], []
    
    for action_type in ['create', 'update']:
        
        for f in files:
            action = {
                'action': action_type,
                'file_path': '{}/{}'.format(push_path, f),
                'content': open('{}/{}'.format(directory, f)).read(),
            }

            if action_type == 'create':
                create_actions.append(action)
            else:
                update_actions.append(action)

    return create_actions, update_actions


def push_to_gitlab(gl, directory, push_path):
    """
    Push the given file to the project's repository on the specified file path and the branch.
    """

    create_actions, update_actions = get_push_actions(directory, push_path)
    project = gl.projects.get(id=PROJECT_ID)

    # commit the files to the project's repository
    # try with a commit that creates new files
    try:
        data = {
            'branch': 'master',
            'commit_message': '[skip ci] gitlab-ci created new data',
            'actions': create_actions
        }
        commit = project.commits.create(data)

    # if files already exist then update the files
    except Exception as e:
        data = {
            'branch': 'master',
            'commit_message': '[skip ci] gitlab-ci updated data',
            'actions': update_actions
        }
        commit = project.commits.create(data)
    
    return commit.attributes


def push():
    """
    Main function for the push.py.
    """

    gl = gitlab.Gitlab(GITLAB_SERVER, GITLAB_PRIVATE_TOKEN)
    gl.auth()

    response = push_to_gitlab(gl, 'data', 'src/data')
    print(response)
    
    response = push_to_gitlab(gl, 'data/user_events', 'src/data/user_events')
    print(response)


if __name__ == '__main__':
    push()
