from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class University(models.Model):
    name = models.CharField(max_length=200, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)  # Dropdown from Country model
    city = models.CharField(max_length=100)  # Manually entered city
    university_type = models.CharField(
        max_length=10,
        choices=[('public', 'Public'), ('private', 'Private')],
        default='public'
    )

    def __str__(self):
        return f'{self.name}, {self.city}, {self.country.name}'
class Program(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    PROGRAM_LEVEL_CHOICES = [
        ('bachelors', 'Bachelors'),
        ('masters', 'Masters'),
    ]
    level = models.CharField(max_length=10, choices=PROGRAM_LEVEL_CHOICES)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"

    
