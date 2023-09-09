from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
	MessageEvent, PostbackEvent,
	TextMessage, TextSendMessage, ImageSendMessage, TemplateSendMessage, FlexSendMessage,
	ButtonsTemplate, 
	MessageTemplateAction
)
import json
import configparser
import datetime

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))


# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
	signature = request.headers['X-Line-Signature']

	body = request.get_data(as_text=True)
	app.logger.info("Request body: " + body)

	#print(body)

	try:
		handler.handle(body, signature)
	except InvalidSignatureError:
		abort(400)

	return 'OK'





# 學你說話
@handler.add(MessageEvent, message=TextMessage)
def echo(event):
	userid = event.source.user_id
	date_today = str(datetime.date.today())
	userid_date = userid + date_today

	if userid != "Udeadbeefdeadbeefdeadbeefdeadbeef":

		#print(event)
		company = event.message.text
		
		print(company)
		print(company[0:3])
		print(company[3:7])


		if (company[0:4] == "Menu"):
			company = company[4:8]

			FlexMessage = json.load(open('menu.json','r',encoding='utf-8'))
			#print(FlexMessage)
			for i in range(2):
				for j in range(3):

					FlexMessage['footer']['contents'][i]['contents'][j]['action']['displayText'] = FlexMessage['footer']['contents'][i]['contents'][j]['action']['displayText'] + company
					FlexMessage['footer']['contents'][i]['contents'][j]['action']['data'] = FlexMessage['footer']['contents'][i]['contents'][j]['action']['data'] + company

			print(FlexMessage)
			
			line_bot_api.reply_message(
				event.reply_token,
				FlexSendMessage('Financial_indicator', FlexMessage)
			)

		else:
			if (company[0:3] == "Div"):
			
				company = company[3:7]
				
				print(company)

				from finfunc import cs_dividends

				cs_dividends(company, userid_date)

			elif(company[0:3] == "Rev"):

				company = company[3:7]

				print(company)

				from finfunc import revenues

				revenues(company, userid_date)
				
			elif(company[0:3] == "Eps"):
				
				company = company[3:7]

				print(company)

				from finfunc import earnings_per_share

				earnings_per_share(company, userid_date)

			elif(company[0:3] == "Sha"):

				company = company[3:7]

				print(company)

				from finfunc import shareholding_ratio

				shareholding_ratio(company, userid_date)

			elif(company[0:3] == "Cqr"):
				company = company[3:7]

				print(company)

				from finfunc import current_quick_ratio

				current_quick_ratio(company, userid_date)

			elif(company[0:3] == "Gpm"):
				company = company[3:7]

				print(company)

				from finfunc import gross_profit_margin

				gross_profit_margin(company, userid_date)

			elif(company[0:3] == "Tie"):
				company = company[3:7]

				print(company)

				from finfunc import times_interest_earned

				times_interest_earned(company, userid_date)

			elif(company[0:3] == "Ccc"):
				company = company[3:7]

				print(company)

				from finfunc import cash_conversion_cycle

				cash_conversion_cycle(company, userid_date)

			else:
				print("NO")

			
			import pyimgur

			PATH1 = './' + userid_date + 'test.png'
			#if (os.path.exists(PATH1)) :
				
			CLIENT_ID = "b2412257c9cc4c5"
			PATH = userid_date + "test.png" #A Filepath to an image on your computer"
			title = "Uploaded with PyImgur"
			im = pyimgur.Imgur(CLIENT_ID)
			uploaded_image = im.upload_image(PATH, title=title)
			
			print(uploaded_image.title)
			print(uploaded_image.link)
			print(uploaded_image.type)

			os.remove(PATH1)

			line_bot_api.reply_message(
				event.reply_token,
				ImageSendMessage(
					original_content_url=uploaded_image.link,
					preview_image_url=uploaded_image.link
				)
			)

@handler.add(PostbackEvent)
def handle_Postback(event):
	#print(event)
	userid = event.source.user_id
	date_today = str(datetime.date.today())
	userid_date = userid + date_today

	company = event.postback.data
	print(company)
	print(company[0:3])
	print(company[3:7])

	if (company[0:3] == "Div"):
			
		company = company[3:7]
		
		print(company)

		from finfunc import cs_dividends

		cs_dividends(company, userid_date)

	elif(company[0:3] == "Rev"):

		company = company[3:7]

		print(company)

		from finfunc import revenues

		revenues(company, userid_date)
		
	elif(company[0:3] == "Eps"):
		
		company = company[3:7]

		print(company)

		from finfunc import earnings_per_share

		earnings_per_share(company, userid_date)

	elif(company[0:3] == "Sha"):

		company = company[3:7]

		print(company)

		from finfunc import shareholding_ratio

		shareholding_ratio(company, userid_date)

	elif(company[0:3] == "Cqr"):
		company = company[3:7]

		print(company)

		from finfunc import current_quick_ratio

		current_quick_ratio(company, userid_date)

	elif(company[0:3] == "Gpm"):
		company = company[3:7]

		print(company)

		from finfunc import gross_profit_margin

		gross_profit_margin(company, userid_date)

	elif(company[0:3] == "Tie"):
		company = company[3:7]

		print(company)

		from finfunc import times_interest_earned

		times_interest_earned(company, userid_date)

	elif(company[0:3] == "Ccc"):
		company = company[3:7]

		print(company)

		from finfunc import cash_conversion_cycle

		cash_conversion_cycle(company, userid_date)
		
	else:
		print("NO")

	
	import pyimgur

	PATH1 = './' + userid_date + 'test.png'
	#if (os.path.exists(PATH1)) :
	
	CLIENT_ID = "b2412257c9cc4c5"
	PATH = userid_date + "test.png" #A Filepath to an image on your computer"
	title = "Uploaded with PyImgur"
	im = pyimgur.Imgur(CLIENT_ID)
	uploaded_image = im.upload_image(PATH, title=title)
	
	print(uploaded_image.title)
	print(uploaded_image.link)
	print(uploaded_image.type)

	os.remove(PATH1)

	line_bot_api.reply_message(
		event.reply_token,
		ImageSendMessage(
			original_content_url=uploaded_image.link,
			preview_image_url=uploaded_image.link
		)
	)

	# FlexMessage = json.load(open('menu.json','r',encoding='utf-8'))
	# print(FlexMessage)
	# for i in range(1):
	# 	for j in range(2):

	# 		FlexMessage['footer']['contents'][i]['contents'][j]['action']['displayText'] = FlexMessage['footer']['contents'][i]['contents'][j]['action']['displayText'] + company
	# 		FlexMessage['footer']['contents'][i]['contents'][j]['action']['data'] = FlexMessage['footer']['contents'][i]['contents'][j]['action']['data'] + company



if __name__ == "__main__":
	app.run()