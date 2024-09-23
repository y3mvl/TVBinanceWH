import os

WEBHOOK_PASSPHRASE=os.environ.get("WEBHOOK_PASSPHRASE")

BINANCE_ENABLED = False
if (os.environ.get("BINANCE_ENABLED") == 'Y'):
  BINANCE_ENABLED = True

  BINANCE_TESTNET = False
  if (os.environ.get("BINANCE_TESTNET") == 'Y'):
    BINANCE_TESTNET = True

  BINANCE_API_KEY=os.environ.get("API_KEY")
  BINANCE_API_SECRET=os.environ.get("API_SECRET")