import unittest
from xrag.configs import Configs


def test_loading_configs():
    configs = Configs()
    assert configs.API_NAME == "xrag"