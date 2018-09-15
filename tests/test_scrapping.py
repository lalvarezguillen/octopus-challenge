import pytest
import responses
from octopus.scraping import fetch_page_text, RetriableHTTPError, HTTPError


@responses.activate
def test_fetch_page_text():
    url = "http://dummywebsite.com"
    responses.add(responses.GET, url, body="<div>asd</div>", status=200)
    text = fetch_page_text(url)
    assert "asd" == text


@responses.activate
def test_fetch_page_remove_script():
    url = "http://dummywebsite.com"
    body = "<div>good</div><script>bad</script>"
    responses.add(responses.GET, url, body=body, status=200)
    text = fetch_page_text(url)
    assert "good" == text


@responses.activate
def test_fetch_retriable():
    url = "http://dummywebsite.com"
    responses.add(responses.GET, url, status=502)
    with pytest.raises(RetriableHTTPError) as err:
        fetch_page_text(url)
        assert err


@responses.activate
def test_http_error():
    url = "http://dummywebsite.com"
    responses.add(responses.GET, url, status=404)
    with pytest.raises(HTTPError) as err:
        fetch_page_text(url)
        assert err
