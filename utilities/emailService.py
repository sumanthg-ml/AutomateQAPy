import smtplib 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
from .loggerService import LoggerService
from .configService import ConfigService

class EmailService(object):

    _testCache = None

    @classmethod
    def Init(cls,obj):
        cls._testCache = obj.testCache
 
    def sendEmail(self,subject=None,recipients=None,body=None,reportpath=None):  
        if self._testCache.config_service.get('emailenabled'):      
            emailSettings = self._testCache.config_service.getCustomSettings("emailsettings")
            if not subject: subject = emailSettings.get('emailsubject')
            sender_email = "SKG<sumanthkumar.gangula@hotmail.com>"
            if not recipients: recipients = emailSettings.get('emailrecipients')

            if recipients:
                
                text = """Test Execution has completed...


                Note: This is an auto-generated mail. Please do not reply.
                """
                if not body: body = text
                part1 = MIMEText(body, "plain")

                filename = reportpath  # In Reports directory
                attachmentname = list(str(filename).split('/'))[1]

                # Open  file in binary mode
                with open(filename, "rb") as attachment:
                    # Add file as application/octet-stream
                    # Email client can usually download this automatically as attachment
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())

                # Encode file in ASCII characters to send by email    
                encoders.encode_base64(part)

                # Add header as key/value pair to attachment part
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {attachmentname}",
                )

                

                message = MIMEMultipart("alternative")
                message["Subject"] = subject
                message["From"] = sender_email
                to_addrs = recipients
                if isinstance(recipients,list): to_addrs = ", ".join(recipients)
                message["To"] = to_addrs
                message.attach(part1)

                # Add attachment to message and convert message to string
                message.attach(part)

                try:
                    server = smtplib.SMTP("smtp.office365.com",587)
                    server.sendmail(sender_email, recipients, message.as_string())
                    self._testCache.logger_service.logger.info("Email sent to : "+to_addrs)
                except:
                    self._testCache.logger_service.logger.error("Sending email failed")
        else:
            self._testCache.logger_service.logger.info("Sending email skipped as not enabled")
        