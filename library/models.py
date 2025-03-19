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
        super().save(*args, **kwargs)  # Save the file first
        if self.file:
            self.extract_text_from_pdf()
            super().save(update_fields=["extracted_text"])  # Save extracted text only

    # def extract_text_from_pdf(self):
    #     """Extracts text from the PDF and stores it in `extracted_text`."""
    #     # Ensure the correct file path
    #     pdf_path = os.path.join(settings.MEDIA_ROOT, self.file.name)  # Correct path
    #     text = ""

    #     try:
    #         with fitz.open(pdf_path) as doc:
    #             for page in doc:
    #                 extracted = page.get_text("text")  # Get text
    #                 if extracted:
    #                     text += extracted + "\n"  # Add newline for better readability

    #         if not text.strip():
    #             print(f"⚠️ Warning: No text extracted from {self.file.name}!")

    #     except Exception as e:
    #         print(f"❌ Error extracting text from {self.file.name}: {e}")

    #     self.extracted_text = text
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

