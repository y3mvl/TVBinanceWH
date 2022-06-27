This is a tradingview webhook  designed to be free & open source.  This bot is written using Python & Flask and is designed to run a free heroku server. It will allow you to create custom alerts in tradingview and send them to your own private webhook server that can place trades on your account via the api.

#### Current Exchanges 
- [Bybit](https://partner.bybit.com/b/webhookbot)
- More will be done on request or can be added by submitting a pull request.

***Help keep this tool free by creating a new account using our referral below:***

[Create Bybit Account](https://partner.bybit.com/b/webhookbot)


# How to Webhook Server on Heroku

1.) Clone Project to Desktop

2.) [Create Free Heroku Account](https://www.heroku.com/)

3.) Edit config.json to add your own api keys & add a custom key to protect the server.

```You need to creat new keys on Bybit & give them the correct acess to trade and see token balance```
	
4.) Open a terminal in the cloned directory:


 5.) Submit the following lines into the terminal and press ENTER after each one to procces the code: 
 
``git init``

``heroku login``

``heroku create --region eu tv-trader-yourservernamehere``

``git add .``

``git commit -m "Initial Commit"``

``git push heroku master``


***Anytime you need to make a change to the code or the API keys, you can push a new build to Heroku:***

``git add .``

``git commit -m "Update"``

``git push heroku master``

# How to send alerts from TradingView to your new Webserver

After starting you server, you shoudl see an address that will allow you to access it like below:

[https://tv-trader-gnome.herokuapp.com/](https://tv-trader-gnome.herokuapp.com/webhook)

#### You will want to add this when you create a new alert like show below:

![image](https://user-images.githubusercontent.com/33667144/176002365-be54dfdc-690a-433d-9702-e8e9641a45b5.png)

#### You will then want to create you syntax based on the format shownb below and place it in the alert msg field

![image](https://user-images.githubusercontent.com/33667144/176003033-26794889-e041-4737-83f1-4f850335f280.png)


_Now when your alerts fire off they should go strait to your server and get proccessed on the exchange almost instantly!_


# TradingView Alerts Format 

```
{
	"key": "678777",
	"exchange": "bybit",
	"symbol": "ETHUSD",
	"type": "Market",
	"side": "Buy",
	"qty": "1",
	"price": "1120",
	"close_position": "False",
	"cancel_orders": "True",
	"order_mode": "Both",
	"take_profit_percent": "1",
	"stop_loss_percent": "0.5"
}
```



---
| Constant |Settings Keys  |
|--|--|
|key| unique key that protects your webhook server
|exchange  | bybit, more coming soon. |
|symbol  | "BTCUSD" for Inverse Pairs && "BTCUSDT" for USDT Perpetual Pairs |
|side	|Buy or Sell		|
|type | Market or Limit		|
|order_mode	 | Both, Profit, Stop 		|
|qty	 | amount of base currency to buy 		|
|price	 |  ticker in quote currency		|
|close_position	 | True or False 		|
|cancel_orders	 |True or False 		|
|take_profit_percent| any float	 (0.5)	|
|stop_loss_Percent	 |and float (0.5)		|



