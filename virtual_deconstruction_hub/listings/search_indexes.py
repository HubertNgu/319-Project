from haystack import indexes
from listings.models import Listing

class ListingIndex(indexes.SearchIndex, indexes.Indexable):
    """ This is the model for the search index that is built for Listing objects.
    IMPORTANT NOTE - Must specify any fields of the model that need to be indexed
    below the 'text' line and also, any model field that are needed to filter 
    search results by need to be specified here as well.
    
    This index allows for the text, title, text_content, created,
    url, price, city, category and for_sale fields of post objects
    to be searchable.
    """
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    text_content = indexes.CharField(model_attr='text_content')
    created = indexes.DateTimeField(model_attr='created')
    url = indexes.CharField(model_attr='url')
    price = indexes.CharField(model_attr='price', null=True)
    city = indexes.CharField(model_attr='city', null=True)
    category = indexes.CharField(model_attr='category')
    for_sale = indexes.CharField(model_attr='for_sale')

    def get_model(self):
        """ Returns the model that this search index is built for.
        In this case it is a Listing object.
        """
        return Listing

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated.
        This only indexes listings that have been verified 
        and haven't expired
        """
        return self.get_model().objects.filter(expired=False).filter(verified=True)    
    
