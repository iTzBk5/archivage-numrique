# Generated by Django 5.0.1 on 2024-04-29 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_blog_summary_alter_blog_publish'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='uploaded_file',
            field=models.FileField(default='none pdf', upload_to='pdfs/'),
        ),
    ]
