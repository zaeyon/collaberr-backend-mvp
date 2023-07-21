from django.db import models
from django.conf import settings


class ChannelBasic(models.Model):
    """
    Based on channel_basic_a2
    Only verified channel will have this report
    Aggregated on date, video_id, subscribed_status, country_code
    """
    class Meta:
        db_table = 'channel_basics'
        verbose_name = 'Channel Basic'
        verbose_name_plural = 'Channel Basics'

    creator_id = models.OneToOneField(
        'creators.Creator',
        on_delete=models.CASCADE,
        related_name='creator_basics',
        db_column='creator_id',
        primary_key=True
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='creator_basics',
    )
    # dimensions
    date = models.DateField()
    channel_id = models.CharField(max_length=100)
    channel_name = models.CharField(max_length=100)
    channel_handle = models.CharField(max_length=100)
    video_id = models.CharField(max_length=100)
    subscribed_status = models.PositiveIntegerField(default=0)
    country_code = models.CharField(max_length=4)
    # core metrics
    views = models.PositiveIntegerField(default=0)
    comments = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    shares = models.PositiveIntegerField(default=0)
    watch_time_minutes = models.PositiveIntegerField(default=0)
    average_view_duration_seconds = models.PositiveIntegerField(default=0)
    average_view_percentage = models.PositiveIntegerField(default=0)
    susbscribers_gained = models.PositiveIntegerField(default=0)
    subscribers_lost = models.PositiveIntegerField(default=0)
    # additional metrics
    annotation_impressions = models.PositiveIntegerField(default=0)
    annotation_clicks = models.PositiveIntegerField(default=0)
    annotation_click_through_rate = models.PositiveIntegerField(default=0)
    card_impressions = models.PositiveIntegerField(default=0)
    card_clicks = models.PositiveIntegerField(default=0)
    card_click_through_rate = models.PositiveIntegerField(default=0)
    videos_added_to_playlists = models.PositiveIntegerField(default=0)
    videos_removed_from_playlists = models.PositiveIntegerField(default=0)
    red_views = models.PositiveIntegerField(default=0)
    red_watch_time_minutes = models.PositiveIntegerField(default=0)


# class ChannelDemographics(models.Model):
#     """
#     Based on channel_traffic_source_a2
#     Only verified channel will have this report
#     Aggregated on date, video_id, subscribed_status, country_code
#     """
