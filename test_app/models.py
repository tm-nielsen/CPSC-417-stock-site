from django.db import models

# Create your models here.
class Exchange(models.Model):
    exchange_timezone = models.TextField(null=True)
    exchange_id = models.TextField(primary_key=True)


class Stock(models.Model):
    name = models.TextField(null=True)
    current_value = models.FloatField(null=True)
    ticker = models.TextField(primary_key=True)
    ex_dividend_date = models.DateField(null=True)
    dividend_amount = models.FloatField(null=True)
    exchange_id = models.ForeignKey(
        'Exchange',
        on_delete=models.CASCADE,
        null=True
    )

class Put(models.Model):
    expiry_date = models.DateField()
    strike_price = models.FloatField()
    bid = models.FloatField(null=True)
    ask = models.FloatField(null=True)
    premium = models.FloatField(null=True)
    ticker = models.ForeignKey(
        'Stock',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = (("expiry_date", "strike_price", "ticker"),)
    
class Call(models.Model):
    expiry_date = models.DateField()
    strike_price = models.FloatField()
    bid = models.FloatField(null=True)
    ask = models.FloatField(null=True)
    premium = models.FloatField(null=True)
    ticker = models.ForeignKey(
        'Stock',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = (("expiry_date", "strike_price", "ticker"),)


class Value_History(models.Model):
    date = models.DateTimeField()
    value = models.FloatField(null=True)
    ticker = models.ForeignKey(
        'Stock',
        on_delete=models.CASCADE
    )
    class Meta:
        unique_together = (('date','ticker'))

class Histogram_Entry(models.Model):
    value = models.FloatField(null=True)
    id = models.OneToOneField(
        'Value_History',
        on_delete=models.CASCADE,
        primary_key = True
    )

class User(models.Model):
    username = models.TextField(primary_key=True)
    email = models.TextField(null=True)
    name = models.TextField(null=True)
    password = models.TextField(null=True)

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
    email = models.TextField(null=True)
    name = models.TextField(null=True)
    password = models.TextField(null=True)

class Analysis(models.Model):
    description = models.TextField(null=True)
    date = models.DateField(null=True)
    title = models.TextField(primary_key=True)
    username = models.ForeignKey(
        'Analyst',
        on_delete=models.CASCADE
        )
    class Meta:
        unique_together = (('title', 'username'),)

