# Import modules and sub-packages
from .api import init_api
from .core import init_core
from .model import init_model
from .util import init_util


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
