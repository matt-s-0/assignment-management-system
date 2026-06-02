from django import forms
from .models import group, assignmentGroup, assignment, submission

class groupForm(forms.ModelForm):
    class Meta:
        model = group
        # auto set: owner
        fields = ['title', 'description', 'openGradeBook', 'teachers', 'students']
    
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