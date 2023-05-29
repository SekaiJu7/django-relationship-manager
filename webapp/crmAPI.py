from tinydb import TinyDB, where
from pathlib import Path
import re
import string  # inclut automatiquement tous les symboles, ponctuation
from faker import Faker


class User:
    DB = TinyDB(Path(__file__).resolve().parent / "data.json", indent=4)

    def __init__(self, fname: str, lname: str, phone_number: int = 0, address: str = ""):
        self.fname = fname
        self.lname = lname
        self.phone_number = phone_number
        self.address = address

    def __str__(self):
        return f"{self.full_name}\n{self.phone_number}\n{self.address}"

    def __repr__(self):
        return f"User({self.fname} {self.lname})"

    @property  # on utilise une propriété pour retourner dynamiquement les attributs sinon on restera sur les valeurs créees dans le init
    def full_name(self):
        return f"{self.fname} {self.lname}"

    @property
    def db_instance(self):
        return User.DB.get((where('fname') == self.fname) & (where('lname') == self.lname))
        # retourne un objet tiny db table document avec le doc id (numéro de l'élément
        # contenant le dict et le dict)

    def _checks(self):
        self._check_name()
        self._check_phone_number()

    def _check_name(self):
        if not (self.fname and self.lname):
            raise ValueError("Le prénom et le nom ne peuvent pas être vides.")

        special_characters = string.punctuation + string.digits
        for _ in self.fname + self.lname:
            if _ in special_characters:
                raise ValueError(f"Nom invalide : {self.full_name}")

    def _check_phone_number(self):
        phone_digits = re.sub(r"[+()\s]*", "", self.phone_number)
        if len(phone_digits) < 10 or not phone_digits.isdigit():
            raise ValueError(f"Le numéro de téléphone {self.phone_number} est invalide.")

    def save(self, validate_data: bool = False) -> int:
        if validate_data:
            self._checks()

        return User.DB.insert(self.__dict__)

    def exists(self):
        return bool(self.db_instance)  # bool(none)-> False bool({}) -> True

    def delete(self) -> list[int]:
        if self.exists():
            return User.DB.remove(doc_ids=[self.db_instance.doc_id])
        return []


def get_users():
    return [User(**user) for user in User.DB.all()]


if __name__ == "__main__":
    Emile = User(fname='Emile', lname="Poulain")
    print(Emile.delete())

    Fake = Faker(locale="fr_FR")
    for _ in range(10):
        user = User(fname=Fake.first_name(),
                    lname=Fake.last_name(),
                    phone_number=Fake.phone_number(),
                    address=Fake.address())
        print(user.save())
