from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import Blog



@registry.register_document
class BlogDocument(Document):
    class Index:
        name = 'blog'

    url = fields.TextField(attr='get_absolute_url')
    class Django:
        model = Blog
        fields = ['id','title', 'description','image','summary','uploaded_file']

