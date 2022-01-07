import pytest

from eligibility_server.hash import Hash as Hash


@pytest.fixture(autouse=True)
def hash(monkeypatch):
    hash = Hash()
    monkeypatch.setattr(hash, "_hash_inputs", False)
    monkeypatch.setattr(hash, "_hash_type", "")
    return hash


@pytest.fixture(autouse=True)
def setup_hash_input_false(monkeypatch):
    monkeypatch.setenv("HASH_INPUTS", "false")
    monkeypatch.setenv("HASH_TYPE", "")
