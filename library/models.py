from django.db import models
import fitz  # PyMuPDF for extracting text from PDFs
import os
from django.conf import settings

class UploadedFile(models.Model):
    file = models.FileField(upload_to="uploads/")
    extracted_text = models.TextField(blank=True, null=True)  # Store extracted text
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp

    def save(self, *args, **kwargs):
        """Extract text from the uploaded PDF and save it in the database."""
        super().save(*args, **kwargs)
        if self.file:
            self.extract_text_from_pdf()
            super().save(update_fields=["extracted_text"])

    def extract_text_from_pdf(self):
        """Extracts text from the PDF efficiently and stores it in `extracted_text`."""
        pdf_path = os.path.join(settings.MEDIA_ROOT, self.file.name)
        text = []

        try:
            with fitz.open(pdf_path) as doc:
                for page in doc:
                    extracted = page.get_text("text")
                    if extracted:
                        text.append(extracted.strip())  # Store text efficiently

            if not text:
                print(f"⚠️ Warning: No text extracted from {self.file.name}!")

        except Exception as e:
            print(f"❌ Error extracting text from {self.file.name}: {e}")
            text = []

        self.extracted_text = "\n".join(text)  # Store text efficiently

import os

def media_upload_path(instance, filename):
    """
    Store images in /media/uploads/images/ and videos in /media/uploads/videos/
    """
    category = instance.get_file_category()
    return f"uploads/{category}s/{filename}"

class MediaFile(models.Model):
    file = models.FileField(upload_to=media_upload_path)
    category = models.CharField(max_length=10, blank=True)  # No choices, no dropdown
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def get_file_category(self):
        """Detect file type based on extension."""
        ext = os.path.splitext(self.file.name)[1].lower()
        if ext in [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"]:
            return "image"
        elif ext in [".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv"]:
            return "video"
        return "other"

    def save(self, *args, **kwargs):
        """Automatically assigns category before saving."""
        self.category = self.get_file_category()
        super().save(*args, **kwargs)