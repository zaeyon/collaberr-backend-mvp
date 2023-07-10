from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MaxLengthValidator

from core.general.models import CreatedModified
from core.api.creators.models import Creator


class Campaign(CreatedModified):
    class Meta:
        verbose_name = 'Campaign'
        verbose_name_plural = 'Campaigns'
        db_table = 'campaigns'

    class Category(models.TextChoices):
        FASHION = 'Fashion'
        BEAUTY = 'Beauty'
        FOOD = 'Food'
        TRAVEL = 'Travel'
        BEVERAGES = 'Beverages'

    class Platform(models.TextChoices):
        INSTAGRAM = 'Instagram'
        YOUTUBE = 'Youtube'
        TIKTOK = 'Tiktok'

    class MissionType(models.TextChoices):
        YOUTUBE_VIDEO = 'Youtube Video'
        YOUTUBE_SHORTS = 'Youtube Shorts'
        POST = 'Post'
        STORY = 'Story'
        REEL = 'Reel'
        IGTV = 'IGTV'
        TIKTOK_VIDEO = 'Tiktok Video'

    id = models.AutoField(
            primary_key=True,
            unique=True,
            editable=False
        )
    owner = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE
        )
    # fields that business owners fill
    brand_name = models.TextField(validators=[MaxLengthValidator(100)])
    title = models.TextField(validators=[MaxLengthValidator(100)])
    thumbnail = models.ImageField(
                            upload_to='campaigns/thumbnails/',
                            null=True,
                            blank=True
                        )
    category = models.TextField(choices=Category.choices)
    platform = models.TextField(choices=Platform.choices)
    recruit_start_date = models.DateField()
    recruit_end_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    mission_type = models.TextField(choices=MissionType.choices)
    reward = models.PositiveIntegerField()
    additional_files = models.FileField(
                            upload_to='campaigns/additional_files/',
                            null=True,
                            blank=True
                        )
    # auto populated fields
    created_at = models.DateTimeField(editable=False)
    modified_at = models.DateTimeField()
    is_draft = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_recruiting = models.BooleanField(default=True)
    is_recruited = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    # creator actions
    requested_creators = models.ManyToManyField(
                                Creator,
                                related_name='requested_campaigns',
                                blank=True
                            )
    approved_creators = models.ManyToManyField(
                                Creator,
                                related_name='approved_campaigns',
                                blank=True
                            )
    rejected_creators = models.ManyToManyField(
                                Creator,
                                related_name='rejected_campaigns',
                                blank=True
                            )

    def __str__(self):
        return f'{self.title} | {self.username}'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super().save(*args, **kwargs)
