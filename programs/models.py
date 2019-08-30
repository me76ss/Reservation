from enum import Enum

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Program(models.Model):
    name = models.CharField(max_length=255)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    notify_at = models.TimeField()
    queueable = models.BooleanField()
    cancel_threshold = models.TimeField()

    def __str__(self):
        start_date = timezone.localtime(self.starts_at)
        end_date = timezone.localtime(self.ends_at)

        return "Program (id={}, name={}, time=[{} - {}])".format(self.id, self.name, start_date, end_date)


class ProgramSlot(models.Model):
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    capacity = models.IntegerField()

    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='slots')

    def __str__(self):
        start_date = timezone.localtime(self.starts_at)
        end_date = timezone.localtime(self.ends_at)
        return "ProgramSlot (id={}, time=[{} - {}], capacity={})".format(self.id, start_date, end_date, self.capacity)

    def is_allowed_to_cancel(self):
        diff = self.starts_at - timezone.now()
        return (diff.total_seconds() - self.program.cancel_threshold.second) > 0


class ProgramSlotType(Enum):
    RESERVE = "RESERVE"
    WAITING = "WAITING"


class ProgramSlotRecord(models.Model):
    type = models.CharField(max_length=50, choices=((t.name, t.value) for t in ProgramSlotType))
    participated = models.BooleanField(default=False)

    slot = models.ForeignKey(ProgramSlot, on_delete=models.CASCADE, related_name='records')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='records')

    def __str__(self):
        return "ProgramSlotRecord (id={}, user:{}, program:{}, type:{}, participated={})" \
            .format(self.id, self.user.username, self.slot.program.name, self.type, self.participated)


class ProgramWhitList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.Case, related_name='white_list')
