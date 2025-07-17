from django.db import models

class Holiday(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField(unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} - {self.date}"
