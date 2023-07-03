from django.db import models


class YoutubeReports(models.Model):
    class Meta:
        db_table = 'youtube_reports'
        verbose_name = 'Youtube Report'
        verbose_name_plural = 'Youtube Reports'
