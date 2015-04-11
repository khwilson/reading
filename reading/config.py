import logging as _logging


_config = None
_logger = _logging.getLogger(__name__)


def get_config():
    return _config


def set_config(from_dict):
    global _config
    _config = Config(from_dict)


def set_config_from_env():
    global _config
    _config = Config()


def configure_app(flask_app):
    """
    Setup the flask app's configuration.

    :param flask.Flask flask_app: The app to configure
    """
    pass


class Config(object):

    testvalue = 10

    def __init__(self, from_dict=None):
        if not from_dict:
            return

        settable_keys = {k for k in self.__dict__.viewkeys() if not k.startswith('__')}
        not_kept_dict = {}
        for key, value in from_dict.viewitems():
            if key in settable_keys:
                self.__dict__[key] = value
            else:
                not_kept_dict[key] = value
        logger.warn("These config values were not used in the configuration: %s", not_kept_dict)
