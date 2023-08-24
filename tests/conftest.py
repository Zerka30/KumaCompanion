import pytest
from api.KumaCompanion import KumaCompanion


@pytest.fixture(scope="session", autouse=True)
def teardown_kuma_companion():
    # This setup code runs once before any tests in the session
    yield
    # This teardown code runs once after all tests in the session
    KumaCompanion().disconnect()
