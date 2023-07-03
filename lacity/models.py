from django.db import models
from django_extensions.db.models import TimeStampedModel

class Council(TimeStampedModel):
    council_id = models.CharField(max_length=255, unique=True)
    url = models.URLField()
    title = models.TextField()
    data = models.JSONField(
        default=dict,
    )
    metting_date = models.DateField(
        null=True,
        blank=True,
    )
    metting_type = models.CharField(
        max_length=255,
        default="Regular",
        null=True,
        blank=True,
    )
    vote_action = models.CharField(
        max_length=255,
        default="Adopted",
        null=True,
        blank=True,
    )
    vote_given = models.CharField(
        max_length=255,
        default="(0 - 0 - 0)",
        null=True,
        blank=True,
    )
    raw_html = models.TextField(
        null=True,
        blank=True,
    )


class Document(TimeStampedModel):
    council = models.ForeignKey(
        Council,
        on_delete=models.CASCADE,
        related_name="documents",
    )
    date = models.DateField()
    title = models.TextField()
    url = models.URLField()
    data = models.JSONField(
        default=dict,
    )


class Voter(TimeStampedModel):
    name = models.CharField()


class Vote(TimeStampedModel):
    council = models.ForeignKey(
        Council,
        on_delete=models.CASCADE,
        related_name="votes",
    )
    voter = models.ForeignKey(
        Voter,
        on_delete=models.CASCADE,
        related_name="votes",
    )


class Activity(TimeStampedModel):
    council = models.ForeignKey(
        Council,
        on_delete=models.CASCADE,
        related_name="activities",
    )
    date = models.DateField()
    activity = models.TextField()
    documents = models.JSONField(
        default=dict,
    )
