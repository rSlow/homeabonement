import enum


class PaymentStatuses(enum.Enum):
    succeeded = 'payment.succeeded'
    canceled = 'payment.canceled'
    waiting_for_capture = 'payment.waiting_for_capture'
    refund_succeeded = 'refund.succeeded'
    payout_succeeded = 'succeeded'
