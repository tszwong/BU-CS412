from django.db import models

# Create your models here.
class Person(models.Model):
    """
        
    """

    name = models.CharField(max_length=120)
    ssn = models.CharField(max_length=9)

    def __str__(self):
        return self.name
    

class BankAccount(models.Model):
    account_num = models.IntegerField()
    balance = models.FloatField()
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.person}'s account - {self.account_num}"


class Student(models.Model):
    name = models.CharField(max_length=120)
    # courses = models.ManyToManyField('Course')

    def __str__(self):
        return self.name
    

class Course(models.Model):

    name = models.CharField(max_length=120)
    number = models.CharField(max_length=10)
    # students = models.ManyToManyField(Student)
    # teacher, meeting time, etc

    def __str__(self):
        return self.name
    

class Registration(models.Model):
    """
        implement many-to-many relationship between Student and Course
    """

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student} - {self.course}"
    

    def get_students_for_course(self, course):
        return Registration.objects.filter(course=course)
    

class FamilyPerson(models.Model):
    """
        a person within a family tree
    """

    name = models.CharField(max_length=120)
    dob = models.DateField()
    
    # define parent relationship, recursive foreign keys/relationships
    mother = models.ForeignKey('FamilyPerson', on_delete=models.CASCADE, related_name='mother_of',
                                null=True, blank=True) # makes it optional
    father = models.ForeignKey('FamilyPerson', on_delete=models.CASCADE, related_name='father_of',
                               null=True, blank=True) # makes it optional

    def __str__(self):
        return self.name