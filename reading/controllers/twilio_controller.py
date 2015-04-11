from twilio.rest import TwilioRestClient

from .. import config


def send(message, to_numbers):
    """
    Send a message to the listed numbers that Twilio can parse.

    :param str message: The message to send
    :param to_numbers: The number or numbers to which to send the message
    :type to_numbers: str | list[str]
    """
    config = config.get_config()
    client = TwilioRestClient(config.twilio.account, config.twilio.token)

    # TODO(kw): Push to db
    if isinstance(to_numbers, basestring):
        client.messages.create(to=to_numbers, from_=config.twilio.from_number,
                               message=message)
    else:
        for to_number in to_numbers:
            client.messages.create(to=to_number, from_=config.twilio.from_number,
                                   message=message)
