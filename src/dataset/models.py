from django.db import models

class DataSet(models.Model):
    SEX_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    EMBARKED_CHOICES = [
        ('C', 'Cherbourg'),
        ('Q', 'Queenstown'),
        ('S', 'Southampton'),
    ]

    SURVIVED_CHOICES = [
        (0, 'No'),
        (1, 'Yes'),
    ]

    CLASS_CHOICES = [
        (1, 'First Class'),
        (2, 'Second Class'),
        (3, 'Third Class'),
    ]

    passenger_id = models.AutoField(primary_key=True)
    survived = models.IntegerField(choices=SURVIVED_CHOICES)
    passenger_class = models.IntegerField(choices=CLASS_CHOICES)
    name = models.CharField(max_length=255)
    sex = models.CharField(max_length=6, choices=SEX_CHOICES)
    age = models.IntegerField(null=True, blank=True)
    sib_sp = models.IntegerField(default=0)
    parch = models.IntegerField(default=0)
    ticket = models.CharField(max_length=20)
    fare = models.DecimalField(max_digits=8, decimal_places=2)
    cabin = models.CharField(max_length=20, null=True, blank=True)
    embarked = models.CharField(max_length=1, choices=EMBARKED_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({'Survived' if self.survived else 'Did not survive'})"

    class Meta:
        db_table = "titanic_dataset"
        verbose_name = "Passenger"
        verbose_name_plural = "Passengers"
