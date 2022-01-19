from django.db import models
from datetime import date, datetime
from django.urls import reverse

from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """
    Пользователи

    Таблица данных о пользователе связанная
    напрямую с встроенной таблицей User
    """

    CHOICES_GENDER = (
        ('Мужской', 'Мужской'),
        ('Женский', 'Женский'),
        ('Не указано', 'Не указано')
    )

    id_user = models.AutoField("ID-пользователя", primary_key=True)
    login = models.OneToOneField(User, verbose_name="Логин", on_delete=models.CASCADE, unique=True)

    # Basic info about User #
    sur_name = models.CharField("Фамилия", max_length=50)
    name = models.CharField("Имя", max_length=50)
    patronymic = models.CharField("Отчество", max_length=50)

    gender = models.CharField("Пол", max_length=10, default="Не указано", choices=CHOICES_GENDER)

    # Position #
    region = models.CharField("Область", max_length=50)  # Можно сделать ENUM областей
    city = models.CharField("Город (Село)", max_length=50)  # Можно сделать ENUM, связаное с пользователем

    street = models.CharField("Улица (Переулок, Проспект)", max_length=50)  # Можно сделать ENUM улиц и переулков
    house = models.PositiveSmallIntegerField("Номер дома")

    prefix_house = models.CharField("Приставка к адресу", max_length=10, blank=True)  # На случай 107а
    flat = models.PositiveSmallIntegerField("Номер квартиры", blank=True, null=True)

    # Contacts #
    tel_number = models.CharField("Номер телефона", max_length=20)
    tel_number_extra = models.CharField("Доп. номер телефона", max_length=20, blank=True)
    email = models.EmailField("Эл. почта", max_length=50, blank=True)

    def __str__(self):
        return 'ID:%s - %s - %s %s %s' % (self.id_user, self.login, self.sur_name, self.name, self.patronymic)

    class Meta:
        verbose_name = "Пользователя"
        verbose_name_plural = "Пользователи"


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


class ServiceProviders(models.Model):
    """
    Поставщики услуг

    Ограниченная таблица с всего 3 даннными -
    трое поставщиков услуг
    """

    id_provider = models.PositiveSmallIntegerField("ID поставщика услуг", primary_key=True)

    # Basic info about Service Provider #
    full_name = models.CharField("Полное имя", max_length=50)
    address = models.CharField("Адрес", max_length=50)

    # Contacts #
    tel_contact = models.CharField("Контактный телефон", max_length=20)
    tel_contact_extra = models.CharField("Доп. контактный телефон", max_length=20, blank=True)
    email = models.EmailField("Эл. почта", max_length=50, blank=True)
    email_extra = models.EmailField("Доп. эл. почта", max_length=50, blank=True)

    # Another field for route url #
    url = models.SlugField("Ссылка", max_length=20, unique=True)

    def __str__(self):
        return self.full_name

    # def get_absolute_url(self):
    #     return reverse("page_pass_cr", kwargs={"slug": self.url})

    class Meta:
        verbose_name = "Поставщика услуг"
        verbose_name_plural = "Поставщики услуг"


class Services(models.Model):
    """
    Услуги

    Отдельная таблица, которая заполняется
    самим поставщиком услуг
    """

    id_service = models.AutoField("ID Услуги", primary_key=True)
    username = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE, unique=True)

    # All about Electricity for User #
    availability_electricity = models.BooleanField("Наличие счетчика Электричества")
    account_electricity = models.CharField("Лицевой счет Электричество", max_length=50, blank=True)
    availability_electricity_night = models.BooleanField("Наличие счетчика Ночного Элестричества")
    account_electricity_night = models.CharField("Личевой счет Ночное Электричество", max_length=50, blank=True)

    # All about Water for User #
    availability_water = models.BooleanField("Наличие счетчика Воды")
    account_water = models.CharField("Лицевой счет Вода", max_length=50, blank=True)
    availability_water_irrigation = models.BooleanField("Наличие счетчика Воды для полива")
    account_water_irrigation = models.CharField("Лицевой счет Вода для полива", max_length=50, blank=True)

    # All about Gas for User #
    availability_gas = models.BooleanField("Наличие счетчика Газа")
    account_gas = models.CharField("Лицевой счет Газ", max_length=50, blank=True)

    def __str__(self):
        return 'ID:%s. %s | %s // %s | %s // %s' % \
               (self.username, self.account_electricity, self.account_electricity_night,
                self.account_water, self.account_water_irrigation, self.account_gas)

    class Meta:
        verbose_name = "Услугу"
        verbose_name_plural = "Услуги"


