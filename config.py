import os

KEY = os.environ.get("WEBHOOK_PASSPHRASE")

BINANCE_ENABLED = False
BINANCE_TESTNET = False
BINANCE_API_KEY = ''
BINANCE_API_SECRET = ''
if (os.environ.get("BINANCE_ENABLED") == 'Y'):
  BINANCE_ENABLED = True

  if (os.environ.get("BINANCE_TESTNET") == 'Y'):
    BINANCE_TESTNET = True

  BINANCE_API_KEY=os.environ.get("API_KEY")
  BINANCE_API_SECRET=os.environ.get("API_SECRET")