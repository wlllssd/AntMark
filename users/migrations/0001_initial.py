# Generated by Django 2.1.4 on 2019-05-14 12:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg_type', models.CharField(choices=[('M', 'massage'), ('S', 'stu_verify'), ('C', 'commodity_verify')], default='message', max_length=20)),
                ('text', models.CharField(max_length=2000)),
                ('id_content', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('sender_del', models.BooleanField(default=False)),
                ('receiver_del', models.BooleanField(default=False)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver_msg', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender_msg', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(default='None', max_length=20)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='Male', max_length=6)),
                ('intro', models.CharField(default='None', max_length=200)),
                ('phone', models.CharField(default='0', max_length=15)),
                ('wechat', models.CharField(default='None', max_length=30)),
                ('qq', models.CharField(default='0', max_length=16)),
                ('profile', imagekit.models.fields.ProcessedImageField(default='user/img/default.jpg', upload_to='user/img')),
                ('is_verified', models.BooleanField(default=False)),
                ('stuCardPhoto', imagekit.models.fields.ProcessedImageField(null=True, upload_to='user/img/verify')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
