from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from django.http import JsonResponse
from library.models import UploadedFile
from rest_framework.response import Response
from rest_framework.decorators import api_view
from haystack.query import SearchQuerySet
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from library.models import UploadedFile
from django.db.models import Q
from library.models import UploadedFile  # Use UploadedFile model
from library.serializers import UploadedFileSerializer  # Ensure this exists
from django.conf import settings
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from library.models import MediaFile
from library.serializers import MediaFileSerializer
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status, viewsets
from library.models import MediaFile
from library.serializers import MediaFileSerializer

@api_view(['GET'])
def get_data(request):
    return Response({"message": "Hello from Django!"})

@api_view(["POST"])
@parser_classes([MultiPartParser])  # Ensures file uploads work correctly
def upload_file(request):
    if "file" not in request.FILES:
        return JsonResponse({"error": "No file uploaded"}, status=400)

    uploaded_file = request.FILES["file"]

    # Save file using Django's model
    file_instance = UploadedFile(file=uploaded_file)
    file_instance.save()

    return JsonResponse(
        {
            "message": "File uploaded successfully",
            "filename": file_instance.file.name,  # Path relative to MEDIA_ROOT
            "file_url": file_instance.file.url,  # Get full URL
        },
        status=201
    )

@csrf_exempt

@api_view(['GET'])

def search_pdfs(request):
    query = request.GET.get('q', '')

    if query:  # Ensure query isn't empty
        keywords = query.split()  # Split query into words
        search_query = SearchQuery(query)  # Full-text search query

        # Annotate with full-text search vector
        results = UploadedFile.objects.annotate(
            search=SearchVector('file', 'extracted_text')
        ).filter(search=search_query)  # Full-text search

        if not results.exists():  # Fallback to basic keyword matching
            q_objects = Q()
            for keyword in keywords:
                q_objects |= (Q(file__icontains=keyword) | Q(extracted_text__icontains=keyword))
            results = UploadedFile.objects.filter(q_objects).distinct()

    else:
        # If query is empty, return the full list
        results = UploadedFile.objects.all()

    pdf_list = [
        {
            "id": pdf.id,
            "filename": pdf.file.name,
            "file_url": request.build_absolute_uri(pdf.file.url),
        }
        for pdf in results
    ]

    return Response({"results": pdf_list})

def pdf_list_api(request):
    query = request.GET.get("q", "").strip()
    pdfs = UploadedFile.objects.all()

    if query:
        pdfs = pdfs.filter(Q(file__icontains=query) | Q(file__regex=query))

    pdf_list = [
        {
            "id": pdf.id,
            "filename": pdf.file.name,
            "file_url": request.build_absolute_uri(pdf.file.url),
        }
        for pdf in pdfs
    ]
    return JsonResponse({"pdfs": pdf_list}, status=200)

def pdf_library_view(request):
    """Render the React frontend inside Django template."""
    return render(request, "offlineLibrary/pdf_library.html")

# class MediaFileViewSet(viewsets.ModelViewSet):
#     queryset = MediaFile.objects.all()
#     serializer_class = MediaFileSerializer
#     parser_classes = (MultiPartParser, FormParser)

#     def create(self, request, *args, **kwargs):
#         file = request.FILES.get("file")
#         category = request.data.get("category")

#         if file and category in ["image", "video"]:
#             media_file = MediaFile(file=file, category=category)
#             media_file.save()
#             return Response({"message": "File uploaded successfully"}, status=status.HTTP_201_CREATED)

#         return Response({"error": "Invalid file or category"}, status=status.HTTP_400_BAD_REQUEST)
class MediaFileViewSet(viewsets.ModelViewSet):
    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        """Upload media files and auto-assign category."""
        file = request.FILES.get("file")

        if file:
            media_file = MediaFile(file=file)  # Auto-assign category
            media_file.save()
            return Response(
                {"message": "File uploaded successfully", "category": media_file.category},
                status=201
            )

        return Response({"error": "Invalid file"}, status=400)

    def list(self, request, *args, **kwargs):
        """List uploaded media files grouped into images and videos."""
        images = MediaFile.objects.filter(category="image")
        videos = MediaFile.objects.filter(category="video")

        return Response({
            "images": MediaFileSerializer(images, many=True).data,
            "videos": MediaFileSerializer(videos, many=True).data
        })

@api_view(['GET'])
def search_media(request):
    query = request.GET.get("q", "").strip().lower()

    if not query:
        return Response({"results": []}, status=status.HTTP_200_OK)

    # Search by filename
    images = MediaFile.objects.filter(category="image", file__icontains=query)
    videos = MediaFile.objects.filter(category="video", file__icontains=query)

    image_data = MediaFileSerializer(images, many=True).data
    video_data = MediaFileSerializer(videos, many=True).data

    return Response({"results": image_data + video_data}, status=status.HTTP_200_OK)