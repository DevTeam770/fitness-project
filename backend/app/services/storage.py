import os
import boto3
from botocore.exceptions import NoCredentialsError
from fastapi import UploadFile

class StorageService:
    def __init__(self):
        # התחברות ל-API של ה-S3 (מקומי או ענן)
        self.s3 = boto3.client(
            's3',
            endpoint_url=os.getenv("STORAGE_ENDPOINT"),
            aws_access_key_id=os.getenv("STORAGE_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("STORAGE_SECRET_KEY")
        )
        self.bucket_name = os.getenv("STORAGE_BUCKET_NAME", "fitness-assets")
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        """מוודא שתיקיית העל (Bucket) קיימת בשרת האחסון, ואם לא - יוצר אותה"""
        try:
            self.s3.head_bucket(Bucket=self.bucket_name)
        except:
            self.s3.create_bucket(Bucket=self.bucket_name)

    def upload_progress_picture(self, user_id: int, file: UploadFile) -> str:
        """מעלה תמונת התקדמות של משתמש ומחזירה את כתובת ה-URL שלה"""
        # יצירת נתיב ייחודי ומאורגן בתוך הענן
        file_extension = os.path.splitext(file.filename)[1]
        file_key = f"users/{user_id}/progress/{file.filename}"
        
        try:
            self.s3.upload_fileobj(
                file.file,
                self.bucket_name,
                file_key,
                ExtraArgs={"ContentType": file.content_type}
            )
            # החזרת ה-URL לצורך שמירה ב-DB
            return f"{os.getenv('STORAGE_ENDPOINT')}/{self.bucket_name}/{file_key}"
        except NoCredentialsError:
            raise Exception("Storage credentials not found")

storage_service = StorageService()