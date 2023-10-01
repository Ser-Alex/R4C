import json
from json.decoder import JSONDecodeError

from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from robots.models import Robot
from robots.validators import validate_unique


@csrf_exempt
def api_robots(request: HttpRequest):
    """
    View функция для получения json, его обработки и сохранения полученной модели в базе
    """
    if request.method == 'POST':
        try:
            # парсим json
            parsed_robot = json.loads(request.body.decode())
        except JSONDecodeError:
            return JsonResponse({"error": "Incorrect json"}, status=400)

        serial = f"{parsed_robot['model']}-{parsed_robot['version']}"
        # создаём модель
        new_robot = Robot(serial=serial,
                          model=parsed_robot['model'],
                          version=parsed_robot['version'],
                          created=parsed_robot['created'],
                          )
        try:
            # проверяем валидацию модели, сохраняем в базе
            validate_unique(new_robot)
            new_robot.save()
        except ValidationError as e:
            return JsonResponse({"error": "incorrect data: " + str(e)}, status=400)

        return JsonResponse({"message": "Done"}, status=200)
    return JsonResponse({"error": "Method not supported"}, status=405)


