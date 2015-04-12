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


class BaseConfig(object):
    def set_from_dict(self, from_dict=None, warn_bad_keys=True):
        if not from_dict:
            return

        all_keys = set(from_dict.keys())
        dict_keys = {key for key, value in from_dict.viewitems() if isinstance(value, dict)}
        non_dict_keys = all_keys - dict_keys

        valid_names = {name for name in dir(self) if not name.startswith('__')}

        not_present_key_values = []
        invalid_key_values = []
        for key in all_keys:
            if key not in valid_names:
                not_present_key_values.append((key, from_dict[key]))
                continue

            if key in dict_keys:
                if not isinstance(getattr(self, key), BaseConfig):
                    invalid_key_values.append((key, from_dict[key]))
                    continue
                not_present, invalid = getattr(self, key).set_from_dict(from_dict=from_dict[key],
                                                                        warn_bad_keys=False)
                if not_present:
                    not_present_key_values.append((key, not_present))
                if invalid:
                    invalid_key_values.append((key, invalid))

            else:
                if isinstance(getattr(self, key), BaseConfig):
                    invalid_key_values.append((key, from_dict[key]))
                    continue
                setattr(self, key, from_dict[key])

        if warn_bad_keys:
            _logger.warn("The following keys were not present in the config: {}".format(
                not_present_key_values))
            _logger.warn("The following configurations were invalid: {}".format(invalid_key_values))
        return not_present_key_values, invalid_key_values


class TwilioConfig(BaseConfig):
    account = "nope"
    token = "hahahaha"
    from_number = "9991234567"


class DatabaseConfig(BaseConfig):
    scheme = 'sqlite'
    host = 'example.db'
    port = ''
    user = ''
    password = ''


class Config(BaseConfig):

    twilio = TwilioConfig()
    database = DatabaseConfig()
