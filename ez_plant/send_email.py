import sendgrid
import os
from sendgrid.helpers.mail import *


class SendEmail(object):
    def __init__(self):
        pass

    def send_mail(self, message):
        with open(os.path.join(os.environ.get('HOME'), '.ez_plant.conf.json')) as config_file:
            config = json.load(config_file)

        sg = sendgrid.SendGridAPIClient(apikey=config['sendgrid_api_key'])
        from_email = Email("EZ-Plant@ezplant.com")
        subject = "EZ-Plant"
        to_email = Email("anat.eliahu@gmail.com")
        content = Content("text/plain", message)
        mail = Mail(from_email, subject, to_email, content)
        sg.client.mail.send.post(request_body=mail.get())
