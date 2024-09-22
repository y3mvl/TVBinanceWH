import json, config
from flask import Flask, render_template, request, jsonify
import ccxt
from binanceFutures import BinanceBot

app = Flask(__name__)

'''
# load config.json
with open('config.json') as config_file:
    config = json.load(config_file)
'''

###############################################################################
#
#             This Section is for Exchange Validation
#
###############################################################################

use_binance_futures = False
if config.BINANCE_ENABLED:
        print("Binance is enabled!")
        use_binance_futures = True

        exchange = ccxt.binance({
        'apiKey': config.BINANCE_API_KEY,
        'secret': config.BINANCE_API_SECRET,
        'options': {
            'defaultType': 'future',
            },
        'urls': {
            'api': {
                'public': 'https://testnet.binancefuture.com/fapi/v1',
                'private': 'https://testnet.binancefuture.com/fapi/v1',
            }, }
        })
        exchange.set_sandbox_mode(True)

@app.route('/')
def index():
    return {'message': 'Server is running!'}

@app.route('/webhook', methods=['POST'])
def webhook():
    print("Hook Received!")
    #data = request.form.to_dict()  ##This is for private testing locally
    data = json.loads(request.data)
    print(data)

    if int(data['key']) != config['KEY']:
        print("Invalid Key, Please Try Again!")
        return {
            "status": "error",
            "message": "Invalid Key, Please Try Again!"
        }

    ##############################################################################
    #             Binance Futures
    ##############################################################################
    if data['exchange'] == 'binance-futures':
        if use_binance_futures:
            bot = BinanceBot()
            bot.run(data)
            return {
                "status": "success",
                "message": "Binance Futures Webhook Received!"
            }

    else:
        print("Invalid Exchange, Please Try Again!")
        return {
            "status": "error",
            "message": "Invalid Exchange, Please Try Again!"
        }

if __name__ == '__main__':
    app.run(debug=False)

