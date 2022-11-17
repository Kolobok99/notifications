# Generated by Django 4.1.2 on 2022-11-17 11:04

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=11, unique=True, verbose_name='Номер телефона')),
                ('timezone', models.IntegerField(default=0, verbose_name='Часовой пояс')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.CreateModel(
            name='ClientTag',
            fields=[
                ('tag', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='Тэг')),
            ],
            options={
                'verbose_name': 'Тэг',
                'verbose_name_plural': 'Тэги',
            },
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(verbose_name='Дата и время начала')),
                ('end_time', models.DateTimeField(verbose_name='Дата и время окончания')),
                ('text', models.TextField(verbose_name='Текст сообщения')),
                ('status', models.CharField(choices=[('C', 'CREATED'), ('S', 'STARTED'), ('F', 'FINISHED')], default='C', editable=False, max_length=1, verbose_name='Стастус')),
                ('task_id', models.CharField(editable=False, max_length=37, null=True, unique=True, verbose_name='ID задачи')),
                ('time_interval_start', models.TimeField(blank=True, default=datetime.time(0, 0), verbose_name='Временной интервал (Старт)')),
                ('time_interval_end', models.TimeField(blank=True, default=datetime.time(23, 59), verbose_name='Временной интервал (Конец)')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки',
            },
        ),
        migrations.CreateModel(
            name='RegionCode',
            fields=[
                ('code', models.CharField(max_length=3, primary_key=True, serialize=False, verbose_name='Код')),
            ],
            options={
                'verbose_name': 'Код региона',
                'verbose_name_plural': 'Коды регионов',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(null=True, verbose_name='Дата и время начала')),
                ('status', models.CharField(choices=[('CREATED', 'СОЗДАНО'), ('SENT', 'ОТПРАВЛЕНО'), ('200', 'ДОСТАВЛЕНО'), ('400', 'НЕ ДОСТАВЛЕНО'), ('IS_OVER', 'ВРЕМЯ ВЫШЛО'), ('LIMITED', 'ВРЕМЕННОЙ ИНТЕРВАЛ')], default='CREATED', max_length=10, verbose_name='Статус')),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='message', to='mailings.client')),
                ('mailing', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='messages', to='mailings.mailing')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
            },
        ),
        migrations.CreateModel(
            name='MailingStatistic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg_count', models.PositiveIntegerField(null=True, verbose_name='Общее кол-во сообщений')),
                ('created_count', models.PositiveIntegerField(null=True, verbose_name='Кол-во созданных ')),
                ('sent_count', models.PositiveIntegerField(null=True, verbose_name='Кол-во отправленных')),
                ('delivered_count', models.PositiveIntegerField(null=True, verbose_name='Кол-во доставленных')),
                ('errors_count', models.PositiveIntegerField(null=True, verbose_name='Кол-во НЕдоставленных')),
                ('is_overed_count', models.PositiveIntegerField(null=True, verbose_name='Кол-во НЕдоставленных (по времени)')),
                ('is_limited_count', models.PositiveIntegerField(null=True, verbose_name='Кол-во НЕдоставленных (по временному интервалу)')),
                ('report', models.TextField(verbose_name='Отчет')),
                ('mailing', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='statistic', to='mailings.mailing')),
            ],
            options={
                'verbose_name': 'Статистика',
                'verbose_name_plural': 'Статистики',
            },
        ),
        migrations.AddField(
            model_name='mailing',
            name='filter_codes',
            field=models.ManyToManyField(blank=True, to='mailings.regioncode', verbose_name='Региональные коды'),
        ),
        migrations.AddField(
            model_name='mailing',
            name='filter_tags',
            field=models.ManyToManyField(blank=True, to='mailings.clienttag', verbose_name='Теги:'),
        ),
        migrations.AddField(
            model_name='client',
            name='region_code',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='client', to='mailings.regioncode'),
        ),
        migrations.AddField(
            model_name='client',
            name='tags',
            field=models.ManyToManyField(blank=True, to='mailings.clienttag'),
        ),
    ]