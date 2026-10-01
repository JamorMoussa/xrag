import unittest
from xrag_old.configs import Configs


def test_loading_configs():
    configs = Configs()
    assert configs.app_name == "xrag"