"""Focused retry checks using mocked HTTP responses; does not call Gemini."""
import io
import os
import sys
import unittest
import urllib.error
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ai  # noqa: E402


class RetryTests(unittest.TestCase):
    def test_retries_503_then_returns_success(self):
        busy = urllib.error.HTTPError("https://example.invalid", 503, "Busy", None, io.BytesIO(b"busy"))
        ok = io.BytesIO(b'{"ok": true}')
        with patch.object(ai.urllib.request, "urlopen", side_effect=[busy, ok]) as request, \
                patch.object(ai.time, "sleep") as sleep:
            result = ai._post_json("https://example.invalid", {}, {})

        self.assertEqual(result, {"ok": True})
        self.assertEqual(request.call_count, 2)
        sleep.assert_called_once_with(1)

    def test_retries_read_timeout_then_returns_success(self):
        ok = io.BytesIO(b'{"ok": true}')
        with patch.object(ai.urllib.request, "urlopen", side_effect=[TimeoutError("read timed out"), ok]) as request, \
                patch.object(ai.time, "sleep") as sleep:
            result = ai._post_json("https://example.invalid", {}, {})

        self.assertEqual(result, {"ok": True})
        self.assertEqual(request.call_count, 2)
        sleep.assert_called_once_with(1)

    def test_gives_up_after_repeated_timeouts(self):
        with patch.object(ai.urllib.request, "urlopen", side_effect=TimeoutError("read timed out")) as request, \
                patch.object(ai.time, "sleep"):
            with self.assertRaisesRegex(RuntimeError, "read timed out"):
                ai._post_json("https://example.invalid", {}, {})

        self.assertEqual(request.call_count, ai.MAX_RETRIES + 1)

    def test_does_not_retry_non_transient_http_error(self):
        bad_request = urllib.error.HTTPError("https://example.invalid", 400, "Bad Request", None,
                                             io.BytesIO(b"bad request"))
        with patch.object(ai.urllib.request, "urlopen", side_effect=bad_request) as request, \
                patch.object(ai.time, "sleep") as sleep:
            with self.assertRaisesRegex(RuntimeError, "HTTP 400"):
                ai._post_json("https://example.invalid", {}, {})

        request.assert_called_once()
        sleep.assert_not_called()


if __name__ == "__main__":
    unittest.main(verbosity=2)
