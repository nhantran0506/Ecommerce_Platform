from config import (
    VNPAY_TMN_CODE,
    VNPAY_HASH_SECRET_KEY,
    VNPAY_PAYMENT_URL,
    VNPAY_RETURN_URL,
)
import logging
from serializers.ProductSerializers import VNPayPaymentCreate
from datetime import datetime
from fastapi import Request
import hmac
import hashlib


logger = logging.getLogger(__name__)


def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0]
    return request.client.host


async def get_vnpay_url(payment: VNPayPaymentCreate, request: Request):
    try:
        vnp_Version = "2.1.0"
        vnp_Command = "pay"
        vnp_TmnCode = VNPAY_TMN_CODE
        vnp_Amount = int(payment.amount)
        vnp_CurrCode = "VND"
        vnp_TxnRef = payment.order_id
        vnp_OrderInfo = payment.order_desc
        vnp_Locale = payment.language or "en"
        vnp_BankCode = ""
        vnp_CreateDate = datetime.now().strftime("%Y%m%d%H%M%S")
        vnp_IpAddr = get_client_ip(request)

        hash_data = {
            "vnp_Version": vnp_Version,
            "vnp_Command": vnp_Command,
            "vnp_TmnCode": vnp_TmnCode,
            "vnp_Amount": vnp_Amount,
            "vnp_CurrCode": vnp_CurrCode,
            "vnp_TxnRef": vnp_TxnRef,
            "vnp_OrderInfo": vnp_OrderInfo,
            "vnp_OrderType": "100000",
            "vnp_Locale": vnp_Locale,
            "vnp_ReturnUrl": VNPAY_RETURN_URL,
            "vnp_IpAddr": vnp_IpAddr,
            "vnp_CreateDate": vnp_CreateDate,
        }

        if vnp_BankCode:
            hash_data["vnp_BankCode"] = vnp_BankCode

        hash_data = sorted(hash_data.items())
        queryString = ""
        seq = 0
        import urllib.parse

        for key, val in hash_data:
            if seq == 1:
                queryString += "&" + key + "=" + urllib.parse.quote_plus(str(val))
            else:
                seq = 1
                queryString = key + "=" + urllib.parse.quote_plus(str(val))

        query = queryString

        secure_hash = hmac.new(
            VNPAY_HASH_SECRET_KEY.encode("utf-8"), query.encode("utf-8"), hashlib.sha512
        ).hexdigest()

        payment_url = f"{VNPAY_PAYMENT_URL}?{query}&vnp_SecureHash={secure_hash}"
        return payment_url
    except Exception as e:
        logger.error(str(e))
        return None
