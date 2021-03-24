from django.db import models

# Create your models here.
class Exchange(models.Model):
    names = models.TextField()
    exchange_id = models.TextField(primary_key=True)
    class Meta:
        unique_together = (('names', 'exchange_id'))


class Stock(models.Model):
    name = models.TextField()
    current_value = models.FloatField()
    ticker = models.TextField(primary_key=True)
    dividend_date = models.DateField()
    dividend_amount = models.FloatField()
    exchange_id = models.ForeignKey(
        'Exchange',
        on_delete=models.CASCADE
    )

class Put(models.Model):
    expiry_date = models.DateField()
    strike_price = models.FloatField()
    bid = models.FloatField()
    ask = models.FloatField()
    premium = models.FloatField()
    ticker = models.ForeignKey(
        'Stock',
        on_delete=models.CASCADE
    )
    
class Call(models.Model):
    expiry_date = models.DateField()
    strike_price = models.FloatField()
    bid = models.FloatField()
    ask = models.FloatField()
    premium = models.FloatField()
    ticker = models.ForeignKey(
        'Stock',
        on_delete=models.CASCADE
    )

class Value_History(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateTimeField()
    value = models.FloatField()
    ticker = models.ForeignKey(
        'Stock',
        on_delete=models.CASCADE
    )
    class Meta:
        unique_together = (('date','ticker'))

class Histogram(models.Model):
    median = models.FloatField()
    quartiles = models.FloatField()
    id = models.OneToOneField(
        'Value_History',
        on_delete=models.CASCADE,
        primary_key = True
    )

class User(models.Model):
    username = models.TextField(primary_key=True)
    email = models.TextField()
    name = models.TextField()
    password = models.TextField()

class Viewed_History(models.Model):
    date_viewed = models.DateTimeField()
    username = models.ForeignKey(
        'User',
        on_delete=models.CASCADE
    )
    ticker = models.ForeignKey(
        'Stock',
        on_delete=models.CASCADE
    )
    class Meta:
        unique_together = (('date_viewed', 'username', 'ticker'))

class Watchlist_Entry(models.Model):
    ticker = models.ForeignKey(
        'Stock',
        on_delete=models.CASCADE
    )
    username = models.ForeignKey(
        'User',
        on_delete=models.CASCADE
    )

class Analyst(models.Model):
    username = models.TextField(primary_key=True)
    email = models.TextField()
    name = models.TextField()
    password = models.TextField()

class Analysis(models.Model):
    description = models.TextField()
    approval = models.IntegerField()
    date = models.DateField()
    title = models.TextField(primary_key=True)
    username = models.ForeignKey(
        'Analyst',
        on_delete=models.CASCADE
        )
    class Meta:
        unique_together = (('title', 'username'),)

class Stock_Analysis(models.Model):
    title = models.ForeignKey(
        'Analysis',
        on_delete=models.CASCADE
    )
    username = models.ForeignKey(
        'Analyst',
        on_delete=models.CASCADE
    )
    ticker = models.ForeignKey(
        'Stock',
        on_delete=models.CASCADE
    )
    class Meta:
        unique_together = (('title', 'username'))

class Survey(models.Model):
    date = models.DateField()
    questions = models.TextField()
    answer = models.TextField()
    sentiment = models.SmallIntegerField()
    survey_id = models.IntegerField(primary_key=True)
    u_username = models.ForeignKey(
        'User',
        on_delete=models.CASCADE
    )
    a_username = models.ForeignKey(
        'Analyst',
        on_delete=models.CASCADE
    )
    class Meta:
        unique_together = (('survey_id', 'u_username'))