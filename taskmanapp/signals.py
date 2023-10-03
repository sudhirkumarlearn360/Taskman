from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete 
from .models import UserActivity, Task

@receiver(post_delete,sender=Task)
def deleted_task(sender,instance,**kwargs):
    if instance.user is not None:
        UserActivity.objects.create(
                user=instance.user,
                activity=f'You deleted task "{instance.task_name}".'
            )

@receiver(post_save,sender=Task)
def create_update_task(sender,instance,created,**kwargs):
    if instance.user is not None:
        if created:
            UserActivity.objects.create(
                user=instance.user, 
                activity=f'You created task: {instance.task_name}'
                )
        else:
            if instance.is_completed:
                UserActivity.objects.create(
                    user=instance.user,
                    activity=f'You marked task "{instance.task_name}" as complete.'
                    )
            else:
                UserActivity.objects.create(
                    user=instance.user,
                    activity=f'You marked task "{instance.task_name}" as incomplete.'
                    )