from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=50, default="Name", null=False)
    description = models.CharField(max_length=500, default="Description", null=False)

    def __str__(self):
        return 'Name: ' + self.name + ', Description: ' + self.description

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    CHOICES = [
        ('sedan', 'Sedan'),
        ('suv', "SUV"),
        ('wagon', 'Wagon'),
        ('other', 'Other')
    ]
    carmake = models.ForeignKey(CarMake, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, null=False, default="Model")
    dealerId = models.IntegerField(null=True)
    cartype = models.CharField(max_length=20, null=False, choices=CHOICES, default='sedan')
    year = models.DateField(null=True)

    def __str__(self):
        return self.name


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
