# Generated by Django 2.1.4 on 2019-04-24 21:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('commodity', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chatmsg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=2000)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('image', imagekit.models.fields.ProcessedImageField(default=None, upload_to='chatroom/img')),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Chatroom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_add', models.DateTimeField(auto_now_add=True)),
                ('mem1_del', models.BooleanField(default=False)),
                ('mem2_del', models.BooleanField(default=False)),
                ('mem1_read', models.BooleanField(default=False)),
                ('mem2_read', models.BooleanField(default=False)),
                ('commodity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commodity.Commodity')),
                ('member1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mem1', to=settings.AUTH_USER_MODEL)),
                ('member2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mem2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='chatmsg',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chatroom.Chatroom'),
        ),
        migrations.AddField(
            model_name='chatmsg',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]