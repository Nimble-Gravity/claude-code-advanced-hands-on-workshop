from contoso import config


def test_constants_exist():
    assert config.TRANSFER_LIMIT == 100
    assert config.THROTTLE_PER_SECOND == 20
    assert config.DEFAULT_WINDOW_SECONDS == 60
