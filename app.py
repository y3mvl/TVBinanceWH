import json
from flask import Flask, request, jsonify
from binanceFutures import BinanceBot
import config

app = Flask(__name__)

###############################################################################
# Exchange Validation
###############################################################################

use_binance_futures = False
exchange = None
if config.BINANCE_ENABLED:
    print("Binance is enabled!")
    use_binance_futures = True
    # Exchange is now managed by BinanceBot, but keep for backward compatibility if needed
    bot = BinanceBot()
    exchange = bot.exchange
else:
    bot = None

@app.route('/')
def index():
    return jsonify({'message': 'Server is running!'})

@app.route('/webhook', methods=['POST'])
def webhook():
    print("Hook Received!")
    try:
        data = request.get_json(force=True)
    except Exception as e:
        return jsonify({"status": "error", "message": f"Invalid JSON: {e}"}), 400
    print(data)

    if not data or 'key' not in data or data['key'] != config.KEY:
        print("Invalid Key, Please Try Again!")
        return jsonify({
            "status": "error",
            "message": "Invalid Key, Please Try Again!"
        }), 401

    if data.get('exchange') == 'binance-futures':
        if use_binance_futures and bot:
            try:
                order_results = bot.run(data)
                return jsonify({
                    "status": "success",
                    "orders": order_results
                })
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 500
        else:
            return jsonify({"status": "error", "message": "Binance Futures not enabled."}), 400
    else:
        print("Invalid Exchange, Please Try Again!")
        return jsonify({
            "status": "error",
            "message": "Invalid Exchange, Please Try Again!"
        }), 400

@app.route('/balance', methods=['GET'])
def balance_endpoint():
    asset = request.args.get('asset', 'USDT')
    if not use_binance_futures or not bot:
        return jsonify({"status": "error", "message": "Binance not enabled."}), 400
    try:
        balance = bot.get_balance(asset)
        return jsonify({"asset": asset, "balance": balance})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/fullbalance', methods=['GET'])
def full_balance_endpoint():
    if not use_binance_futures or not bot:
        return jsonify({"status": "error", "message": "Binance not enabled."}), 400
    try:
        balance = bot.get_full_balance()
        return jsonify({"balance": balance})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)

