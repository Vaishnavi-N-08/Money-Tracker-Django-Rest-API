from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Transaction(models.Model):
    amount = models.FloatField()
    title = models.CharField(max_length=100)
    split_between_users = models.ManyToManyField(User, related_name='transactions')
    paid_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='paid_by')

    def __str__(self):
        return str(self.title) + str(self.pk)

