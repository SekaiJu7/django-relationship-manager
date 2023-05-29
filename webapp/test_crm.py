from crmAPI import User
import pytest
from tinydb import TinyDB
from tinydb.storages import MemoryStorage


# Une fixture permet de donner aux fonctions de test ce dont elles ont besoin.
# Elles permettent de ne pas réutiliser le même code dans chaque fonction de test.

@pytest.fixture
def setup_db():
    User.DB = TinyDB(storage=MemoryStorage)


@pytest.fixture
def user(setup_db):
    u = User(fname="Martin", lname="Collins",
             address="22 avenue du grand pont",
             phone_number="0610548552")
    u.save()
    return u


def test_full_name(user):  # (user) permet d'utiliser le fixture
    assert user.full_name == "Martin Collins"


def test_exists(user):
    assert user.exists() is True


def test__check_phone_number():
    user_good = User(fname="Bon", lname="UserGood", address="5 rue de l'emilion", phone_number="0610548963")
    user_bad = User(fname="Mauvais", lname="UserGood", address="5 rue de l'emilion", phone_number="abcd")

    with pytest.raises(ValueError) as err:
        user_bad._check_phone_number()
    assert "invalide" in str(err.value)


