# Generated by Django 2.0.1 on 2018-01-28 19:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0004_topic_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='message',
        ),
    ]
