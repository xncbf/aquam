from haystack import indexes
from .models import Gallery


class GalleryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.EdgeNgramField(model_attr='title')
    detail = indexes.EdgeNgramField(model_attr='detail')
    created_date = indexes.DateTimeField(model_attr='created_date')
    categorys = indexes.CharField(model_attr='categorys_id')

    def get_model(self):
        return Gallery

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()