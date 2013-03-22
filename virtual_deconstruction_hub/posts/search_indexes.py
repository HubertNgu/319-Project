from haystack import indexes
from posts.models import Post

"""IMPORTANT NOTE - Must specify any fields of the model that you want to be indexed below the 'text' line
and also, any model field that you want to filter search results by needs to be specified here as well """
class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    text_content = indexes.CharField(model_attr='text_content')
    created = indexes.DateTimeField(model_attr='created')
    url = indexes.CharField(model_attr='url')
    type = indexes.CharField(model_attr='type', faceted=True)

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated. This only indexes posts that have been verified"""
        return self.get_model().objects.filter(verified=True)  
    
