from django.db import models


# Create your models here.
class CoreModel(models.Model):
    """ Core Model Definition """

    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    class Meta:
        """ 
        Abstract base classes로 만들어 
        데이터베이스테는 올라가지 않는 모델이다.
        """

        abstract = True
