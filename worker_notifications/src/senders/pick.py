from senders.smart_email import SmartEmailSender


def get_sender_by_posting(posting) -> SmartEmailSender:
    # пока у нас только один Сендер, но потом будет логика.
    return SmartEmailSender(posting)
