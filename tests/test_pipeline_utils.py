import unittest
import time
from bot_ai.selector.pipeline_utils import _safe_ticker, _cache_valid

class TestPipelineUtils(unittest.TestCase):

    def test_safe_ticker(self):
        self.assertEqual(_safe_ticker("BTC/USDT"), "BTCUSDT")
        self.assertEqual(_safe_ticker("eth-usdt"), "ETHUSDT")
        self.assertEqual(_safe_ticker("Ada/Busd"), "ADABUSD")

    def test_cache_valid(self):
        now = time.time()
        cache = {
            "key1": (now - 5, "value"),
            "key2": (now - 100, "value")
        }
        self.assertTrue(_cache_valid(cache, "key1", ttl=10))
        self.assertFalse(_cache_valid(cache, "key2", ttl=10))
        self.assertFalse(_cache_valid(cache, "missing", ttl=10))

if __name__ == "__main__":
    unittest.main()

