"""
This file contains pytest fixtures accessible from modules in the tests/ directory.
"""

import pytest
from babbagecoin.master.routes import app as master_app


@pytest.fixture(scope="module")
def test_client():
    master_app.testing = True
    return master_app.test_client()
