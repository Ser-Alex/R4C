from django.core.mail import send_mail
from django.db.models.signals import pre_save
from django.dispatch import receiver

from orders.models import Order
from .models import Robot


@receiver(pre_save, sender=Robot)
def new_robot_custom(sender, instance, **kwargs):
    """
    Функция, которая срабатывает от сигнала, проверят есть ли такой робот в заказах, и если есть
    то отправляет письмо заказчику, после удаляет заказ
    """
    orders = Order.objects.filter(robot_serial=instance.serial)
    if orders:
        # подтягиваем email заказчика
        to_mail = [orders[0].customer.email]
        subject = 'Robots-Company R4C'
        message = 'Добрый день!\n' \
                  f'Недавно вы интересовались нашим роботом модели {instance.model}, версии {instance.version}. \n' \
                  'Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами'
        # отправляем письмо
        send_mail(subject, message, 'robots@example.com', to_mail)
        # удаляем заказ
        orders[0].delete()
