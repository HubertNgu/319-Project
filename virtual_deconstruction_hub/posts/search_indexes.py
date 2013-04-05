from haystack import indexes
from posts.models import Post

class PostIndex(indexes.SearchIndex, indexes.Indexable):
    """ This is the model for the search index that is built for Post objects.
    IMPORTANT NOTE - Must specify any fields of the model that need to be indexed
    below the 'text' line and also, any model field that are needed to filter 
    search results by need to be specified here as well.
    
    This index allows for the text, title, text_content, created,
    url and type fields of post objects to be searchable.
    """
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    text_content = indexes.CharField(model_attr='text_content')
    created = indexes.DateTimeField(model_attr='created')
    url = indexes.CharField(model_attr='url')
    type = indexes.CharField(model_attr='type', faceted=True)

    def get_model(self):
        """ Returns the model that this search index is built for.
        In this case it is a Post object.
        """
        return Post

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated.
        This only indexes posts that have been verified
        """
        return self.get_model().objects.filter(verified=True)  
    
