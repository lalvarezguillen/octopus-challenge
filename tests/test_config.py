from backend.config import Config


def test_init_config():
    conf = Config()
    assert conf.PRIVATE_KEY
    assert conf.SALT


def test_export():
    conf = Config()
    exported = conf.export()
    assert isinstance(exported, dict)
