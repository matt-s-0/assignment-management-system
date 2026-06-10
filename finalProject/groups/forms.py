from django import forms
from .models import group, assignmentGroup, assignment, submission
from users.models import User

class groupForm(forms.ModelForm):

    teachers = forms.CharField(required=False, widget=forms.TextInput())
    students = forms.CharField(required=False, widget=forms.TextInput())

    class Meta:
        model = group
        # auto set: owner
        fields = ['title', 'description', 'openGradeBook', 'teachers', 'students']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):

        cleanedData = super().clean()

        tEmails = [e.strip().lower() for e in cleanedData.get('teachers', '').split(',') if e.strip()]
        sEmails = [e.strip().lower() for e in cleanedData.get('students', '').split(',') if e.strip()]

        overlapping_emails = set(tEmails).intersection(set(sEmails))
        if overlapping_emails:
            self.add_error('teachers', 'A user cannot be in both the teacher and student fields.')

        owner = self.user or (self.instance.owner if (self.instance and hasattr(self.instance, 'owner')) else None)

        if owner and getattr(owner, 'email', None):
            owner_email = owner.email.strip().lower()
            
            if owner_email in tEmails:
                self.add_error('teachers', 'The group owner cannot be added as a teacher.')
                
            if owner_email in sEmails:
                self.add_error('students', 'The group owner cannot be added as a student.')

        return cleanedData

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if commit:
            instance.save()

        tEmails = [e.strip() for e in self.cleaned_data.get('teachers', '').split(',') if e.strip()]
        sEmails = [e.strip() for e in self.cleaned_data.get('students', '').split(',') if e.strip()]

        if commit:
            instance.teachers.set(User.objects.filter(email__in=tEmails))
            instance.students.set(User.objects.filter(email__in=sEmails))
            self.save_m2m = lambda: None
        else:
            def save_m2m_custom():
                instance.teachers.set(User.objects.filter(email__in=tEmails))
                instance.students.set(User.objects.filter(email__in=sEmails))
            self.save_m2m = save_m2m_custom

        return instance
    
class assignmentGroupForm(forms.ModelForm):
    class Meta:
        model = assignmentGroup
        # auto set: group
        fields = ['title', 'subtitle']

class assignmentForm(forms.ModelForm):
    class Meta:
        model = assignment
        # auto set: assignment group
        fields = ['title', 'description', 'gradeMax', 'isHidden', 'assignmentType']

class studentSubmissionForm(forms.ModelForm):
    class Meta:
        model = submission
        # auto set: assignment, student
        # other: submittedFileContent, grade, teacherFeedback
        fields = ['submittedText']

class teacherSubmissionForm(forms.ModelForm):
    class Meta:
        model = submission
        # treated as an 'edit' to an already existing submission (but only editting the grade & teacherFeedback)
        fields = ['grade', 'teacherFeedback']