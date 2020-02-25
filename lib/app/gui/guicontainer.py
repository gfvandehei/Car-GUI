from dependency_injector import containers, providers
from lib.app.core.logger import Logger
from lib.app.gui.controllers.appcontroller import AppController
from lib.app.gui.views.appscreen import AppScreen

class GUIContainer(containers.DeclarativeContainer):
    """ the container for core components of the program """
    config = providers.Configuration('config')

    logger = providers.Singleton(Logger, name=config.logging.name, view_level=config.logging.level)
    app_controller = providers.Singleton(AppController, applications=config.apppath)
    app_screen = providers.Factory(AppScreen, app_controller=app_controller)