from twilio.rest import Client

from backend.settings import TWILLIO_SID, TWILLIO_TOKEN


twilio = Client(TWILLIO_SID, TWILLIO_TOKEN)
