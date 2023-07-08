from django.db import models


class Tariff(models.Model):
    name = models.CharField('название тарифа', max_length=30, primary_key=True)
    meets = models.IntegerField('количество встреч в неделю')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'


class Psychologist(models.Model):
    name = models.CharField('имя', max_length=30)
    tg_link = models.CharField('ссылка на летеграм', max_length=30, default='')
    age = models.IntegerField('возраст')
    description = models.TextField('о психологе', max_length=1000)
    photo = models.ImageField('путь к фото', max_length=100, default="")
    meet_price = models.IntegerField('стоимость сеанас Р', default=0)
    average_score = models.IntegerField('Средняя оценка', default=0)
    likes = models.IntegerField('оценки нравится', default=0)
    approved = models.BooleanField('содержание профиля проверено', default=False)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Психолог'
        verbose_name_plural = 'Психологи'


class Specialization(models.Model):
    name = models.CharField('название специализации', max_length=30)
    psychologists_specializations = models.ManyToManyField(Psychologist)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'


class Client(models.Model):
    tg_id = models.IntegerField('id телеграмм аккаунта клиента', primary_key=True)
    name = models.CharField('имя', max_length=30)
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE, null=True, blank=True, default=None)
    remaining_meets = models.IntegerField('cеансов осталось', default=0)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Schedule(models.Model):
    psychologist = models.ForeignKey(Psychologist, on_delete=models.CASCADE, null=True, blank=True, default=None)
    day_of_the_week = models.CharField('День недели', max_length=20, unique=True)

    def __str__(self):
        return str((str(self.day_of_the_week), str(self.psychologist)))

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'


class Meet(models.Model):
    time_start = models.TimeField('Начало сеанса', null=True, default=None)
    time_end = models.TimeField('Конец сеанса', null=True, default=None)
    day_of_the_week = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=True, blank=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str((str(self.day_of_the_week), str(self.time_start), str(self.time_end)))

    class Meta:
        verbose_name = 'Сеанс'
        verbose_name_plural = 'Сеансы'
