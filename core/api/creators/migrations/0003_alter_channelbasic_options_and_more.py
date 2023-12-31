# Generated by Django 4.2.3 on 2023-07-19 07:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("creators", "0002_alter_creator_channel_handle_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="channelbasic",
            options={
                "verbose_name": "Channel Basic",
                "verbose_name_plural": "Channel Basics",
            },
        ),
        migrations.AlterField(
            model_name="channelbasic",
            name="creator_id",
            field=models.OneToOneField(
                db_column="creator_id",
                on_delete=django.db.models.deletion.CASCADE,
                primary_key=True,
                related_name="creator_stats",
                serialize=False,
                to="creators.creator",
            ),
        ),
        migrations.AlterModelTable(
            name="channelbasic",
            table="channel_basics",
        ),
    ]
