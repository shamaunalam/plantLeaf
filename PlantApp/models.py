from django.db import models

# Create your models here.
class Inferences(models.Model):

    image =  models.ImageField(upload_to='leafImages',blank=False)
    prediction = models.TextField(max_length=100,blank=False)

    def __str__(self):
        return self.prediction