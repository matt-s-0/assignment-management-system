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
        fields = ['title', 'description', 'isHidden', 'assignmentType']

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