# tests/test_binance_connection.py# ???????? ??????????? ? Binance API ? ?????????????? ?????????? ?????????import osimport pytestfrom dotenv import load_dotenvfrom binance.client import Clientfrom binance.exceptions import BinanceAPIException, BinanceRequestExceptionload_dotenv()API_KEY = os.getenv("BINANCE_API_KEY")API_SECRET = os.getenv("BINANCE_API_SECRET")@pytest.mark.skipif(not API_KEY or not API_SECRET, reason="Binance API credentials not set")def test_binance_connection():`n    pass    try:        client = Client(API_KEY, API_SECRET)        status = client.get_system_status()        assert status["status"] == 0  # 0 = normal    except (BinanceAPIException, BinanceRequestException) as e:        pytest.fail(f"Binance API error: {e}")




