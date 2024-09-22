Config.py:

  BYBIT_ENABLED=os.environ.get("BYBIT_ENABLED")
  BYBIT_API_KEY=os.environ.get("BYBIT_API_KEY")
  BYBIT_API_SECRET=os.environ.get("BYBIT_API_SECRET")

app.py:
  import pybit
############
  use_bybit = False
  if config.BYBIT_ENABLED:
    print("Bybit is enabled!")
    use_bybit = True

    session = HTTP(
        endpoint='https://api.bybit.com',
        api_key=config.BYBIT_API_KEY,
        api_secret=config.BYBIT_API_SECRET
    )
############
  ##############################################################################
  #             Bybit ## MOVE THIS CODE TO NEW FILE
  ##############################################################################
  if data['exchange'] == 'bybit':

      if use_bybit:
          if data['close_position'] == 'True':
              print("Closing Position")
              session.close_position(symbol=data['symbol'])
          else:
              if 'cancel_orders' in data:
                  print("Cancelling Order")
                  session.cancel_all_active_orders(symbol=data['symbol'])
              if 'type' in data:
                  print("Placing Order")
                  if 'price' in data:
                      price = data['price']
                  else:
                      price = 0


                  if data['order_mode'] == 'Both':
                      take_profit_percent = float(data['take_profit_percent'])/100
                      stop_loss_percent = float(data['stop_loss_percent'])/100
                      current_price = session.latest_information_for_symbol(symbol=data['symbol'])['result'][0]['last_price']
                      if data['side'] == 'Buy':
                          take_profit_price = round(float(current_price) + (float(current_price) * take_profit_percent), 2)
                          stop_loss_price = round(float(current_price) - (float(current_price) * stop_loss_percent), 2)
                      elif data['side'] == 'Sell':
                          take_profit_price = round(float(current_price) - (float(current_price) * take_profit_percent), 2)
                          stop_loss_price = round(float(current_price) + (float(current_price) * stop_loss_percent), 2)


                      print("Take Profit Price: " + str(take_profit_price))
                      print("Stop Loss Price: " + str(stop_loss_price))

                      session.place_active_order(symbol=data['symbol'], order_type=data['type'], side=data['side'],
                                                  qty=data['qty'], time_in_force="GoodTillCancel", reduce_only=False,
                                                  close_on_trigger=False, price=price, take_profit=take_profit_price, stop_loss=stop_loss_price)

                  elif data['order_mode'] == 'Profit':
                      take_profit_percent = float(data['take_profit_percent'])/100
                      current_price = session.latest_information_for_symbol(symbol=data['symbol'])['result'][0]['last_price']
                      if data['side'] == 'Buy':
                          take_profit_price = round(float(current_price) + (float(current_price) * take_profit_percent), 2)
                      elif data['side'] == 'Sell':
                          take_profit_price = round(float(current_price) - (float(current_price) * take_profit_percent), 2)

                      print("Take Profit Price: " + str(take_profit_price))
                      session.place_active_order(symbol=data['symbol'], order_type=data['type'], side=data['side'],
                                                  qty=data['qty'], time_in_force="GoodTillCancel", reduce_only=False,
                                                  close_on_trigger=False, price=price, take_profit=take_profit_price)
                  elif data['order_mode'] == 'Stop':
                      stop_loss_percent = float(data['stop_loss_percent'])/100
                      current_price = session.latest_information_for_symbol(symbol=data['symbol'])['result'][0]['last_price']
                      if data['side'] == 'Buy':
                          stop_loss_price = round(float(current_price) - (float(current_price) * stop_loss_percent), 2)
                      elif data['side'] == 'Sell':
                          stop_loss_price = round(float(current_price) + (float(current_price) * stop_loss_percent), 2)

                      print("Stop Loss Price: " + str(stop_loss_price))
                      session.place_active_order(symbol=data['symbol'], order_type=data['type'], side=data['side'],
                                                  qty=data['qty'], time_in_force="GoodTillCancel", reduce_only=False,
                                                  close_on_trigger=False, price=price, stop_loss=stop_loss_price)



                  else:
                      session.place_active_order(symbol=data['symbol'], order_type=data['type'], side=data['side'],
                                                  qty=data['qty'], time_in_force="GoodTillCancel", reduce_only=False,
                                                  close_on_trigger=False, price=price)


      return {
          "status": "success",
          "message": "Bybit Webhook Received!"
      }
