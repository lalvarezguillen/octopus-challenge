from unittest import mock
import pytest
import backend.jobs
from backend.jobs import frequency_analysis, store_in_db


@mock.patch("backend.jobs.fetch_page_text")
@mock.patch("backend.jobs.store_in_db")
def test_frequency_analysis(mock_store_in_db, mock_fetch_page):
    mock_fetch_page.return_value = "This is Sparta"

    result = frequency_analysis("https://dummy.com")
    assert result == [{"frequency": 1, "token": "sparta"}]

    assert mock_fetch_page.called
    assert mock_store_in_db.delay.called


@mock.patch("backend.jobs.URL")
@mock.patch("backend.jobs.Token")
class TestStoreInDB:
    @classmethod
    def setup_class(cls):  # Is there a simpler way?
        cls.old_conf = backend.jobs.CELERY.conf
        backend.jobs.CELERY.conf = {"encryptor": mock.MagicMock()}

    def test_store_in_db_existing(self, TokenMock, URLMock):
        URLMock.get_by_hash.return_value = "existing"

        counts = [{"token": "dummy", "frequency": 2}]
        store_in_db("http://dummy.com", counts)

        assert URLMock.get_by_hash.called
        assert not URLMock.new.called
        assert not TokenMock.batch_update.called

    def test_store_in_db_new(self, TokenMock, URLMock):
        URLMock.get_by_hash.return_value = None

        counts = [{"token": "dummy", "frequency": 2}]
        store_in_db("http://dummy.com", counts)

        assert URLMock.get_by_hash.called
        assert URLMock.new.called
        assert TokenMock.batch_update.called

    @classmethod
    def teardown_class(cls):
        backend.jobs.CELERY.conf = cls.old_conf
