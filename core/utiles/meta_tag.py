from core.models import SiteSettings
from django.http import HttpRequest


class MetaTag:
    def __init__(self, title=None, description=None, keywords=None, image=None, robots=None):
        """
        title: str = None
        description: str = None
        keywords: str = None
        image: str = None
        robots: str = None
        """
        site = SiteSettings.get_instance()

        # Safe defaults
        self.base_title = site.meta_title or site.title or ""
        self.page_title = title or ""
        self.title = f"{self.base_title} | {self.page_title}" if self.page_title else self.base_title

        # Safe logo handling
        try:
            default_image = site.logo.url
        except Exception:
            default_image = ""

        self.image = image or default_image

        # Description
        self.description = description or site.meta_description or ""

        # Keywords
        self.keywords = keywords or site.meta_keywords or ""
        # Robots
        self.robots = robots or "index, follow"


    def full_meta_tag(self):
        return {
            "title": self.title,
            "description": self.description,
            "keywords": self.keywords,
            "og_image": self.image,
        }
