import datetime

from django.core.files.temp import NamedTemporaryFile
from django.db import models
from openpyxl.workbook import Workbook


class Robot(models.Model):
    serial = models.CharField(max_length=5, blank=False, null=False)
    model = models.CharField(max_length=2, blank=False, null=False)
    version = models.CharField(max_length=2, blank=False, null=False)
    created = models.DateTimeField(blank=False, null=False)

    def robots_week_excel(self) -> bytes:
        """
        Функция создание excel файла со сводкой показательей производства роботов

        :return: временный поток excel файла
        """
        # создаём экземпляр рабочего документа excel
        wb = Workbook()
        date = datetime.date.today() - datetime.timedelta(days=7)
        # сортируем всех роботов по дате(неделя)
        robots = Robot.objects.filter(created__gte=date)

        robots_model = {robot.model for robot in robots}
        for model in robots_model:
            # создаём страничку в файле и заполняем данные
            ws = wb.create_sheet()
            ws.title = f'Robots model {model}'
            ws.append(["Модель", "Версия", "Количество за неделю"])

            robots_filter_model = robots.filter(model=model)
            robots_version = {robot.version for robot in robots_filter_model}
            for version in robots_version:
                count_robots = robots_filter_model.filter(version=version).count()
                ws.append([model, version, count_robots])

        # удаляем первую стандартную страничку
        wb.remove(wb['Sheet'])

        # обращаемся к контекстному менеджеру, читаем временный файл
        with NamedTemporaryFile() as tmp:
            wb.save(tmp.name)
            tmp.seek(0)
            stream = tmp.read()
        return stream
