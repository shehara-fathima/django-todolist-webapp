from django.db import models

# Create your models here.
class regmodel(models.Model):

    name = models.CharField(max_length=15,unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=10)
    cpass = models.CharField(max_length=10)

class TaskModel(models.Model):
    user=models.ForeignKey(regmodel,on_delete=models.CASCADE,related_name='tasks',null=True,blank=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]
    CATEGORY_CHOICES = [
        ('Work','Work'),
        ('Personal','Personal'),
        ('Other','Other'),
    ]
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=300)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

class Drawing(models.Model):
    user = models.ForeignKey(regmodel, on_delete=models.CASCADE, related_name='drawings', null=True, blank=True)
    image=models.ImageField(upload_to='drawings/')
