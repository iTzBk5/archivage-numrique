from django.urls import path
from .import views

urlpatterns = [
    #path('', views.index, name='index'),
    #('extract-to-pdf/', views.extract_pdf_to_db, name='extract-to-pdf'),
    #path('extract-ocr/', views.extract_ocr, name='extract-ocr'),
    path('blog/<int:pk>/', views.blog_detail, name='blog-detail'),  # Dynamic URL for blog details
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('pdf/', views.extract_pdf_to_db, name='pdf'),
    path('afterPdf/', views.afterPdf, name='afterPdf'),
    path('OCR/', views.extract_ocr, name='OCR'),
]
