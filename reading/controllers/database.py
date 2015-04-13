from sqlalchemy import create_engine

from .. import config
from .. import models

def get_database_connection(cfg=None):
    """
    From a config object return a database connection.

    :param config.Config.DatabaseConfig cfg: A config object
    :return: A database model
    :rtype: models.Database
    """
    if not cfg:
        cfg = config.get_config().database

    if cfg.scheme.lower() == 'sqlite':
        engine = create_engine('sqlite:///' + cfg.host)
        return models.Database(engine)
    else:
        raise ValueError("Currently only sqlite is supported")
