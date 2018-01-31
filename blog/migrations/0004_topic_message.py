# Generated by Django 2.0.1 on 2018-01-28 18:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_topic_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='message',
            field=models.CharField(default=django.utils.timezone.now, help_text='The max length of the text is 4000.', max_length=4000),
            preserve_default=False,
        ),
    ]