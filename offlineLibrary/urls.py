"""
URL configuration for offlineLibrary project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from offlineLibrary.views import get_data, upload_file, pdf_library_view, pdf_list_api, search_pdfs, search_media
from rest_framework.routers import DefaultRouter
from offlineLibrary.views import MediaFileViewSet

router = DefaultRouter()
router.register(r'media', MediaFileViewSet, basename='media')
# from offlineLibrary.views import MediaListSearchView
urlpatterns = [
    path('', pdf_library_view, name='home'),
    path('api/data/', get_data),
    path('api/upload/', upload_file, name='file-upload'),
    path("pdf-library/", pdf_library_view, name="pdf_library"),
    path("api/pdf-list-api/", pdf_list_api, name="pdf_list_api"),  # ✅ API for React
    path("api/search-pdfs/", search_pdfs, name="search_pdfs"),
    path("api/", include(router.urls)),
    path("api/search-media/", search_media, name="search-media"),
    # path("upload/", UploadMediaView.as_view(), name="upload_media"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


