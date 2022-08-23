from django.contrib.auth.models import User
from django.db import models

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64, blank=False)
    description = models.TextField(blank=True)
    complete = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pk}) {self.title}: {self.description} | created @{self.created_on}"
    
    class Meta:
        # send complete tasks to the end of the list, order by creation date ascending 
        ordering = ['complete', 'created_on']