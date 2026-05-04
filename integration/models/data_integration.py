from django.db import models



class TimeStamp(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Integration(TimeStamp):
    SOURCE_TYPES = (('Sage','Sage'), ('Other', 'Other'))
    
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    host = models.URLField(max_length=100)
    key= models.CharField(max_length=200)
    endpoint = models.CharField(max_length=500)
    source = models.CharField(max_length=100, choices=SOURCE_TYPES)
    is_active = models.BooleanField(default=True)
    

    def __str__(self):
        return self.host
    
        
    def get_data(self):
        pass

    def get_data_keys(self):
        pass
