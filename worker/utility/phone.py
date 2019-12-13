# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# 您的帐户Sid和来自o.com/console的验证令牌
account_sid = 'AC4e30ba292bcf6fc97ca656aa71b34bc6'
auth_token = 'your_auth_token'
client = Client(account_sid, auth_token)

message = client.messages.create(from_='+15017122661', body='body', to='+15558675310')

print(message.sid)