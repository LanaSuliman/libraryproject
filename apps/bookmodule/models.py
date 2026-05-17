from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200)
    DOB = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)


    author = models.CharField(max_length=50, blank=True, null=True)

    price = models.FloatField(default=0.0)


    edition = models.SmallIntegerField(default=1)


    quantity = models.IntegerField(default=1)
    pubdate = models.DateTimeField(null=True, blank=True)
    rating = models.SmallIntegerField(default=1)
    publisher = models.ForeignKey(Publisher, null=True, blank=True, on_delete=models.SET_NULL)
    authors = models.ManyToManyField(Author, blank=True)

    def __str__(self):
        return self.title


class Address(models.Model):
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.city


class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Address2(models.Model):
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.city


class Student2(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    addresses = models.ManyToManyField(Address2, blank=True)

    def __str__(self):
        return self.name
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField(default=0.0)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name