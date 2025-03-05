# shop/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return ['home', 'about','contact']

    def location(self, item):
        return reverse(item)