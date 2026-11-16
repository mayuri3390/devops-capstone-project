import logging
import unittest
from service import app
from service.models import Account, DataValidationError, db
from tests.factories import AccountFactory


class TestAccount(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
        app.logger.setLevel(logging.CRITICAL)
        Account.init_db(app)

    def setUp(self):
        db.session.query(Account).delete()
        db.session.commit()

    def tearDown(self):
        db.session.remove()

    def test_crud_account(self):
        acc = AccountFactory()
        acc.create()
        self.assertIsNotNone(acc.id)
        self.assertEqual(Account.find(acc.id).name, acc.name)
        acc.email = "new@example.com"
        acc.update()
        self.assertEqual(Account.find(acc.id).email, "new@example.com")
        self.assertEqual(Account.find_by_name(acc.name)[0].id, acc.id)
        self.assertEqual(len(Account.all()), 1)
        acc.delete()
        self.assertEqual(len(Account.all()), 0)

    def test_deserialize_errors(self):
        acc = Account()
        self.assertRaises(DataValidationError, acc.deserialize, {})
        self.assertRaises(DataValidationError, acc.deserialize, [])
        self.assertEqual(repr(Account(name="Foo")), "<Account Foo id=[None]>")
