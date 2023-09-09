import requests as rq
from bs4 import BeautifulSoup
import io
import re

import pandas as pd
import matplotlib.pyplot as plt

def cs_dividends(company, userid_date):
	nextlink = "https://goodinfo.tw/StockInfo/StockDividendPolicy.asp?STOCK_ID="+ str(company)
	headers = {
		"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
	}

	#print(nextlink)
	nl_response = rq.get(nextlink, headers = headers) # 用 requests 的 get 方法把網頁抓下來

	nl_response.encoding = 'utf-8'
	#print(nl_response.text)

	soup = BeautifulSoup(nl_response.text, "lxml") # 指定 lxml 作為解析器

	dividends = soup.find_all('tr', attrs={'bgcolor':['#ffffff', '#f0f0f0'], 'align':'center'})


	#print(dividends[0])
	#print(dividends[1])

	year = []
	cash_dividend = []
	stock_dividend = []

	for i in range(10):
		list_dividends = list(dividends[i])
		every_year = str(list_dividends[1])
		every_year = re.sub('\S*'+'<b>', "" , every_year)
		every_year = re.sub('</b>'+'\S*', "" , every_year)
		#print(every_year)
		if (every_year == "累計"):
			break
		else:
			year.append(every_year)
		
		#print(list_dividends[7])
		cash = re.sub('\s*', "" ,str(list_dividends[7]))
		cash = re.sub('\S*'+'\"'+'>', "" ,cash)[0:-5:]
		if(cash == '-'):
			cash = 0
		else:
			cash = float(cash)
		cash_dividend.append(cash)
		
		
		#print(list_dividends[13])
		stock = re.sub('\s*', "" ,str(list_dividends[13]))
		stock = re.sub('\S*'+'\"'+'>', "" , stock)[0:-5:]
		if(stock == '-'):
			stock = 0
		else:
			stock = float(stock)
		stock_dividend.append(stock)
		
		
		
		
	#print(year)
	#print(cash_dividend)
	#print(stock_dividend)


	#for i in range(len(cash_dividend)):
		#cash_dividend[i] = float(cash_dividend[i])
		#stock_dividend[i] = float(stock_dividend[i])

	year.reverse()
	cash_dividend.reverse()
	stock_dividend.reverse()

	#print(year)
	#print(cash_dividend)
	#print(stock_dividend)


	plt.bar(year, cash_dividend, color='blue', label='Cash_Dividend')
	plt.bar(year, stock_dividend, color='green', label='Stock_Dividend', bottom=cash_dividend)

	plt.xlabel('Year')
	plt.ylabel('Dividend')
	plt.legend()
	plt.title(str(company) + '-Dividend')

	plt.savefig(userid_date + 'test')
	plt.show()
	plt.close()

