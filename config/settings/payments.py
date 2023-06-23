from yookassa import Configuration

from config.settings.base import ENV

YOOKASSA_SHOP_ID = ENV.int("YOOKASSA_SHOP_ID")  # shopId
YOOKASSA_ACCOUNT_ID = ENV.str("YOOKASSA_ACCOUNT_ID")  # account_secret_key
Configuration.account_id = YOOKASSA_SHOP_ID
Configuration.secret_key = YOOKASSA_ACCOUNT_ID
YOOKASSA_NETS = ENV.list("YOOKASSA_NETS")
YOOKASSA_IPS = ENV.list("YOOKASSA_IPS")

PAYMENT_DECIMAL_PLACES = 2
PAYMENT_MAX_DIGITS = 10
