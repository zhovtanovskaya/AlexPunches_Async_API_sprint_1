from worker_notifications.src.senders import SmartEmailSender


def get_sender_by_posting(posting):
    # пока у нас только один Сендер, но потом будет логика.
    return SmartEmailSender(posting)
