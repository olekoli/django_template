import uuid
import datetime

from django.db import models
from django.conf import settings
from django.utils import timezone


class IDable(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Ownable(models.Model):
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Timestampable(models.Model):
    created_date = models.DateTimeField(editable=False, null=True)
    modified_date = models.DateTimeField(editable=False, null=True)

    def save(self, *args, **kwargs):

        if not self.created_date:
            self.created_date = timezone.now()

        self.modified_date = timezone.now()

        return super(Timestampable, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Timeframable(models.Model):
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        today = datetime.date.today()
        if self.end_date:
            if self.start_date > self.end_date:
                raise ValueError(
                    f"End date: {self.end_date} is before start date {self.start_date}"
                )
        if self.start_date > today:
            raise ValueError("Start date is in the future")
        if self.active:
            self.end_date = None

        return super(Timeframable, self).save(*args, **kwargs)

    class Meta:
        abstract = True
