import logging as _logging

import yaml


_config = None
_logger = _logging.getLogger(__name__)


def get_config():
    return _config


def dump_config_to_dict(cfg=None):
    """
    Take a BaseConfig object and serialize it into a python dictionary.

    :param BaseConfig cfg: A config object
    :return: A dictionary version of the config
    :rtype: dict
    """
    if not cfg:
        cfg = get_config()

    output = {}
    for attrname in _data_attrnames(cfg):
        attr = getattr(cfg, attrname)
        if isinstance(attr, BaseConfig):
            # Recurse until basic types appear
            output[attrname] = dump_config(cfg=attr)
        elif not hasattr(attr, '__call__'):
            # Assume that there aren't terribly complex types
            output[attrname] = attr

    return output


def dump_config(cfg=None):
    """
    Take a BaseConfig object and serialize it as a yaml string

    :param BaseConfig cfg: A config object
    :return: A serialized version of the config
    :rtype: str
    """
    if not cfg:
        cfg = get_config()

    return yaml.dump(dump_config_to_dict(cfg=cfg))


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


def _data_attrnames(obj):
    attrnames = [attrname for attrname in dir(obj) if not attrname.startswith('__') and
                                                  not hasattr(getattr(obj, attrname), '__call__')]
    attrnames.sort()
    return attrnames


class BaseConfig(object):

    def __init__(self, from_dict=None, warn_bad_keys=True):
        self.set_from_dict(from_dict=from_dict, warn_bad_keys=warn_bad_keys)

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

    def __eq__(self, other):
        if type(other) is not type(self):
            return False

        self_attrs = set(_data_attrnames(self))
        other_attrs = set(_data_attrnames(other))

        if not self_attrs == other_attrs:
            return False

        return all(getattr(self, attrname) == getattr(other, attrname) for attrname in self_attrs)

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        attrnames = _data_attrnames(self)
        return ('[' +
                ', '.join(attrname + '=' + str(getattr(self, attrname)) for attrname in attrnames) +
                ']')

class TwilioConfig(BaseConfig):
    account = "nope"
    token = "hahahaha"
    from_number = "9991234567"

    def __init__(self, *args, **kwargs):
        super(TwilioConfig, self).__init__(*args, **kwargs)


class DatabaseConfig(BaseConfig):
    scheme = 'sqlite'
    host = 'example.db'
    port = ''
    user = ''
    password = ''

    def __init__(self, *args, **kwargs):
        super(DatabaseConfig, self).__init__(*args, **kwargs)


class Config(BaseConfig):

    twilio = TwilioConfig()
    database = DatabaseConfig()

    def __init__(self, *args, **kwargs):
        super(Config, self).__init__(*args, **kwargs)
