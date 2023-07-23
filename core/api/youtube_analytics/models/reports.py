from django.db import models


class YoutubeReportingJob(models.Model):
    """
    Display what kind of reports are available along with dates
    """
    class Meta:
        db_table = 'youtube_reporting_job'
        verbose_name = 'Youtube Reporting Job'
        verbose_name_plural = 'Youtube Reporting Jobs'

    id = models.AutoField(primary_key=True)
    owner = models.OneToOneField(
        'creators.Creator',
        on_delete=models.CASCADE,
        db_column='owner',
        related_name='youtube_reporting_job',
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    job_id = models.CharField(max_length=255)
    # report_url = models.CharField(max_length=255)
    job_type = models.CharField(max_length=255)
    job_name = models.CharField(max_length=255)
