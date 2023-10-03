from django.apps import AppConfig


class TaskmanappConfig(AppConfig):
    name = 'taskmanapp'

    def ready(self):
        import taskmanapp.signals
