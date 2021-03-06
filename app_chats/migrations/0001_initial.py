# Generated by Django 3.2.4 on 2021-07-30 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_main', '0001_initial'),
        ('app_accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app_main.basemodel')),
                ('room_name', models.CharField(max_length=50)),
                ('room_icon', models.ImageField(blank=True, null=True, upload_to='room')),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            bases=('app_main.basemodel',),
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app_main.basemodel')),
                ('message', models.CharField(max_length=50)),
                ('is_deleted', models.BooleanField(default=False)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group', to='app_chats.room')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sender', to='app_accounts.customers')),
            ],
            bases=('app_main.basemodel',),
        ),
    ]
