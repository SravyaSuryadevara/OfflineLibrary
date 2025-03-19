from haystack import indexes
from .models import UploadedFile  # ✅ Import model, don't redefine it

class UploadedFileIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    
    def get_model(self):
        return UploadedFile