TD_ACCOUNT_NO = '012345678'
LAST_FOUR_SSN = '1234'
NAME = 'john smith'
ADDRESS = '99 main street'
CITY = 'new york'
STATE = 'NY'
ZIP = '11011'
ROUTING_NO = '987654321'
CHECKING_ACCT = '123456789'
PAYMENT_AMT = '9999.99'
EMAIL = 'foo@email.com'

#########################################
#########################################
#########################################

import requests
from bs4 import BeautifulSoup
import datetime
# from functools import reduce

url = 'https://securepay.tdbank.com/cgi/tdbankExpress-bin/vortex.cgi'

def get_hidden_inputs(html):
	soup = BeautifulSoup(html, features="html.parser")
	hidden = {i['name']: i['value'] for i in soup.find('form', {'name': 'payment'}).find_all('input', type='hidden')}
	return hidden

def get_AcctValidate_form():
	form = {
		'Action': 'AcctValidate',
		'acct_num': TD_ACCOUNT_NO,
		'loginvar1': LAST_FOUR_SSN,
		'loginvar2': 'ML' # Mortgage Loan
	}

	response = requests.get(url, params=form)
	response.raise_for_status()
	return response.text

def post_ValidatePaymentInfo_form(inputs):
	inputs['Action'] = 'ValidatePaymentInfo'
	inputs['ec_subtype'] = 'C' # Checking
	inputs['ec_name1'] = NAME
	inputs['ec_addr1'] = ADDRESS
	inputs['ec_addr2'] = ''
	inputs['ec_city'] = CITY
	inputs['ec_state'] = STATE
	inputs['ec_zip'] = ZIP
	inputs['ec_aba'] = ROUTING_NO
	inputs['verify_ec_aba'] = ROUTING_NO
	inputs['ec_fund_acct_num'] = CHECKING_ACCT
	inputs['verify_ec_fund_acct_num'] = CHECKING_ACCT
	inputs['pmtdate1'] = '{dt.month}/{dt.day}/{dt.year}'.format(dt=datetime.datetime.now())
	inputs['ec_amt1'] = PAYMENT_AMT

	response = requests.post(url, data=inputs)
	response.raise_for_status()
	return response.text

def post_ConfirmPaymentInfo_form(inputs):
	inputs['Action'] = 'ConfirmPaymentInfo'

	response = requests.post(url, data=inputs)
	response.raise_for_status()
	return response.text

def post_SendEmail_form(inputs):
	inputs['Action'] = 'SendEmail'
	inputs['email'] = EMAIL
	
	response = requests.post(url, data=inputs)
	response.raise_for_status()
	return response.text

if __name__ == "__main__":
	print('gettting initial form')
	html = get_AcctValidate_form()
	print('posting validate payment form')
	html = post_ValidatePaymentInfo_form(get_hidden_inputs(html))
	print('posting confirm payment form')
	html = post_ConfirmPaymentInfo_form(get_hidden_inputs(html))
	print('posting send email form')
	html = post_SendEmail_form(get_hidden_inputs(html))
	print('done')	
	
	#reduce(lambda html, func: func(get_hidden_inputs(html)), [post_ValidatePaymentInfo_form, post_ConfirmPaymentInfo_form, post_SendEmail_form], get_AcctValidate_form())
