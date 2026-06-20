from unittest.mock import MagicMock, patch

import pytest
from werkzeug.exceptions import NotFound

from debug_decorator import auto_debug_with_openai


def test_http_exception_passes_through_without_calling_openai():
    @auto_debug_with_openai
    def view():
        raise NotFound()

    with patch("debug_decorator._get_client") as mock_get_client:
        with pytest.raises(NotFound):
            view()
        mock_get_client.assert_not_called()


def test_unexpected_exception_calls_openai_and_reraises():
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content="Looks like a KeyError, check your dict access."))
    ]

    @auto_debug_with_openai
    def view():
        raise KeyError("missing")

    with patch("debug_decorator._get_client", return_value=mock_client):
        with pytest.raises(KeyError):
            view()
        mock_client.chat.completions.create.assert_called_once()


def test_openai_failure_does_not_mask_original_exception():
    with patch("debug_decorator._get_client", side_effect=RuntimeError("no api key")):
        @auto_debug_with_openai
        def view():
            raise ValueError("original error")

        with pytest.raises(ValueError):
            view()
