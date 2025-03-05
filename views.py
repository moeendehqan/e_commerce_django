import logging
logger = logging.getLogger(__name__)

class ZarinpalCallbackView(View):
    def get(self, request):
        logger.info("درخواست بازگشت از زرین‌پال دریافت شد")
        # ... کد موجود ...