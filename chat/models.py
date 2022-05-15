from django.db import models
from members.models import Account



class FriendRequest(models.Model):
    sender_account = models.ForeignKey(Account, related_name="sender_account", on_delete=models.CASCADE)
    receiver_account = models.ForeignKey(Account, related_name="receiver_account", on_delete=models.CASCADE)


    def __str__(self):
        return (f'{self.sender_account.username} to {self.receiver_account}')


class PublicMessage(models.Model):
    sender = models.ForeignKey(Account, on_delete = models.CASCADE)
    message_content = models.TextField(blank = False, null = False)
    date_added = models.DateTimeField(auto_now_add = True)


    class Meta:
        ordering = ['date_added']