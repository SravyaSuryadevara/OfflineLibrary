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
# def search_pdfs(request):
#     query = request.GET.get('q', '').strip()

#     if query:
#         results = UploadedFile.objects.filter(
#             Q(file__icontains=query) | Q(extracted_text__icontains=query)
#         )
#     else:
#         results = UploadedFile.objects.all()  # Return all PDFs if no search term

#     # Debugging - Print matching results in the terminal
#     print(f"Search Query: {query}")
#     print("Search Results:", results)

#     # Serialize results
#     serializer = UploadedFileSerializer(results, many=True)
    
#     return Response({"results": serializer.data})

# def search_pdfs(request):
#     query = request.GET.get('q', '').strip()
    
#     if query:
#         results = UploadedFile.objects.filter(
#             Q(file__icontains=query) | Q(extracted_text__icontains=query)
#         )
#     else:
#         results = UploadedFile.objects.all()

#     # Construct full URL for PDFs
#     pdf_list = [
#         {
#             "id": pdf.id,
#             "filename": pdf.file.name,
#             "file_url": request.build_absolute_uri(pdf.file.url),  # ✅ Fix
#         }
#         for pdf in results
#     ]

#     return Response({"results": pdf_list})

def search_pdfs(request):
    query = request.GET.get('q', '').strip()
    
    if query:
        keywords = query.split()  # Split query into individual words
        q_objects = Q()

        # Use OR (|=) to match PDFs containing at least one keyword
        for keyword in keywords:
            q_objects |= (Q(file__icontains=keyword) | Q(extracted_text__icontains=keyword))

        results = UploadedFile.objects.filter(q_objects).distinct()  # Ensure unique results
    else:
        results = UploadedFile.objects.all()

    # Construct full URL for PDFs
    pdf_list = [
        {
            "id": pdf.id,
            "filename": pdf.file.name,
            "file_url": request.build_absolute_uri(pdf.file.url),  # ✅ Fix
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

# def pdf_library_view(request):
#     """Render the React frontend inside Django template."""
#     return render(request, "pdf_library.html")
def pdf_library_view(request):
    """Render the React frontend inside Django template."""
    return render(request, "offlineLibrary/pdf_library.html")