def revenues(company, userid_date):
	nextlink = "https://goodinfo.tw/StockInfo/ShowSaleMonChart.asp?STOCK_ID="+ str(company)
	headers = {
		"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
	}

	#print(nextlink)
	nl_response = rq.get(nextlink, headers = headers) # 用 requests 的 get 方法把網頁抓下來

	nl_response.encoding = 'utf-8'
	#print(nl_response.text)

	soup = BeautifulSoup(nl_response.text, "lxml") # 指定 lxml 作為解析器

	#revenue = soup.find_all('table', attrs={'class':'b1 p4_2 r0_10 row_bg_2n row_mouse_over', 'style':'width:100%;font-size:10pt;line-height:17px;'})

	revenue1 = soup.select("table tr")

	month = []
	revenue_list = []
	price_list = []

	#a= list(revenue[88])
	#str(a[1])[10:17]

	for i in range(88,106):
	
		#print(i)
		#print(revenue1[i])
	
		month.append(str(list(revenue1[i])[1])[12:17])
	
		monthly_revenue = str(list(revenue1[i])[15])
		monthly_revenue = monthly_revenue.replace(',', '')
		monthly_revenue = re.sub('\s*', "" , monthly_revenue)
		monthly_revenue = re.sub('\S*'+'<nobr>', "" , monthly_revenue)[0:-12]
		revenue_list.append(monthly_revenue)

		price = str(list(revenue1[i])[5])
		price = re.sub('\S*'+'<nobr>', "" , price)[0:-12]
		price = re.sub('</nobr>'+'\S*', "" , price)
		price_list.append(price)

	for i in range(110,116):

		#print(i)
		#print(revenue[i])
	
		month.append(str(list(revenue1[i])[1])[12:17])
	
		monthly_revenue = str(list(revenue1[i])[15])
		monthly_revenue = monthly_revenue.replace(',', '')
		monthly_revenue = re.sub('\s*', "" , monthly_revenue)
		monthly_revenue = re.sub('\S*'+'<nobr>', "" , monthly_revenue)[0:-12]
		revenue_list.append(monthly_revenue)

		price = str(list(revenue1[i])[5])
		price = re.sub('\S*'+'<nobr>', "" , price)[0:-12]
		price = re.sub('</nobr>'+'\S*', "" , price)
		price_list.append(price)


	for i in range(len(revenue_list)):
		revenue_list[i] = float(revenue_list[i])
		price_list[i] = float(price_list[i])
	
	month.reverse()
	revenue_list.reverse()
	price_list.reverse()

	#print(month)
	#print(revenue_list)
	#print(price_list)


	fig = plt.figure(figsize=(12,6))

	fig, ax=plt.subplots(figsize = (12, 6))

	ax.bar(month, revenue_list, color='#FFE153', label='Revenue')
	ax.set_xlabel("Month")
	ax.set_ylabel("Revenue")


	plt.xticks(rotation = 30)

	ax1 = ax.twinx()
	ax1.plot(month, price_list, color='red', label='Stock_Price')
	ax1.set_ylabel("Stock_Price")

	#handles, labels = ax.get_legend_handles_labels()
	#ax1.legend(handles, labels)

	lines, labels = ax.get_legend_handles_labels()
	lines1, labels1 = ax1.get_legend_handles_labels()
	ax1.legend(lines + lines1, labels + labels1)

	fig.suptitle(str(company) + '-Revenue')

	plt.savefig(userid_date + 'test')
	plt.show()
	plt.close()

