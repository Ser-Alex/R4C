from django.core import mail
from django.test import TestCase

from customers.models import Customer
from orders.models import Order
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


class SignalNewRobotTestCase(TestCase):
    """
    Тесты для проверки new_robot_custom
    """
    email_customer = 'Test@mail.com'

    def test1(self):
        # тест на проверку удаления заказа, а так же на проверку email пользователя
        Customer(email=self.email_customer).save()
        Order(robot_serial='R2-D2', customer_id='1').save()
        Robot(serial='R2-D2', model='R2', version='D2', created='2022-12-31 23:59:59').save()

        self.assertFalse(Order.objects.all())

        first_message = mail.outbox[0]
        self.assertEqual(self.email_customer, first_message.to[0])

    def test2(self):
        # тест без заказов, проверка на то что письмо не отправиться
        Robot(serial='R2-D2', model='R2', version='D2', created='2022-12-31 23:59:59').save()
        self.assertFalse(mail.outbox)

    def test3(self):
        # тест с заказом, но с разными сериями
        Customer(email=self.email_customer).save()
        Order(robot_serial='R2-D2', customer_id='1').save()
        Robot(serial='R2-D3', model='R2', version='D2', created='2022-12-31 23:59:59').save()

        self.assertFalse(mail.outbox)



