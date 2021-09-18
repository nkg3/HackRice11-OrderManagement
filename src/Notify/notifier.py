import os
from twilio.rest import Client
from dotenv import load_dotenv


class Notifier:

    def __init__(self) -> None:
        load_dotenv()
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        self.client = Client(account_sid, auth_token)


    def notify_new_order(self, worker_name: str, phone_number: str, facility_id: str, equipment_id: str, time: str) -> str:
        body_str = 'New work order assigned to ' + worker_name + '. Report to ' + equipment_id + ' at ' + facility_id + '.'
        message = self.client.messages.create(
                                body=body_str,
                                from_='+17133641490',
                                to=phone_number
                                )
        return(message.sid)


n1 = Notifier()
n1.notify_new_order('Nik Gautam', '+13019198375', 'Fac3', 'El032', '02:00:00')