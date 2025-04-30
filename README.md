# OfflineLibrary
📄 PDF Upload with Text Extraction

Uses PyMuPDF (fitz) to extract text from uploaded PDFs.

Generates and stores a thumbnail for each PDF.

🔍 Full-text PDF Search

Powered by PostgreSQL Full-Text Search (SearchVector, SearchQuery, SearchRank).

Fallback to keyword-based search using Django Q lookups.

🖼️ Media Uploads (Images & Videos)

Auto-classifies media files using file extensions.

Supports previewing and filtering based on media type.

Media Search is done through videos and images filename.

🌐 REST API with Django REST Framework

Clean, structured APIs for uploading and fetching PDF/media data.

🧰 Tech Stack

Layer	Technology
Backend Framework	Django + Django REST Framework
Database	PostgreSQL
PDF Parsing	PyMuPDF (fitz)
Thumbnail Generator	Custom utility using PyMuPDF
Media Parsing	File extension-based logic
Search Engine	PostgreSQL Full-Text Search + fallback to icontains
Frontend Rendering	React (served via Django template)
CSS Framework	Tailwind CSS (utility-first styling)

💻 Local LAN Setup

The project was developed and tested in a LAN (Local Area Network) environment.

Django’s settings.py was configured with appropriate ALLOWED_HOSTS, e.g.:

ALLOWED_HOSTS = ['192.168.X.X', 'localhost', '127.0.0.1']

This allows access to the app from other devices on the same network for easier testing.