def earnings_per_share(company, userid_date):
	nextlink = "https://goodinfo.tw/StockInfo/StockFinDetail.asp?RPT_CAT=IS_M_QUAR&STOCK_ID=" + str(company)
	headers = {
		"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
	}

	#print(nextlink)
	nl_response = rq.get(nextlink, headers = headers) # 用 requests 的 get 方法把網頁抓下來

	nl_response.encoding = 'utf-8'
	#print(nl_response.text)

	soup = BeautifulSoup(nl_response.text, "lxml") # 指定 lxml 作為解析器

	eps_data = soup.select("table tr td")


	eps_data.pop(68)

	quarter_index = [i for i in eps_data if "業外損益" in str(i)]
	qi = eps_data.index(quarter_index[0])

	eps_index = [i for i in eps_data if "每股稅後盈餘(元)" in str(i)]
	epsi = eps_data.index(eps_index[0])

	print(qi)
	print(epsi)

	quarter_list = []
	eps_list = []

	for i in range(qi + 1, qi + 8, 1):
		print(eps_data[i])
	
		quarter_data = str(eps_data[i])
		quarter_data = re.sub('\s*', "" , quarter_data)
		quarter_data = re.sub('\S*'+'<nobr>', "" , quarter_data)
		quarter_data = re.sub('</nobr>'+'\S*', "" , quarter_data)
		#quarter_data = float(quarter_data)
		
		print(quarter_data)
		quarter_list.append(quarter_data)
	
	for j in range(epsi + 1, epsi + 15, 2):
		print(eps_data[j])
		
		eps_value = str(eps_data[j])
		eps_value = re.sub('\s*', "" , eps_value)
		eps_value = re.sub('\S*'+'<nobr>', "" , eps_value)
		eps_value = re.sub('</nobr>'+'\S*', "" , eps_value)
		eps_value = float(eps_value)
		
		eps_list.append(eps_value)

	if (quarter_list[6][-1] == "1"):
		qrytime = int(quarter_list[6][0:4]) - 1
		qrytime = str(qrytime) + "4"
	else:
		qrytime = int(quarter_list[6][-1]) - 1
		qrytime = quarter_list[6][0:4] + str(qrytime)


	nextlink = "https://goodinfo.tw/StockInfo/StockFinDetail.asp?RPT_CAT=IS_M_QUAR&STOCK_ID=" + str(company) + "&QRY_TIME=" + qrytime
	headers = {
		"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
	}

	#print(nextlink)
	nl_response = rq.get(nextlink, headers = headers) # 用 requests 的 get 方法把網頁抓下來

	nl_response.encoding = 'utf-8'
	#print(nl_response.text)

	soup = BeautifulSoup(nl_response.text, "lxml") # 指定 lxml 作為解析器

	eps_data = soup.select("table tr td")

	eps_data.pop(68)

	quarter_index = [i for i in eps_data if "業外損益" in str(i)]
	qi = eps_data.index(quarter_index[0])

	eps_index = [i for i in eps_data if "每股稅後盈餘(元)" in str(i)]
	epsi = eps_data.index(eps_index[0])

	print(qi)
	print(epsi)

	for i in range(qi + 1, qi + 8, 1):
		print(eps_data[i])

		quarter_data = str(eps_data[i])
		quarter_data = re.sub('\s*', "" , quarter_data)
		quarter_data = re.sub('\S*'+'<nobr>', "" , quarter_data)
		quarter_data = re.sub('</nobr>'+'\S*', "" , quarter_data)
		#quarter_data = float(quarter_data)

		print(quarter_data)
		quarter_list.append(quarter_data)

	for j in range(epsi + 1, epsi + 15, 2):
		print(eps_data[j])

		eps_value = str(eps_data[j])
		eps_value = re.sub('\s*', "" , eps_value)
		eps_value = re.sub('\S*'+'<nobr>', "" , eps_value)
		eps_value = re.sub('</nobr>'+'\S*', "" , eps_value)
		eps_value = float(eps_value)

		eps_list.append(eps_value)

	quarter_list.reverse()
	eps_list.reverse()

	print(quarter_list)
	print(eps_list)

	plt.bar(quarter_list, eps_list, color='#FFA042', label='EPS')
	
	plt.xticks(rotation = 30)

	plt.xlabel('Quarter')
	plt.ylabel('EPS')
	plt.title(str(company) + '-EPS')

	plt.savefig(userid_date + 'test')
	plt.show()
	plt.close()