class LastCounterReading(models.Model):
    """
    Последнее показание счетчика

    Таблица основной информации,
    которая выводиться на главную страницу

    Заполнение происходит поставщиком,
    когда тот скидывает данные о балансе.
    А так же пользователем,
    когда он передает показания
    """

    id_reading = models.AutoField("ID-Последнего показания", primary_key=True)
    username = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE)

    # All about Electricity reading for User #
    date_electricity_cr = models.DateField("Дата последнего показания Электричество", blank=True, default=date.today)

    account_electricity = models.CharField("Лицевой счет Электричество", max_length=50, blank=True)
    last_electricity_cr = models.PositiveIntegerField(
        "Последнее показание счетчика Электричество", blank=True, null=True
    )

    account_electricity_night = models.CharField("Лицевой счет Ночное Электричество", max_length=50, blank=True)
    last_electricity_night_cr = models.PositiveIntegerField(
        "Последнее показание счетчика Ночное Электричество", blank=True, null=True
    )

    # All about Electricity balance for User #
    date_electricity_balance = models.DateField("Дата последнего баланса Электричество", blank=True, default=date.today)
    account_electricity_balance = models.IntegerField("Баланс денег Электричество", blank=True, default=0)

    # All about Water reading for User #
    date_water_cr = models.DateField("Дата последнего показания Вода", blank=True, default=date.today)

    account_water = models.CharField("Лицевой счет Вода", max_length=50, blank=True)
    last_water_cr = models.PositiveIntegerField(
        "Последнее показание счетчика Вода", blank=True, null=True
    )

    account_water_irrigation = models.CharField("Лицевой счет Вода для полива", max_length=50, blank=True)
    last_water_irrigation_cr = models.PositiveIntegerField(
        "Последнее показание счетчика Вода для полива", blank=True, null=True
    )

    # All about Water balance for User #
    date_water_balance = models.DateField("Дата последнего баланса Вода", blank=True, default=date.today)
    account_water_balance = models.IntegerField("Баланс денег Вода", blank=True, default=0)

    # All about Gas reading for User #
    date_gas_cr = models.DateField("Дата последнего показания Газ", blank=True, default=date.today)

    account_gas = models.CharField("Лицевой счет Газ", max_length=50, blank=True)
    last_gas_cr = models.PositiveIntegerField(
        "Последнее показание счетчика Газ", blank=True, null=True
    )

    # All about Gas balance for User #
    date_gas_balance = models.DateField("Дата последнего баланса Газ", blank=True, default=date.today)
    account_gas_balance = models.IntegerField("Баланс денег Газ", blank=True, default=0)

    def __str__(self):
        return 'ID:%s' % self.username

    class Meta:
        verbose_name = "Последнее показание счетчика"
        verbose_name_plural = "Последние показания счетчика"


class HistoryGasCR(models.Model):
    """
    История передачи показаний по газу

    Большая таблица, которая заполняется
    пользователем на отдельной странице сайта
    """

    id_reading = models.AutoField("ID показания", primary_key=True)
    username = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)

    # Account with DB Services
    first_account = models.CharField("Лицевой счет Газ", max_length=50, default="RJ_545-45")

    # All about data reading Gas
    date_cr = models.DateField("Дата передачи показаний", default=date.today)
    first_cr = models.PositiveIntegerField("Показание счетчика по газу")

    # Hidden date recording
    date_recording = models.DateTimeField("Дата записи в БД показания", auto_now=True)

    def __str__(self):
        return 'ID-User:%s / ID-Показания:%s' % (self.username, self.id_reading)

    class Meta:
        verbose_name = "Историю показаний счетчика газа"
        verbose_name_plural = "История показаний счетчика газа"


class HistoryElectricityCR(models.Model):
    """
    История передачи показаний по свету

    Большая таблица, которая заполняется
    пользователем на отдельной странице сайта
    """

    id_reading = models.AutoField("ID показания", primary_key=True)
    username = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)

    # Account with DB Services
    first_account = models.CharField("Лицевой счет Электричество", max_length=50, default="RJ_545-45")
    second_account = models.CharField("Лицевой счет Ночное Электричество", max_length=50, blank=True, null=True)

    # All about data reading Electricity
    date_cr = models.DateField("Дата передачи показаний", default=date.today)
    first_cr = models.PositiveIntegerField("Показание дневного счетчика")
    second_cr = models.PositiveIntegerField("Показание ночного счетчика", blank=True, null=True)

    # Hidden date recording
    date_recording = models.DateTimeField("Дата записи в БД показания", auto_now=True)

    def __str__(self):
        return 'ID-User:%s / ID-Показания:%s' % (self.username, self.id_reading)

    class Meta:
        verbose_name = "Историю показаний счетчика электричество"
        verbose_name_plural = "Истории показаний счетчика электричество"


class HistoryWaterCR(models.Model):
    """
    История передачи показаний по воде

    Большая таблица, которая заполняется
    пользователем на отдельной странице сайта
    """

    id_reading = models.AutoField("ID показания", primary_key=True)
    username = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)

    # Account with DB Services
    first_account = models.CharField("Лицевой счет Вода", max_length=50, blank=True, default="RJ_545-45")
    second_account = models.CharField("Лицевой счет Вода для полива", max_length=50, blank=True)

    # All about data reading Water
    date_cr = models.DateField("Дата передачи показаний", default=date.today)
    first_cr = models.PositiveIntegerField("Показание счетчика питьевой воды")
    second_cr = models.PositiveIntegerField("Показание счетчика воды для полива", blank=True, null=True)

    # Hidden date recording
    date_recording = models.DateTimeField("Дата записи в БД показания", auto_now=True)

    def __str__(self):
        return 'ID-User:%s / ID-Показания:%s' % (self.username, self.id_reading)

    class Meta:
        verbose_name = "Историю показаний счетчика воды"
        verbose_name_plural = "История показаний счетчика воды"
