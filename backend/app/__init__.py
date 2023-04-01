# Import modules and sub-packages
import api
import core
import model


# Define package-level functions
def init_app():
    """
    Initialize the app module
    """

    # Set up database
    model.init_model()

    # Set up core functionality
    core.init_core()

    # Set up api
    api.init_api()