def shareholding_ratio(company, userid_date):
	nextlink = "https://goodinfo.tw/StockInfo/EquityDistributionCatHis.asp?STOCK_ID="+ str(company)
	headers = {
		"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
	}

	#print(nextlink)
	nl_response = rq.get(nextlink, headers = headers) # 用 requests 的 get 方法把網頁抓下來

	nl_response.encoding = 'utf-8'
	print(nl_response.text)

	soup = BeautifulSoup(nl_response.text, "lxml") # 指定 lxml 作為解析器

	#dividends = soup.find_all('tr', attrs={'bgcolor':['#ffffff', '#f0f0f0'], 'align':'center'})

	structure = soup.select("table tr td")

	structure_data = structure[67].select("table tr td")

	if ("期貨標的" in str(structure_data[3])):
		#print("YYYYYYYYYYY")
		structure_data.pop(3)
	
	if ("選擇權標的" in str(structure_data[3])):
		#print("YYYYYYYYYYY")
	 	structure_data.pop(3)
	    
	if ("權證標的" in str(structure_data[3])):
		#print("YYYYYYYYYYY")
		structure_data.pop(3)


	gov_shareholding = str(structure_data[91])
	gov_shareholding = re.sub('\S*'+'<nobr>', "" , gov_shareholding)
	gov_shareholding = re.sub('</nobr>'+'\S*', "" , gov_shareholding)
	gov_shareholding = float(gov_shareholding)


	foreign_investment = str(structure_data[96])
	foreign_investment = re.sub('\S*'+'<nobr>', "" , foreign_investment)
	foreign_investment = re.sub('</nobr>'+'\S*', "" , foreign_investment)
	foreign_investment = float(foreign_investment)


	fin_institution = str(structure_data[99])
	fin_institution = re.sub('\S*'+'<nobr>', "" , fin_institution)
	fin_institution = re.sub('</nobr>'+'\S*', "" , fin_institution)
	fin_institution = float(fin_institution)


	juridical_person = str(structure_data[102])
	juridical_person = re.sub('\S*'+'<nobr>', "" , juridical_person)
	juridical_person = re.sub('</nobr>'+'\S*', "" , juridical_person)
	juridical_person = float(juridical_person)


	natural_person = str(structure_data[103])
	natural_person = re.sub('\S*'+'<nobr>', "" , natural_person)
	natural_person = re.sub('</nobr>'+'\S*', "" , natural_person)
	natural_person = float(natural_person)

	
	kind = ['gov_shareholding', 'foreign_investment', 'fin_institution', 'juridical_person', 'natural_person']
	shareholding_structure = [gov_shareholding, foreign_investment, fin_institution, juridical_person, natural_person]


	treasury_stock = str(structure_data[104])
	treasury_stock = re.sub('\S*'+'<nobr>', "" , treasury_stock)
	treasury_stock = re.sub('</nobr>'+'\S*', "" , treasury_stock)
	treasury_stock = float(treasury_stock)

	if (treasury_stock != 0):
		kind.append('treasury_stock')
		shareholding_structure.append(treasury_stock)
	

	fig = plt.figure(figsize=(12,6))

	plt.pie(shareholding_structure, labels = kind)

	plt.axis('equal')
	plt.title(str(company) + '-Shareholding Structure')
	plt.legend()


	plt.savefig(userid_date + 'test')
	plt.show()
	plt.close()

def current_quick_ratio(company, userid_date):
	nextlink = "https://goodinfo.tw/StockInfo/StockFinDetail.asp?RPT_CAT=XX_M_QUAR&STOCK_ID="+ str(company)
	headers = {
		"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
	}

	#print(nextlink)
	nl_response = rq.get(nextlink, headers = headers) # 用 requests 的 get 方法把網頁抓下來

	nl_response.encoding = 'utf-8'
	#print(nl_response.text)

	soup = BeautifulSoup(nl_response.text, "lxml") # 指定 lxml 作為解析器

	ratio = soup.select("table tr td")

	ratio_data = ratio[67].select("table tr td")

	if ("期貨標的" in str(ratio_data[3])):
		#print("YYYYYYYYYYY")
		ratio_data.pop(3)
	
	if ("選擇權標的" in str(ratio_data[3])):
		#print("YYYYYYYYYYY")
		ratio_data.pop(3)
	
	if ("權證標的" in str(ratio_data[3])):
		#print("YYYYYYYYYYY")
		ratio_data.pop(3)

	#for i in range(len(ratio_data)):
		#print(i)
		#print(ratio_data[i])


	current_index = [i for i in ratio_data if "流動比" in str(i)]
	ci = ratio_data.index(current_index[0])

	quick_index = [i for i in ratio_data if "速動比" in str(i)]
	qi = ratio_data.index(quick_index[0])

	quarter_list = []
	quick_list = []
	current_list = []

	for i in range(61, 71, 1):
		quarter_list.append(str(ratio_data[i])[10:16])
	
		#print(str(ratio_data[i])[10:16])
	
	for j in range(qi + 1, qi + 11, 1):
		print(ratio_data[j])
		quick_data = str(ratio_data[j])
		quick_data = re.sub('\s*', "" , quick_data)
		quick_data = re.sub('\S*'+'<nobr>', "" , quick_data)
		quick_data = re.sub('</nobr>'+'\S*', "" , quick_data)
		quick_data = float(quick_data)
		quick_list.append(quick_data)
	
	for k in range(ci + 1, ci + 11, 1):
		current_data = str(ratio_data[k])
		current_data = re.sub('\s*', "" , current_data)
		current_data = re.sub('\S*'+'<nobr>', "" , current_data)
		current_data = re.sub('</nobr>'+'\S*', "" , current_data)
		current_data = float(current_data)
		current_list.append(current_data)
	
	quarter_list.reverse()
	quick_list.reverse()
	current_list.reverse()

	print(quarter_list)
	print(quick_list)
	print(current_list)

	plt.plot(quarter_list, current_list, 'o-', color = 'g', label="Current_Ratio")
	plt.plot(quarter_list, quick_list, 's-', color = 'r', label="Quick_Ratio")

	plt.xticks(rotation = 30)

	plt.xlabel('Quarter')
	plt.ylabel('Ratio')
	plt.title(str(company) + '-Current Ratio / Quick Ratio')

	plt.legend()

	plt.savefig(userid_date + 'test')
	plt.show()
	plt.close()

