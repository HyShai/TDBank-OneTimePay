TD_ACCOUNT_NO = '012345678'
LAST_FOUR_SSN = '1234'
NAME = 'john smith'
ROUTING_NO = '987654321'
CHECKING_ACCT = '123456789'
PAYMENT_AMT = 9999.99
EMAIL = 'foo@email.com'
BANK_NAME = 'MY BANK'.upper()

'''
XXXXXXXXXXXXXXX
X| .........\XX
XXX| @ XXX\  XX
XXX| @ XXXX| XX
XXX| @ XXX/  XX
XXX| @      /XX
XXXXXXXXXXXXXXX
XXXXXXXXXXXXXXX
'''

#region Setup
import requests
from bs4 import BeautifulSoup
import re
import json
import datetime
import logging

logging.basicConfig(level=logging.DEBUG)

s = requests.Session()

PAYMENT_DATE = '{dt.month}/{dt.day}/{dt.year}'.format(dt=datetime.datetime.now())
#endregion

#region Login
url = 'https://tdbank.billeriq.com/ebpp/TDUSPAYMENTS/Login/PayAsGuest'
data = {
    'BillerID': '3435',
    'AccountNumber': TD_ACCOUNT_NO,
    'PIN': LAST_FOUR_SSN
}
response = s.post(url, data=data)
#endregion

#region IDs
url = 'https://tdbank.billeriq.com/ebpp/TDUSPAYMENTS/BillPay'
response = s.get(url)

soup = BeautifulSoup(response.content)
invoice_row = soup.find('div', id=re.compile(r'^invoice-row-\d+$'))
invoice_id = invoice_row['data-id']
billing_account = invoice_row['data-billingaccount']
#endregion

#region AddPaymentMethod
url = 'https://tdbank.billeriq.com/ebpp/TDUSPAYMENTS/PaymentAccount/AddPaymentMethodACH?forPayment=true'
data = {
    'ID' : 0,
    'AchUsageType' : 'Personal',
    'AchType' : 'Checking',
    'IsDescriptionRequired' : 'False',
    'Name' : NAME,
    'AchRoutingNumber' : ROUTING_NO,
    'AchBankName' : BANK_NAME,
    'AchAccountNumber' : CHECKING_ACCT,
    'AchAccountNumberConfirm' : CHECKING_ACCT,
    'AchAgree' : 'true',
    'AchAgree' : 'false'
}
response = s.post(url, data=data)
#endregion

#region CalculateTotal
url = 'https://tdbank.billeriq.com/ebpp/TDUSPAYMENTS/Payment/BillPayCalculateTotal'
selection = {
    invoice_id: {
        'Amount': PAYMENT_AMT,
        'a': billing_account,
        'CreditMemo': False,
        'DefaultPayment': PAYMENT_AMT,
        's': True,
        'ServerSelected': False,
        'ReasonText': '',
        'DecryptedReferenceNumber': CHECKING_ACCT,
        'AdditionalFields': {}
    }
}
data = {
    'Selection': json.dumps(selection),
    'AccountAddOnSeclection': '',
    'AccountAddOnAmount': '0',
    'AccountAddOnLabel': '',
    'UserLevelAddonSelection': 'null',
    'PaymentAccountIndex': '0',
    'CVVCode': '',
    'PaymentDate': PAYMENT_DATE
}
response = s.post(url, data=data)
#endregion

#region BillPay
url = 'https://tdbank.billeriq.com/ebpp/TDUSPAYMENTS/Payment/BillPay'
response = s.post(url, data=data)
#endregion

#region VerifyAccountTotal
url = 'https://tdbank.billeriq.com/ebpp/TDUSPAYMENTS/Payment/VerifyAccountTotal'
data = {
    'Selection': '{}',
    'SkipDuplicate': '',
    'SkipFDPCheck': '',
    'SkipSupervisorApprovalCheck': '',
    'ApprovedByUserID': '',
    'SourcePage': 'BillPay',
    'AddOnAmount': '0',
    'AddOnAccount': '',
    'AccountAddOnAmount': '0',
    'AccountAddOnAccountLabel': '',
    'IsPPD': 'False',
    'UserlevelAddonSelection': '',
    'MailPaymentConfirmation': 'False',
    'EmailPaymentConfirmation': 'False',
    'MailConfirmationDelivery': '',
    'PaymentAccountIndex': '0',
    'CVVCode': '',
    'PaymentDate': PAYMENT_DATE
}
response = s.post(url, data=data)
#endregion

#region VerifyCalculateTotal
url = 'https://tdbank.billeriq.com/ebpp/TDUSPAYMENTS/Payment/VerifyCalculateTotal'
response = s.post(url, data=data)
#endregion

#region Confirm
url = 'https://tdbank.billeriq.com/ebpp/TDUSPAYMENTS/Payment/Confirm'
data = {
    'Selection': '{}',
    'SkipDuplicate': 'False',
    'SkipFDPCheck': 'False',
    'SkipSupervisorApprovalCheck': 'False',
    'ApprovedByUserID':'',
    'SourcePage': 'BillPay',
    'AddOnAmount': '0',
    'AddOnAccount': '',
    'AccountAddOnAmount': '0',
    'AccountAddOnAccountLabel': '',
    'IsPPD': 'False',
    'UserlevelAddonSelection': '{}',
    'MailPaymentConfirmation': 'False',
    'EmailPaymentConfirmation': 'True',
    'MailConfirmationDelivery': 'Email',
    'PaymentAccountIndex': '0',
    'CVVCode': '',
    'PaymentDate': PAYMENT_DATE,
    'CompanyName': NAME,
    'Email': EMAIL,
    'MailConfirmationDelivery': 'Email',
    'CustomerMailing.MailingEmail': EMAIL,
    'CompanyName': NAME,
    'MobilePhone': '',
    'Email': EMAIL,
    'CustomerMailing.MailingCompanyName': '',
    'CustomerMailing.MailingEmail': '',
    'CustomerMailing.MailingCountry': 'USA',
    'CustomerMailing.MailingAddress': '',
    'CustomerMailing.MailingAddress2': '',
    'CustomerMailing.MailingCity': '',
    'CustomerMailing.MailingZip': ''
}
response = s.post(url, data=data)
#endregion

#region Debugging
# url = 'https://example.com'
# response = requests.get(url, proxies={'http': 'http://127.0.0.1:8888', 'https':'http:127.0.0.1:8888'}, verify=r'FiddlerRoot.pem')
#endregion