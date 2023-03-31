# Import modules and sub-packages
from . import api
from . import core
from . import model


# Define package-level functions
def init_app():
    """
    Initialize the app
    """

    # Set up database
    model.init_db()

    # Set up core functionality
    core.init_core()

    # Set up api
    api.init_api()
