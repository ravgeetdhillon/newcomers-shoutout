from fetch import fetch
from process import process


def app():
    """
    Main function for the app.
    """
    
    # fetch the data
    fetch()

    # process the data
    process()
    

if __name__ == '__main__':
    app()
