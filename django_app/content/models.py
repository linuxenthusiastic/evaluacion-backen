import uuid
from django.db import models
from django.conf import settings


class Conference(models.Model):
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name        = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    starts_at   = models.DateTimeField()
    ends_at     = models.DateTimeField()
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '"content"."conference"'
        ordering = ['starts_at']

    def __str__(self):
        return self.name


class Track(models.Model):
    id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name         = models.CharField(max_length=255)
    color        = models.CharField(max_length=7, default='#6366f1')
    conference   = models.ForeignKey(
        Conference,
        on_delete=models.CASCADE,
        related_name='tracks'
    )
    created      = models.DateTimeField(auto_now_add=True)
    modified     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '"content"."track"'

    def __str__(self):
        return self.name


class Speaker(models.Model):
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name        = models.CharField(max_length=255)
    bio         = models.TextField(blank=True)
    affiliation = models.CharField(max_length=255, blank=True, default='')
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '"content"."speaker"'

    def __str__(self):
        return self.name


class Session(models.Model):
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title       = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    starts_at   = models.DateTimeField()
    ends_at     = models.DateTimeField(null=True, blank=True)
    capacity    = models.PositiveIntegerField(default=0)
    track       = models.ForeignKey(
        Track,
        on_delete=models.CASCADE,
        related_name='sessions'
    )
    speakers    = models.ManyToManyField(
        Speaker,
        through='SessionSpeaker',
        related_name='sessions'
    )
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '"content"."session"'
        ordering = ['starts_at']

    def __str__(self):
        return self.title


class SessionSpeaker(models.Model):
    id       = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session  = models.ForeignKey(Session, on_delete=models.CASCADE)
    speaker  = models.ForeignKey(Speaker, on_delete=models.CASCADE)
    created  = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '"content"."session_speaker"'
        constraints = [
            models.UniqueConstraint(
                fields=['session', 'speaker'],
                name='unique_session_speaker'
            )
        ]


class Registration(models.Model):
    id            = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user          = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='registrations'
    )
    session       = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name='registrations'
    )
    registered_at = models.DateTimeField(auto_now_add=True)
    created       = models.DateTimeField(auto_now_add=True)
    modified      = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '"content"."registration"'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'session'],
                name='unique_user_session'
            )
        ]
