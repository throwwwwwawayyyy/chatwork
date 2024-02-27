from constants.texts import *
from enum import Enum

class AckCodes(Enum):
    CREDENTIALS_DENIED = 0
    CREDENTIALS_ACCEPTED = 1
    WHITELIST_OFF = 2
    WHITELIST_ON = 3
    CLIENT_DENIED = 4
    CLIENT_AUTHORIZED = 5
    ERROR = 6

errored_ack_codes = [AckCodes.CLIENT_DENIED, 
                     AckCodes.CREDENTIALS_DENIED, 
                     AckCodes.WHITELIST_OFF, 
                     AckCodes.ERROR]

ack_to_text = {
    AckCodes.CREDENTIALS_DENIED: CREDENTIALS_DENIED_TEXT,
    AckCodes.CREDENTIALS_ACCEPTED: CREDENTIALS_ACCEPTED_TEXT,
    AckCodes.WHITELIST_OFF: WHITELIST_OFF_TEXT,
    AckCodes.WHITELIST_ON: WHITELIST_ON_TEXT,
    AckCodes.CLIENT_DENIED: CLIENT_DENIED_TEXT,
    AckCodes.CLIENT_AUTHORIZED: CLIENT_AUTHORIZED_TEXT,
    AckCodes.ERROR: ERROR_TEXT
}