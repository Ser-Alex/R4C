from django.core.exceptions import ValidationError


# Валидация модели робота
def validate_unique(robot):
    from robots.models import Robot

    is_other = Robot.objects.filter(model=robot.model).exists()
    if not is_other:
        raise ValidationError(
            'No such model exists %(model)s',
            code='invalid',
            params={'model': robot.model},
        )
