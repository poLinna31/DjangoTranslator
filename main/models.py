from django.db import models

class TranslateHistory(models.Model):
    src_value = models.CharField(max_length=1000)
    trans_value = models.CharField(max_length=1000)    
    src_lang = models.CharField(max_length=10, default='')
    trans_lang = models.CharField(max_length=10, default='')


class Language(models.Model):
    alias = models.CharField(max_length=1000)
    name = models.CharField(max_length=1000)
    
    def __init__(self, name, alias):
        self.name = name
        self.alias = alias
            
    def __str__(self):
        return self.name + ' ' + self.alias
    