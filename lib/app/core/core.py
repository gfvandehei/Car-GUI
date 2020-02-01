from dependency_injector import containers, providers
from lib.app.core.logger import Logger


class Core(containers.DeclarativeContainer):
    """ the container for core components of the program """
    config = providers.Configuration('config')

    logger = providers.Singleton(Logger, name=config.logging.name, view_level=config.logging.level)

