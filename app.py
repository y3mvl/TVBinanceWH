import json
from flask import Flask, request, jsonify
from binanceFutures import BinanceBot
import config
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
)
logger = logging.getLogger(__name__)

###############################################################################
# Exchange Validation
###############################################################################

use_binance_futures = False
exchange = None
if config.BINANCE_ENABLED:
    logger.info("Binance is enabled!")
    use_binance_futures = True
    # Exchange is now managed by BinanceBot, but keep for backward compatibility if needed
    bot = BinanceBot()
    exchange = bot.exchange
else:
    bot = None

@app.route('/')
def index():
    logger.info('Health check at /')
    return jsonify({'message': 'Server is running!'})

@app.route('/webhook', methods=['POST'])
def webhook():
    logger.info("Webhook received!")
    try:
        data = request.get_json(force=True)
    except Exception as e:
        logger.error(f"Invalid JSON: {e}")
        return jsonify({"status": "error", "message": f"Invalid JSON: {e}"}), 400
    logger.info(f"Webhook data: {data}")

    if not data or 'key' not in data or data['key'] != config.KEY:
        logger.warning("Invalid Key, Please Try Again!")
        return jsonify({
            "status": "error",
            "message": "Invalid Key, Please Try Again!"
        }), 401

    if data.get('exchange') == 'binance-futures':
        if use_binance_futures and bot:
            try:
                order_results = bot.run(data)
                logger.info(f"Order results: {order_results}")
                return jsonify({
                    "status": "success",
                    "orders": order_results
                })
            except Exception as e:
                logger.error(f"Webhook error: {e}")
                return jsonify({"status": "error", "message": str(e)}), 500
        else:
            logger.warning("Binance Futures not enabled.")
            return jsonify({"status": "error", "message": "Binance Futures not enabled."}), 400
    else:
        logger.warning("Invalid Exchange, Please Try Again!")
        return jsonify({
            "status": "error",
            "message": "Invalid Exchange, Please Try Again!"
        }), 400

@app.route('/balance', methods=['GET'])
def balance_endpoint():
    asset = request.args.get('asset', 'USDT')
    if not use_binance_futures or not bot:
        logger.warning("Balance endpoint called but Binance not enabled.")
        return jsonify({"status": "error", "message": "Binance not enabled."}), 400
    try:
        balance = bot.get_balance(asset)
        logger.info(f"Balance for {asset}: {balance}")
        return jsonify({"asset": asset, "balance": balance})
    except Exception as e:
        logger.error(f"Balance error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/fullbalance', methods=['GET'])
def full_balance_endpoint():
    if not use_binance_futures or not bot:
        logger.warning("Full balance endpoint called but Binance not enabled.")
        return jsonify({"status": "error", "message": "Binance not enabled."}), 400
    try:
        balance = bot.get_full_balance()
        logger.info(f"Full balance: {balance}")
        return jsonify({"balance": balance})
    except Exception as e:
        logger.error(f"Full balance error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)

