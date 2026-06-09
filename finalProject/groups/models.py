from django.db import models
from django.core.exceptions import ValidationError

class group(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, null=True, blank=True)
    openGradeBook = models.BooleanField(default=False, blank=True)
    
    owner = models.ForeignKey(
        'users.User', 
        on_delete=models.CASCADE, 
        related_name='ownedGroups' 
    )

    teachers = models.ManyToManyField('users.User', related_name='teachers', blank=True)
    students = models.ManyToManyField('users.User', related_name='students', blank=True)

    def save(self, *args, **kwargs):

        if self.pk:
            if self.teachers.filter(pk=self.owner.pk).exists():
                raise ValidationError({'teachers': 'Group owner is in the teacher field.'})
            
            if self.students.filter(pk=self.owner.pk).exists():
                raise ValidationError({'students': 'Group owner is in the student field.'})
            
            if self.teachers.filter(pk__in=self.students.all()).exists():
                raise ValidationError('A user is in both teacher and student fields.')
            
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

            if self.teachers.filter(pk=self.owner.pk).exists():
                self.delete()
                raise ValidationError({'teachers': 'Group owner is in the teacher field.'})
            
            if self.students.filter(pk=self.owner.pk).exists():
                self.delete()
                raise ValidationError({'students': 'Group owner is in the student field.'})
            
            if self.teachers.filter(pk__in=self.students.all()).exists():
                self.delete()
                raise ValidationError('A user is in both teacher and student fields.')
        
    def getUserRelation(self, user) -> str | None:
        if self.owner.id == user.id:
            return 'owner'
        if self.teachers.filter(id=user.id).exists():
            return 'teacher'
        if self.students.filter(id=user.id).exists():
            return 'student'
        return None
            
    def __str__(self) -> str:
        return self.title

class assignmentGroup(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100, blank=True, null=True)
    
    group = models.ForeignKey(
        group, 
        on_delete=models.CASCADE, 
        related_name='assignmentGroups'
    )

    def save(self, *args, **kwargs):
        if self.subtitle == None:
            self.subtitle = ''

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.group.title} - {self.title}'


class assignment(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    isHidden = models.BooleanField(default=True, blank=True)

    gradeMax = models.FloatField(
        null=True, 
        blank=True
    )

    '''
    Submittable = Assignment can be submitted once
    Resubmittable = Assignment can be resubmitted unlimited times
    Unsubmittable = Not able to be submitted
    '''
    assignmentTypeChoices = [
        ('submittable', 'Submittable'),
        ('resubmittable', 'Resubmittable'),
        ('unsubmittable', 'Unsubmittable')
    ]
    assignmentType = models.CharField(choices=assignmentTypeChoices, max_length=20, default='submittable')

    assignmentGroup = models.ForeignKey(
        assignmentGroup, 
        on_delete=models.CASCADE, 
        related_name='assignments'
    )

    def save(self, *args, **kwargs) -> None:
        if self.gradeMax is not None:
            self.gradeMax = round(self.gradeMax, 3)
            
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title
    
class submission(models.Model):
    assignment = models.ForeignKey(
        'assignment', 
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    
    student = models.ForeignKey(
        'users.User', 
        on_delete=models.CASCADE,
        related_name='submissionStudents'
    )
    
    # CDR
    submittedFileContent = models.TextField(max_length=1300000, blank=True, null=True)
    originalFileName = models.CharField(max_length=255, blank=True, null=True)
    submittedText = models.TextField(max_length=100000, blank=True, null=True)
    
    submittedAt = models.DateTimeField(auto_now_add=True)
    isGraded = models.BooleanField(default=False, blank=True)

    grade = models.FloatField(
        null=True, 
        blank=True,
        default=None
    )

    teacherFeedback = models.TextField(max_length=10000, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.student.username} - {self.assignment.title}'