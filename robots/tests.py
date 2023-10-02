from django.test import TestCase

from robots.models import Robot


class RobotsLoadTestCase(TestCase):
    """
    Тесты для проверки robots_api

    загружаем фикстуры
    """
    fixtures = ['fixtures/fixtures-robots.json']

    def test1(self):
        # тест с идеальными событиями
        json_robot = '{"model": "R2", "version": "D2", "created": "2022-12-31 23:59:59"}'
        response = self.client.post('/api/robots/', json_robot, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test2(self):
        # тест с нарушением json
        json_robot = '{"model": "R2", "version": "D2", "created": "2022-12-31 23:59:59" JSON violation '
        response = self.client.post('/api/robots/', json_robot, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test3(self):
        # тест с валидацией моделей
        json_robot = '{"model": "non-existent model", "version": "D2", "created": "2022-12-31 23:59:59"}'
        response = self.client.post('/api/robots/', json_robot, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test4(self):
        # тест с неправильным методом запроса
        json_robot = '{"model": "R2", "version": "D2", "created": "2022-12-31 23:59:59"}'
        response = self.client.get('/api/robots/')
        self.assertEqual(response.status_code, 405)


class ExcelRobotsTestCase(TestCase):
    """
    Тесты для проверки robots_index_excel

    загружаем фикстуры
    """
    fixtures = ['fixtures/fixtures-robots.json']
    def test1(self):
        # тест с проверкой полученного ответа на файл excel
        response = self.client.get('/robots/excel/download/')
        self.assertEqual("application/vnd.ms-excel", response['Content-Type'])