def gross_profit_margin(company, userid_date):
	nextlink = "https://goodinfo.tw/StockInfo/StockFinDetail.asp?RPT_CAT=IS_M_QUAR&STOCK_ID=" + str(company)
	headers = {
		"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
	}

	#print(nextlink)
	nl_response = rq.get(nextlink, headers = headers) # 用 requests 的 get 方法把網頁抓下來

	nl_response.encoding = 'utf-8'
	#print(nl_response.text)

	soup = BeautifulSoup(nl_response.text, "lxml") # 指定 lxml 作為解析器

	gross_profit = soup.select("table tr td")

	gross_profit.pop(68)

	quarter_index = [i for i in gross_profit if "業外損益" in str(i)]
	qi = gross_profit.index(quarter_index[0])

	gp_index = [i for i in gross_profit if "營業毛利" in str(i)]
	gpi = gross_profit.index(gp_index[0])

	quarter_list = []
	gp_list = []
	gpm_list = []

	for i in range(qi + 1, qi + 8, 1):
		#print(gross_profit[i])
	
		quarter_data = str(gross_profit[i])
		quarter_data = re.sub('\s*', "" , quarter_data)
		quarter_data = re.sub('\S*'+'<nobr>', "" , quarter_data)
		quarter_data = re.sub('</nobr>'+'\S*', "" , quarter_data)
	
		quarter_list.append(quarter_data)
	
	for j in range(gpi + 1, gpi + 15, 1):
		#print(gross_profit[j])
	
		gp_data = str(gross_profit[j])
		gp_data = re.sub('\S*'+'<nobr>', "" , gp_data)
		gp_data = re.sub('</nobr>'+'\S*', "" , gp_data)
		gp_data = float(gp_data)
	
		if ((j - gpi) % 2 == 1):
			gp_list.append(gp_data)
		else:
			gpm_list.append(gp_data)

	if (quarter_list[6][-1] == "1"):
		qrytime = int(quarter_list[6][0:4]) - 1
		qrytime = str(qrytime) + "4"
	else:
		qrytime = int(quarter_list[6][-1]) - 1
		qrytime = quarter_list[6][0:4] + str(qrytime)




	nextlink = "https://goodinfo.tw/StockInfo/StockFinDetail.asp?RPT_CAT=IS_M_QUAR&STOCK_ID=" + str(company) + "&QRY_TIME=" + qrytime
	headers = {
		"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
	}

	#print(nextlink)
	nl_response = rq.get(nextlink, headers = headers) # 用 requests 的 get 方法把網頁抓下來

	nl_response.encoding = 'utf-8'
	#print(nl_response.text)

	soup = BeautifulSoup(nl_response.text, "lxml") # 指定 lxml 作為解析器

	gross_profit = soup.select("table tr td")

	gross_profit.pop(68)

	quarter_index = [i for i in gross_profit if "業外損益" in str(i)]
	qi = gross_profit.index(quarter_index[0])

	gp_index = [i for i in gross_profit if "營業毛利" in str(i)]
	gpi = gross_profit.index(gp_index[0])


	for i in range(qi + 1, qi + 8, 1):
		#print(gross_profit[i])
	
		quarter_data = str(gross_profit[i])
		quarter_data = re.sub('\s*', "" , quarter_data)
		quarter_data = re.sub('\S*'+'<nobr>', "" , quarter_data)
		quarter_data = re.sub('</nobr>'+'\S*', "" , quarter_data)
		
		quarter_list.append(quarter_data)
	
	for j in range(gpi + 1, gpi + 15, 1):
		print(j)
		print(gross_profit[j])
		
		gp_data = str(gross_profit[j])
		gp_data = re.sub('\S*'+'<nobr>', "" , gp_data)
		gp_data = re.sub('</nobr>'+'\S*', "" , gp_data)
		gp_data = float(gp_data)
	
		if ((j - gpi) % 2 == 1):
			gp_list.append(gp_data)
		else:
			gpm_list.append(gp_data)


	quarter_list.reverse()
	gp_list.reverse()
	gpm_list.reverse()

	print(quarter_list)
	print(gp_list)
	print(gpm_list)

	fig = plt.figure(figsize=(12,6))

	fig, ax=plt.subplots(figsize = (12, 6))

	ax.bar(quarter_list, gp_list, color='#FFE153', label='Gross_Profit')
	ax.set_xlabel("Quarter")
	ax.set_ylabel("Gross_Profit")


	plt.xticks(rotation = 30)

	ax1 = ax.twinx()
	ax1.plot(quarter_list, gpm_list, color='red', label='Gross_Margin')
	ax1.set_ylabel("Gross_Margin(%)")

	#handles, labels = ax.get_legend_handles_labels()
	#ax1.legend(handles, labels)

	lines, labels = ax.get_legend_handles_labels()
	lines1, labels1 = ax1.get_legend_handles_labels()
	ax1.legend(lines + lines1, labels + labels1).get_frame().set_alpha(0.3)

	fig.suptitle(str(company) + '-Gross_Profit / Gross_Margin')

	plt.savefig(userid_date + 'test')
	plt.show()
	plt.close()

