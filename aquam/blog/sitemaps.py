from django.contrib.sitemaps import Sitemap
from .models import Gallery


class Detail(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Gallery.objects.all()

    def lastmod(self, obj):
        return obj.created_date
