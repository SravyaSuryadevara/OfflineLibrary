from rest_framework import serializers
from library.models import UploadedFile

class UploadedFileSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = UploadedFile
        fields = ["id", "filename", "file_url", "extracted_text"]

    def get_filename(self, obj):
        return obj.file.name  # ✅ Extracts the filename correctly

    def get_file_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.file.url) if request else obj.file.url
