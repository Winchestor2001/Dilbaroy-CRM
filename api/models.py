from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):
    full_name = models.CharField(max_length=200, verbose_name="Ф.И.О")

    def __str__(self) -> str:
        return f"{self.full_name}"

    class Meta:
        verbose_name = "Доктор"
        verbose_name_plural = "Докторлар"


class Service(models.Model):
    service_name = models.CharField(max_length=200, verbose_name="Номи")
    service_price = models.FloatField(default=0, verbose_name="Нархи")

    def __str__(self) -> str:
        return f"{self.service_name}"

    class Meta:
        verbose_name = "Хизмат тури"
        verbose_name_plural = "Хизмат турлари"


class RoomType(models.Model):
    room_type = models.CharField(max_length=150, verbose_name="Хона тури")

    def __str__(self) -> str:
        return str(self.room_type)

    class Meta:
        verbose_name = "Хона тури"
        verbose_name_plural = "Хона турлари"


class Room(models.Model):
    COMFORTABLE = (
        ('Lux', 'Lux'),
        ('Oddiy', 'Oddiy'),
    )
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, verbose_name="Хона тури")
    room_number = models.CharField(max_length=150, verbose_name="Ракам")
    room_personal = models.IntegerField(verbose_name="Сигим")
    room_patients = models.IntegerField(default=0, verbose_name="Буш")
    room_price = models.FloatField(verbose_name="Нархи")
    room_comfortable = models.CharField(max_length=150, choices=COMFORTABLE, verbose_name="Кулайлиги")

    def __str__(self) -> str:
        return str(self.room_number)

    class Meta:
        ordering = ('room_number',)
        verbose_name = "Хона"
        verbose_name_plural = "Хоналар"

    def save(self, *args, **kwargs):
        self.room_patients = self.room_personal
        super().save(*args, **kwargs)


class Patient(models.Model):
    slug_name = models.CharField(max_length=200, null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name="Доктор")
    full_name = models.CharField(max_length=200, verbose_name="Ф.И.О")
    pass_data = models.CharField(max_length=50, null=True, blank=True, verbose_name="Паспорт сериа")
    phone_number = models.CharField(max_length=50, verbose_name="Тел. ракам")
    address = models.CharField(max_length=255, verbose_name="Манзил")
    workplace = models.CharField(max_length=200)
    birthday = models.DateField(null=True, verbose_name="Тугилган сана")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Руйхатдан утган сана")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Хона раками")
    duration = models.IntegerField(blank=True, null=True, verbose_name="Муддати")
    service = models.ManyToManyField(Service, null=True, blank=True, verbose_name="Хизмат турлари")
    food = models.ForeignKey("Food", on_delete=models.CASCADE, null=True, blank=True, verbose_name="Таом")
    food_amount = models.FloatField(default=0, verbose_name="Таом нархи")
    food_duration = models.IntegerField(blank=True, null=True, verbose_name="Таом Муддати")
    from_date = models.DateTimeField(blank=True, null=True, verbose_name="Хона бант килинган сана")
    food_refund = models.FloatField(default=0, verbose_name="Кайтарилган сумма")
    room_refund = models.FloatField(default=0, verbose_name="Кайтарилган сумма")
    total_refund = models.FloatField(default=0, verbose_name="Кайтарилган сумма")
    total_amount = models.FloatField(default=0, verbose_name="Жами сумма")
    room_status = models.BooleanField(default=False, verbose_name="Хона")

    def __str__(self) -> str:
        return str(self.full_name)

    class Meta:
        verbose_name = "Бемор"
        verbose_name_plural = "Беморлар"


class Food(models.Model):
    food = models.CharField(max_length=200, blank=True, null=True, verbose_name="Таомнома")
    food_price = models.FloatField(default=0, verbose_name="Таомнома нархи")

    def __str__(self) -> str:
        return str(self.food)

    class Meta:
        verbose_name = "Бемор таоми"
        verbose_name_plural = "Беморлар таоми"

