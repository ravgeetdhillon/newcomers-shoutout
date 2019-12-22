from fetch import fetch
from process import process
from push import push


def app():
    """
    Main function for the app.
    """
    
    # fetch the data
    fetch()

    # process the data
    process()
    
    # push the data to the repository
    push()


if __name__ == '__main__':
    app()
