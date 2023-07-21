from django.db import models


class YoutubeReports(models.Model):
    class Meta:
        db_table = 'youtube_reports'
        verbose_name = 'Youtube Report'
        verbose_name_plural = 'Youtube Reports'

    id = models.AutoField(primary_key=True)
    date = models.DateField()
    report_url = models.CharField(max_length=255)
    report_type = models.CharField(max_length=255)
    report_name = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
