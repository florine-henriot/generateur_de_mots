from django.db import models

# Create your models here.

class EnNoun(models.Model):
    en_noun = models.TextField()
    def __str__(self):
        return self.en_noun
