from django.conf import settings
from kavenegar import APIException, HTTPException, KavenegarAPI

from notification.services.sms_providers.base_sms_provider import BaseSMSProvider


class KavenegarSMSProvider(BaseSMSProvider):
    """
    SMS provider using Kavenegar API.
    """

    def __init__(self):
        """
        Initializes the Kavenegar API instance.
        """
        self.api_key = settings.SMS_SERVER_API_KEY
        self.sender_number = settings.SMS_NUMBER_SENDER

    def send_sms(self, recipient: str, message: str) -> bool:
        """
        Send an SMS via Kavenegar.

        :param recipient: The recipient's phone number.
        :param message: The SMS content.
        :return: True if sent successfully, False otherwise.
        """
        try:
            api = KavenegarAPI(self.api_key)
            params = {
                "sender": self.sender_number,
                "receptor": recipient,
                "message": message,
            }
            api.sms_send(params)
            print(f"SMS sent successfully to {recipient}")
            return True

        except (APIException, HTTPException) as e:
            print(f"Failed to send SMS: {e}")
            return False
