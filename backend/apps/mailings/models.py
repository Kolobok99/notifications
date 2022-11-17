import datetime

from django.db import models


class Mailing(models.Model):
    """Модель рассылки"""

    STATUS_CHOICES = (
        ('C', 'CREATED'),
        ('S', 'STARTED'),
        ('F', 'FINISHED'),
    )

    start_time = models.DateTimeField("Дата и время начала")
    end_time = models.DateTimeField("Дата и время окончания")
    text = models.TextField("Текст сообщения")

    filter_codes = models.ManyToManyField("RegionCode", verbose_name='Региональные коды', blank=True)
    filter_tags = models.ManyToManyField("ClientTag", verbose_name='Теги:', blank=True)

    status = models.CharField('Стастус', max_length=1, choices=STATUS_CHOICES, default='C', editable=False)

    task_id = models.CharField(verbose_name='ID задачи', max_length=37, null=True, editable=False, unique=True)

    time_interval_start = models.TimeField('Временной интервал (Старт)', blank=True,
                                           default=datetime.time(hour=0, minute=0))
    time_interval_end = models.TimeField('Временной интервал (Конец)', blank=True,
                                         default=datetime.time(hour=23, minute=59))

    def __str__(self):
        return f"{self.pk} '{self.text}' ({self.start_time} - {self.end_time})"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"


class MailingStatistic(models.Model):
    """Модель статистики по определенной рассылке"""

    mailing = models.OneToOneField(Mailing, related_name='statistic', on_delete=models.CASCADE)

    msg_count = models.PositiveIntegerField(verbose_name='Общее кол-во сообщений', null=True)
    created_count = models.PositiveIntegerField(verbose_name="Кол-во созданных ", null=True)
    sent_count = models.PositiveIntegerField(verbose_name='Кол-во отправленных', null=True)
    delivered_count = models.PositiveIntegerField(verbose_name="Кол-во доставленных", null=True)
    errors_count = models.PositiveIntegerField(verbose_name="Кол-во НЕдоставленных", null=True)
    is_overed_count = models.PositiveIntegerField(verbose_name="Кол-во НЕдоставленных (по времени)", null=True)
    is_limited_count = models.PositiveIntegerField(verbose_name="Кол-во НЕдоставленных (по временному интервалу)",
                                                   null=True)

    report = models.TextField(verbose_name='Отчет')

    def __str__(self):
        return self.mailing.pk

    class Meta:
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистики'


class Client(models.Model):
    """ Модель клиента"""

    phone = models.CharField(verbose_name="Номер телефона", max_length=11, unique=True)
    region_code = models.ForeignKey("RegionCode",
                                    on_delete=models.SET_NULL,
                                    related_name='client',
                                    editable=False, null=True
                                    )

    tags = models.ManyToManyField("ClientTag", blank=True)

    timezone = models.IntegerField(verbose_name="Часовой пояс", default=0)

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Message(models.Model):
    """Модель сообщения"""

    STATUS = (
        ('CREATED', 'СОЗДАНО'),
        ('SENT', 'ОТПРАВЛЕНО'),
        ('200', 'ДОСТАВЛЕНО'),
        ('400', 'НЕ ДОСТАВЛЕНО'),
        ('IS_OVER', "ВРЕМЯ ВЫШЛО"),
        ('LIMITED', "ВРЕМЕННОЙ ИНТЕРВАЛ")
    )

    start_time = models.DateTimeField("Дата и время начала", null=True, editable=True)
    status = models.CharField("Статус", max_length=10, choices=STATUS, default='CREATED')
    mailing = models.ForeignKey(Mailing,
                                related_name='messages',
                                on_delete=models.SET_NULL,
                                null=True
                                )
    client = models.ForeignKey(Client,
                               related_name='message',
                               on_delete=models.SET_NULL,
                               null=True
                               )

    def __str__(self):
        return f"{self.client.phone} - {self.status} ({self.start_time})"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class ClientTag(models.Model):
    """Модель тэгов"""

    tag = models.CharField(verbose_name='Тэг', max_length=10, primary_key=True)

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"


class RegionCode(models.Model):
    """Модель регионального кода мобильного оператора"""

    code = models.CharField("Код", max_length=3, primary_key=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Код региона"
        verbose_name_plural = "Коды регионов"

