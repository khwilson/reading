import unittest

from reading import config

class SimpleConfig(config.BaseConfig):
    a = 10
    b = 20


class DeepConfig(config.BaseConfig):
    c = 30
    simple_config = SimpleConfig()


class TestConfig(unittest.TestCase):
    def test_simple_config(self):
        conf = SimpleConfig()
        from_dict = {'a': 21, 'c': 40}
        not_present, invalid = conf.set_from_dict(from_dict)
        self.assertEqual(not_present, [('c', 40)])
        self.assertFalse(invalid)
        self.assertEqual(conf.a, 21)
        self.assertEqual(conf.b, 20)

        self.assertEqual(SimpleConfig().a, 10)

    def test_deep_config_not_present(self):
        conf = DeepConfig()
        from_dict = {'c': 10, 'simple_config': {'b': 40, 'c': 5}}
        not_present, invalid = conf.set_from_dict(from_dict)

        self.assertEqual(conf.c, 10)
        self.assertEqual(conf.simple_config.a, 10)
        self.assertEqual(conf.simple_config.b, 40)

        self.assertEqual(not_present, [('simple_config', [('c', 5)])])
        self.assertFalse(invalid)

    def test_deep_config_invalid(self):
        conf = DeepConfig()
        from_dict = {'simple_config': 'a'}
        not_present, invalid = conf.set_from_dict(from_dict)

        self.assertEqual(conf.c, 30)
        self.assertEqual(conf.simple_config.a, 10)
        self.assertEqual(conf.simple_config.b, 20)

        self.assertFalse(not_present)
        self.assertEqual(invalid, [('simple_config', from_dict['simple_config'])])
