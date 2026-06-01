import logging

# הגדרת לוגר ייעודי כדי שנראה את ההתראות בטרמינל בצורה ברורה
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NotificationSystem")

class NotificationService:
    @staticmethod
    def send_push_notification(user_id: int, title: str, body: str, data: dict = None):
        """
        שולח התראת Push למכשיר של המשתמש.
        בשלב הלוקאלי - מדמה את השליחה ללוגים. בפרודקשן - יתחבר ל-Firebase/Expo.
        """
        logger.info("\n" + "="*50)
        logger.info(f"📱 SENDING PUSH NOTIFICATION TO USER [{user_id}]")
        logger.info(f"🔔 TITLE: {title}")
        logger.info(f"💬 BODY:  {body}")
        if data:
            logger.info(f"📦 PAYLOAD DATA: {data}")
        logger.info("="*50 + "\n")
        
        # כאן בעתיד נכתוב:
        # messaging.send(messaging.Message(...)) # קוד Firebase רשמי
        return True

notification_service = NotificationService()