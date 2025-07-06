import json
import config
import time
import ccxt
import random
import string

class BinanceBot:
    def __init__(self):
        if config.BINANCE_TESTNET:
            self.exchange = ccxt.binance({
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
            self.exchange.set_sandbox_mode(True)
        else:
            self.exchange = ccxt.binance({
                'apiKey': config.BINANCE_API_KEY,
                'secret': config.BINANCE_API_SECRET,
                'options': {
                    'defaultType': 'future',
                },
                'urls': {
                    'api': {
                        'public': 'https://fapi.binance.com/fapi/v1',
                        'private': 'https://fapi.binance.com/fapi/v1',
                    }, }
            })
        self.clientId = None

    def create_string(self):
        N = 7
        res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
        baseId = 'y-20TVbiWH'
        self.clientId = baseId + str(res)
        return

    def calculate_qty(self, symbol, usd_amount):
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            current_price = ticker['last']
            qty = round(float(usd_amount) / current_price, 3)
            return qty
        except Exception as e:
            print(f"Error calculating qty: {e}")
            return 0

    def close_position(self, symbol):
        try:
            positions = self.exchange.fetch_positions(symbol)
            if positions:
                position = positions[0].get('positionAmt', 0)
            else:
                print("No open position to close.")
                return
            self.create_string()
            params = {
                "newClientOrderId": self.clientId,
                'reduceOnly': True
            }
            if float(position) > 0:
                print("Closing Long Position")
                order = self.exchange.create_order(symbol, 'MARKET', 'SELL', float(position), params=params)
                return self._extract_order_info(order)
            elif float(position) < 0:
                print("Closing Short Position")
                order = self.exchange.create_order(symbol, 'MARKET', 'BUY', -float(position), params=params)
                return self._extract_order_info(order)
            else:
                print("No position to close.")
        except Exception as e:
            print(f"Error closing position: {e}")

    def run(self, data):
        close_position = data.get('close_position', 'False')
        print(close_position)
        order_results = []
        if close_position == 'True':
            print("Closing Position")
            result = self.close_position(symbol=data['symbol'])
            order_results.append(result)
        else:
            if 'cancel_orders' in data:
                print("Cancelling Order")
                try:
                    cancel_result = self.exchange.cancel_all_orders(symbol=data['symbol'])
                    order_results.append(cancel_result)
                except Exception as e:
                    print(f"Error cancelling orders: {e}")
                    order_results.append({'error': str(e)})
            if 'type' in data:
                print("Placing Order")
                price = data.get('price', 0)
                if 'usd_value' in data:
                    qty = self.calculate_qty(data['symbol'], data['usd_value'])
                else:
                    qty = float(data['qty'])
                try:
                    if data['order_mode'] == 'Both':
                        take_profit_percent = float(data['take_profit_percent']) / 100
                        stop_loss_percent = float(data['stop_loss_percent']) / 100
                        current_price = self.exchange.fetch_ticker(data['symbol'])['last']
                        if data['side'] == 'Buy':
                            take_profit_price = round(float(current_price) + (float(current_price) * take_profit_percent), 2)
                            stop_loss_price = round(float(current_price) - (float(current_price) * stop_loss_percent), 2)
                        elif data['side'] == 'Sell':
                            take_profit_price = round(float(current_price) - (float(current_price) * take_profit_percent), 2)
                            stop_loss_price = round(float(current_price) + (float(current_price) * stop_loss_percent), 2)
                        print("Take Profit Price: " + str(take_profit_price))
                        print("Stop Loss Price: " + str(stop_loss_price))
                        self.create_string()
                        params = {
                            "newClientOrderId": self.clientId,
                            'reduceOnly': False
                        }
                        if data['type'] == 'Limit':
                            order = self.exchange.create_order(data['symbol'], data['type'], data['side'], qty, price=float(price), params=params)
                        else:
                            order = self.exchange.create_order(data['symbol'], data['type'], data['side'], qty, params=params)
                        order_results.append(self._extract_order_info(order))
                        # Set risk orders
                        risk_results = self.set_risk(data['symbol'], data, stop_loss_price, take_profit_price)
                        if risk_results:
                            order_results.extend(risk_results)
                    elif data['order_mode'] == 'Profit':
                        take_profit_percent = float(data['take_profit_percent']) / 100
                        current_price = self.exchange.fetch_ticker(data['symbol'])['last']
                        if data['side'] == 'Buy':
                            take_profit_price = round(float(current_price) + (float(current_price) * take_profit_percent), 2)
                        elif data['side'] == 'Sell':
                            take_profit_price = round(float(current_price) - (float(current_price) * take_profit_percent), 2)
                        print("Take Profit Price: " + str(take_profit_price))
                        self.create_string()
                        params = {
                            "newClientOrderId": self.clientId,
                            'reduceOnly': False
                        }
                        if data['type'] == 'Limit':
                            order = self.exchange.create_order(data['symbol'], data['type'], data['side'], qty, price=float(price), params=params)
                        else:
                            order = self.exchange.create_order(data['symbol'], data['type'], data['side'], qty, params=params)
                        order_results.append(self._extract_order_info(order))
                        risk_results = self.set_risk(data['symbol'], data, 0, take_profit_price)
                        if risk_results:
                            order_results.extend(risk_results)
                    elif data['order_mode'] == 'Stop':
                        stop_loss_percent = float(data['stop_loss_percent']) / 100
                        current_price = self.exchange.fetch_ticker(data['symbol'])['last']
                        if data['side'] == 'Buy':
                            stop_loss_price = round(float(current_price) - (float(current_price) * stop_loss_percent), 2)
                        elif data['side'] == 'Sell':
                            stop_loss_price = round(float(current_price) + (float(current_price) * stop_loss_percent), 2)
                        print("Stop Loss Price: " + str(stop_loss_price))
                        self.create_string()
                        params = {
                            "newClientOrderId": self.clientId,
                            'reduceOnly': False
                        }
                        if data['type'] == 'Limit':
                            order = self.exchange.create_order(data['symbol'], data['type'], data['side'], qty, price=float(price), params=params)
                        else:
                            order = self.exchange.create_order(data['symbol'], data['type'], data['side'], qty, params=params)
                        order_results.append(self._extract_order_info(order))
                        risk_results = self.set_risk(data['symbol'], data, stop_loss_price, 0)
                        if risk_results:
                            order_results.extend(risk_results)
                    else:
                        order_results.append({'status': 'error'})
                except Exception as e:
                    print(f"Error placing order: {e}")
                    order_results.append({'error': str(e)})
        return order_results

    def set_risk(self, symbol, data, stop_loss, take_profit):
        results = []
        try:
            position = self.exchange.fetch_positions(symbol)
            if not position:
                print("No open position for risk management.")
                return results
            size = abs(float(position[0]['info']['positionAmt']))
            if data['order_mode'] == 'Both':
                if data['side'] == 'Buy':
                    self.create_string()
                    order1 = self.exchange.create_order(symbol, 'STOP_MARKET', 'SELL', size, params={
                        "newClientOrderId": self.clientId,
                        'reduceOnly': True,
                        'stopPrice': stop_loss,
                    })
                    results.append(self._extract_order_info(order1))
                    self.create_string()
                    order2 = self.exchange.create_order(symbol, 'TAKE_PROFIT_MARKET', 'SELL', size, params={
                        "newClientOrderId": self.clientId,
                        'reduceOnly': True,
                        'stopPrice': take_profit,
                    })
                    results.append(self._extract_order_info(order2))
                else:
                    self.create_string()
                    order1 = self.exchange.create_order(symbol, 'STOP_MARKET', 'BUY', size, params={
                        "newClientOrderId": self.clientId,
                        'reduceOnly': True,
                        'stopPrice': stop_loss,
                    })
                    results.append(self._extract_order_info(order1))
                    self.create_string()
                    order2 = self.exchange.create_order(symbol, 'TAKE_PROFIT_MARKET', 'BUY', size, params={
                        "newClientOrderId": self.clientId,
                        'reduceOnly': True,
                        'stopPrice': take_profit,
                    })
                    results.append(self._extract_order_info(order2))
            elif data['order_mode'] == 'Profit':
                if data['side'] == 'Buy':
                    self.create_string()
                    order = self.exchange.create_order(symbol, 'TAKE_PROFIT_MARKET', 'SELL', size, params={
                        "newClientOrderId": self.clientId,
                        'reduceOnly': True,
                        'stopPrice': take_profit,
                    })
                    results.append(self._extract_order_info(order))
                else:
                    self.create_string()
                    order = self.exchange.create_order(symbol, 'TAKE_PROFIT_MARKET', 'BUY', size, params={
                        "newClientOrderId": self.clientId,
                        'reduceOnly': True,
                        'stopPrice': take_profit,
                    })
                    results.append(self._extract_order_info(order))
            elif data['order_mode'] == 'Stop':
                if data['side'] == 'Buy':
                    self.create_string()
                    order = self.exchange.create_order(symbol, 'STOP_MARKET', 'SELL', size, params={
                        "newClientOrderId": self.clientId,
                        'reduceOnly': True,
                        'stopPrice': stop_loss,
                    })
                    results.append(self._extract_order_info(order))
                else:
                    self.create_string()
                    order = self.exchange.create_order(symbol, 'STOP_MARKET', 'BUY', size, params={
                        "newClientOrderId": self.clientId,
                        'reduceOnly': True,
                        'stopPrice': stop_loss,
                    })
                    results.append(self._extract_order_info(order))
        except Exception as e:
            print(f"Error in set_risk: {e}")
            results.append({'error': str(e)})
        return results

    def _extract_order_info(self, order):
        # Extract order id and status from the order response
        return {
            'order_id': order.get('id'),
            'status': order.get('status'),
            'info': order.get('info', {})
        }

    def get_balance(self, asset='USDT'):
        try:
            balance = self.exchange.fetch_balance()
            futures_balance = balance['total']
            if asset in futures_balance:
                print(f"{asset} Balance: {futures_balance[asset]}")
                return futures_balance[asset]
            else:
                print(f"{asset} not found in account balance.")
                return 0
        except Exception as e:
            print(f"Error fetching balance: {e}")
            return 0

    def get_full_balance(self):
        try:
            balance = self.exchange.fetch_balance()
            print(json.dumps(balance, indent=4))
            return balance
        except Exception as e:
            print(f"Error fetching full balance: {e}")
            return {}
