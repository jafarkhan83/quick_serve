from django.db import models

# Create your models here.

class User(models.Model):
    __tablename__ = 'users'

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

class ServiceProfile(models.Model):
    __tablename__ = 'service_profiles'

    service_provider = models.ForeignKey(User, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service_name} ({self.service_provider})"

class Order(models.Model):
    __tablename__ = 'orders'

    client = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(ServiceProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order for {self.client} - {self.service} by {self.service.service_provider}"