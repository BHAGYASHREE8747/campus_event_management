from django.db import models

class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    college_id = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    event_type = models.CharField(max_length=100)
    date = models.DateField()
    college_id = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Registration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'event')  # prevent duplicate registrations


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    class Meta:
        unique_together = ('student', 'event')  # one attendance record per student-event


class Feedback(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    rating = models.IntegerField()

    class Meta:
        unique_together = ('student', 'event')  # one feedback per student-event
