from haystack.forms import SearchForm


class GallerySearchForm(SearchForm):

    def no_query_found(self):
        return self.searchqueryset.all()
