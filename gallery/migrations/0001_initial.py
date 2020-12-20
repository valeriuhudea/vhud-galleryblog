# Generated by Django 3.0.7 on 2020-12-17 03:33

from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields
import taggit.managers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(blank=True, max_length=1024, null=True)),
                ('thumbnail', imagekit.models.fields.ProcessedImageField(blank=True, upload_to='media')),
                ('visibility', models.CharField(choices=[('hidden', 'Hidden'), ('visible', 'Visible')], default='hidden', max_length=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'ordering': ('-modified',),
            },
        ),
        migrations.CreateModel(
            name='ClientMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Sender Name', max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('subject', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'ClientMessage',
            },
        ),
        migrations.CreateModel(
            name='AlbumImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to='media')),
                ('thumbnail', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to='media')),
                ('alt', models.CharField(default=uuid.uuid4, max_length=255)),
                ('description', models.TextField(blank=True, max_length=1024, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('width', models.IntegerField(default=0)),
                ('height', models.IntegerField(default=0)),
                ('slug', models.SlugField(default=uuid.uuid4, editable=False, max_length=70)),
                ('availability', models.CharField(choices=[('unavailable', 'Unavailable'), ('available', 'Available'), ('sold', 'Sold')], default='Unavailable', max_length=12)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('album', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='gallery.Album')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]