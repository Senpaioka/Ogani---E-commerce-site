from django.db import models

# Create your models here.


class ContactInfoModel(models.Model):

    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    open_time = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    



class ContactFormModel(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    message_body = models.TextField()
    sending_time = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name
    

    





class NewsLetterModel(models.Model):
    email = models.EmailField(max_length=100)
    send_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    