def times_interest_earned(company, userid_date):
	nextlink = "https://goodinfo.tw/StockInfo/StockFinDetail.asp?RPT_CAT=XX_M_QUAR&STOCK_ID="+ str(company)
	headers = {
		"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
	}

	#print(nextlink)
	nl_response = rq.get(nextlink, headers = headers) # 用 requests 的 get 方法把網頁抓下來

	nl_response.encoding = 'utf-8'
	#print(nl_response.text)

	soup = BeautifulSoup(nl_response.text, "lxml") # 指定 lxml 作為解析器

	#revenue = soup.find_all('table', attrs={'class':'b1 p4_2 r0_10 row_bg_2n row_mouse_over', 'style':'width:100%;font-size:10pt;line-height:17px;'})

	ratio = soup.select("table tr td")

	ratio.pop(67)

	quarter_index = [i for i in ratio if "償債能力" in str(i)]
	qi = ratio.index(quarter_index[0])

	tie_index = [i for i in ratio if "利息保障倍數" in str(i)]
	tiei = ratio.index(tie_index[0])

	quarter_list = []
	tie_list = []

	for i in range(qi + 1, qi + 11, 1):
		#print(ratio[i])
		quarter_data = str(ratio[i])
		quarter_data = re.sub('\S*'+'<nobr>', "" , quarter_data)
		quarter_data = re.sub('</nobr>'+'\S*', "" , quarter_data)
	
		quarter_list.append(quarter_data)
	
	for j in range(tiei + 1, tiei + 11, 1):
		#print(ratio[j])
		tie_data = str(ratio[j])
		tie_data = re.sub('\s*', "" , tie_data)
		tie_data = re.sub('\S*'+'<nobr>', "" , tie_data)
		tie_data = re.sub('</nobr>'+'\S*', "" , tie_data)
		tie_data = float(tie_data)
	
		tie_list.append(tie_data)
	
	quarter_list.reverse()
	tie_list.reverse()

	print(quarter_list)
	print(tie_list)

	plt.plot(quarter_list, tie_list, 'o-', color = '#FF5809', label="TIE")

	plt.xticks(rotation = 30)

	plt.xlabel('Quarter')
	plt.ylabel('TIE')
	plt.title(str(company) + '-TIE')

	plt.legend()

	plt.savefig(userid_date + 'test')
	plt.show()
	plt.close()

