import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
def verify(mobile):
    account_sid = 'ACf9573b4828f0151c6af5904a4e31604e'
    auth_token = '94bdf4b2a23595b5bbcdec78ab90323e'
    client = Client(account_sid, auth_token)

    verification = client.verify \
                     .services('VA061ae5f0a6ce7574c9441a87fd2a74bb') \
                     .verifications \
                     .create(to='+91'+mobile, channel='sms')

    print(verification.status)
def verify2(mobile,otp):
    account_sid = 'ACf9573b4828f0151c6af5904a4e31604e'
    auth_token = '94bdf4b2a23595b5bbcdec78ab90323e'
    client = Client(account_sid, auth_token)

    verification_check = client.verify \
                           .services('VA061ae5f0a6ce7574c9441a87fd2a74bb') \
                           .verification_checks \
                           .create(to='+91'+mobile, code=otp)

    print(verification_check.status)

    if verification_check.status == 'approved':
        return True
    else:
        return False