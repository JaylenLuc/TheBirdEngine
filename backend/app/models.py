from django.db import models

# Create your models here.
class Data(models.Model):
    text_query = models.CharField(max_length = 30)
    def __str__(self):
        return self.text_query
    class Meta:
        db_table = 'text_query'