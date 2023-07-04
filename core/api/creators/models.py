from datetime import datetime

from django.db import models
from django.conf import settings

from core.plugins.youtube_analytics.query import YouTubeQueryHook


class Creator(models.Model):
    class Meta:
        db_table = 'creators'
        verbose_name = 'Creator'
        verbose_name_plural = 'Creators'

    account_id = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='creator',
        db_column='account_id',
    )
    earnings = models.PositiveIntegerField(default=0)
    channel_id = models.CharField(max_length=255, null=True, blank=True)
    channel_name = models.CharField(max_length=255, null=True, blank=True)
    channel_verified = models.BooleanField(default=False)

    # Could be a better way to verify channel but this works for now
    def verify_channel(self, **credentials):
        """
        Verify channel based on query result from
        credentials and channel_id
        """
        query_params = {
            'channel_id': self.channel_id,
            'start_date': datetime.date.today() - datetime.timedelta(days=5),
            'end_date': datetime.date.today() - datetime.timedelta(days=3),
            'metrics': 'views',
            'dimensions': 'day',
            'sort': '-views',
        }
        youtube_query_hook = YouTubeQueryHook(**credentials)
        query_result = youtube_query_hook.get_query(**query_params)
        if query_result:
            self.channel_verified = True
            self.save()
            return True
        else:
            raise Exception('Channel could not be verified')
