import logging
from unittest import TestCase
from tests.factories import AccountFactory
from service.common import status
from service.models import db, Account
from service.routes import app
from service import talisman

BASE_URL = "/accounts"
HTTPS_ENVIRON = {"wsgi.url_scheme": "https"}


class TestAccountService(TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
        app.logger.setLevel(logging.CRITICAL)
        talisman.force_https = False
        Account.init_db(app)

    def setUp(self):
        db.session.query(Account).delete()
        db.session.commit()
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()

    def _create_accounts(self, count):
        accounts = []
        for _ in range(count):
            acc = AccountFactory()
            resp = self.client.post(BASE_URL, json=acc.serialize())
            self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
            acc.id = resp.get_json()["id"]
            accounts.append(acc)
        return accounts

    def test_index_and_health(self):
        self.assertEqual(self.client.get("/").status_code, status.HTTP_200_OK)
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.get_json()["status"], "OK")

    def test_create_read_update_delete_list(self):
        acc = self._create_accounts(1)[0]
        resp = self.client.get(f"{BASE_URL}/{acc.id}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        data["name"] = "Updated Name"
        resp = self.client.put(f"{BASE_URL}/{acc.id}", json=data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.get_json()["name"], "Updated Name")
        self.assertEqual(len(self.client.get(BASE_URL).get_json()), 1)
        resp = self.client.delete(f"{BASE_URL}/{acc.id}")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.client.get(f"{BASE_URL}/{acc.id}").status_code, status.HTTP_404_NOT_FOUND)

    def test_error_handlers(self):
        self.assertEqual(self.client.post(BASE_URL, json={}).status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            self.client.post(BASE_URL, json={}, content_type="text/html").status_code,
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        )
        self.assertEqual(self.client.put(f"{BASE_URL}/0", json={}).status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.client.delete(BASE_URL).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_security_headers_and_cors(self):
        resp = self.client.get("/", environ_overrides=HTTPS_ENVIRON)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.headers.get("X-Frame-Options"), "SAMEORIGIN")
        self.assertEqual(resp.headers.get("X-Content-Type-Options"), "nosniff")
        self.assertEqual(resp.headers.get("Content-Security-Policy"), "default-src 'self'; object-src 'none'")
        self.assertEqual(resp.headers.get("Referrer-Policy"), "strict-origin-when-cross-origin")
        self.assertEqual(resp.headers.get("Access-Control-Allow-Origin"), "*")