def cash_conversion_cycle(company, userid_date):
	nextlink = "https://goodinfo.tw/StockInfo/StockFinDetail.asp?RPT_CAT=XX_M_QUAR&STOCK_ID="+ str(company)
	headers = {
		"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
	}

	#print(nextlink)
	nl_response = rq.get(nextlink, headers = headers) # 用 requests 的 get 方法把網頁抓下來

	nl_response.encoding = 'utf-8'
	#print(nl_response.text)

	soup = BeautifulSoup(nl_response.text, "lxml") # 指定 lxml 作為解析器

	days = soup.select("table tr td")

	days.pop(67)

	quarter_index = [i for i in days if "經營能力" in str(i)]
	qi = days.index(quarter_index[0])

	rcp_index = [i for i in days if "應收款項收現日數" in str(i)]
	rcpi = days.index(rcp_index[0])

	pcp_index = [i for i in days if "應付款項付現日數" in str(i)]
	pcpi = days.index(pcp_index[0])

	icp_index = [i for i in days if "平均售貨日數" in str(i)]
	icpi = days.index(icp_index[0])

	print(rcpi)
	print(pcpi)
	print(icpi)

	quarter_list = []
	rcp_list = []#應收帳款收現天數
	pcp_list = []#應付帳款付現天數
	icp_list = []#存貨週轉天數

	for i in range(qi + 1, qi + 11, 1):
		quarter_list.append(str(days[i])[10:16])

	for j in range(rcpi + 1, rcpi + 11, 1):#應收帳款收現天數
		rcp_data = str(days[j])
		rcp_data = re.sub('\s*', "" , rcp_data)
		rcp_data = re.sub('\S*'+'<nobr>', "" , rcp_data)
		rcp_data = re.sub('</nobr>'+'\S*', "" , rcp_data)
		rcp_data = float(rcp_data)
		rcp_list.append(rcp_data)
	
	for k in range(pcpi + 1, pcpi + 11, 1):#應付帳款付現天數
		pcp_data = str(days[k])
		pcp_data = re.sub('\s*', "" , pcp_data)
		pcp_data = re.sub('\S*'+'<nobr>', "" , pcp_data)
		pcp_data = re.sub('</nobr>'+'\S*', "" , pcp_data)
		pcp_data = float(pcp_data)
		pcp_list.append(pcp_data)
	
	for l in range(icpi + 1, icpi + 11, 1):#存貨週轉天數
		icp_data = str(days[l])
		icp_data = re.sub('\s*', "" , icp_data)
		icp_data = re.sub('\S*'+'<nobr>', "" , icp_data)
		icp_data = re.sub('</nobr>'+'\S*', "" , icp_data)
		icp_data = float(icp_data)
		icp_list.append(icp_data)

	quarter_list.reverse()
	rcp_list.reverse()
	pcp_list.reverse()
	icp_list.reverse()

	ccc_list = [round((rcp_list[i] + icp_list[i] - pcp_list[i]), 2) for i in range(len(rcp_list))]

	#print(quarter_list)
	#print(rcp_list)
	#print(pcp_list)
	#print(icp_list)
	#print(ccc_list)

	fig = plt.figure(figsize=(12,5))

	plt.plot(quarter_list, rcp_list, 'o-', color = '#73BF00', label="Receivables conversion period")
	plt.plot(quarter_list, pcp_list, 's-', color = '#FFD306', label="Payables conversion period")
	plt.plot(quarter_list, icp_list, 's-', color = '#0080FF', label="Inventory conversion period")
	plt.plot(quarter_list, ccc_list, 's-', linewidth = 3, color = '#FF5151', label="Cash Conversion Cycle")

	plt.xticks(rotation = 30)

	plt.xlabel('Quarter')
	plt.ylabel('Days')
	plt.title(str(company) + '-Cash Conversion Cycle')

	num1 = 1.01
	num2 = 1
	num3 = 0
	num4 = 0
	plt.legend(bbox_to_anchor=(num1, num2), loc=num3, borderaxespad=num4).get_frame().set_alpha(0.5)

	plt.savefig(userid_date + 'test')
	plt.show()
	plt.close()