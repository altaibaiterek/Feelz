from django.dispatch import receiver

from django.db.models.signals import post_migrate

from apps.classroom.models import DayOfWeek


@receiver(post_migrate)
def create_days_of_week(sender, **kwargs):
    if not DayOfWeek.objects.exists():
        for day_id, day_name in DayOfWeek.DAYS_OF_WEEK:
            DayOfWeek.objects.create(id=day_id)
