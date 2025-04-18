import pytest
from common.api.trainer import TrainerApi
@pytest.fixture(scope="session")
def api():
    """
    Basic api fixture
    """
    pokemon_api = TrainerApi()
    yield pokemon_api