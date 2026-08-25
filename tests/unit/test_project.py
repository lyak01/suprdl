from importlib.metadata import version


def test_package_version_is_available() -> None:
    assert version("suprdl") == "0.1.0"
