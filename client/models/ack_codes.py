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

errored_ack_codes = [AckCodes.CLIENT_DENIED.value, 
                     AckCodes.CREDENTIALS_DENIED.value, 
                     AckCodes.WHITELIST_OFF.value, 
                     AckCodes.ERROR.value]

ack_to_text = {
    AckCodes.CREDENTIALS_DENIED.value: CREDENTIALS_DENIED_TEXT,
    AckCodes.CREDENTIALS_ACCEPTED.value: CREDENTIALS_ACCEPTED_TEXT,
    AckCodes.WHITELIST_OFF.value: WHITELIST_OFF_TEXT,
    AckCodes.WHITELIST_ON.value: WHITELIST_ON_TEXT,
    AckCodes.CLIENT_DENIED.value: CLIENT_DENIED_TEXT,
    AckCodes.CLIENT_AUTHORIZED.value: CLIENT_AUTHORIZED_TEXT,
    AckCodes.ERROR.value: ERROR_TEXT
}