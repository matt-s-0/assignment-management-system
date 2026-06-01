from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_GET
from .forms import *
from .decorators import *

#################### Groups ####################

@require_POST
def createGroup(request):
    form = groupForm(request.POST)

    if form.is_valid():
        newForm = form.save(commit=False)
        newForm.owner = request.user
        newForm.save()
        newForm.save_m2m()
        return redirect('home')
        
    # return redirect('')

@require_POST
@validateUserEdit(group)
def editGroup(request, pk):
    form = groupForm(request.POST, instance=request.baseObject)

    if form.is_valid(): 
        form.save()

        # return redirect('')

@require_POST
@validateUserEdit(group)
def deleteGroup(request, pk):
    request.groupObject.delete()
    
    return redirect('home')

@require_GET
@validateUserAccess(group)
def studentViewGroup(request, pk):
    if not (request.groupObject.students.filter(id=request.user.id).exists()):
        return HttpResponseForbidden(f"You do not have permission to access: {request.groupObject._meta.verbose_name}")
    
    # return render stuff #####################################################################################################################

@require_GET
@validateUserAccess(group)
def teacherViewGroup(request, pk):
    if not (request.groupObject.teachers.filter(id=request.user.id).exists()):
        return HttpResponseForbidden(f"You do not have permission to access: {request.groupObject._meta.verbose_name}")
    
    # return render stuff #####################################################################################################################

@require_GET
@validateUserAccess(group)
def ownerViewGroup(request, pk):
    if request.groupObject.owner != request.user:
        return HttpResponseForbidden(f"You do not have permission to access: {request.groupObject._meta.verbose_name}")
    
    # return render stuff #####################################################################################################################

#################### Assignment Groups ####################

@require_POST
@validateUserEdit(group)
def createAssignmentGroup(request, pk):
    form = assignmentGroupForm(request.POST)

    if form.is_valid():
        newForm = form.save(commit=False)
        newForm.group = request.groupObject
        newForm.save()
        
        newForm.save_m2m() 
        
        return redirect('home')

@require_POST
@validateUserEdit(assignmentGroup)
def editAssignmentGroup(request, pk):
    form = assignmentGroupForm(request.POST, instance=request.baseObject)

    if form.is_valid(): 
        form.save()

@require_POST
@validateUserEdit(assignmentGroup)
def deleteAssignmentGroup(request, pk):
    request.baseObject.delete()
    
    return redirect('home')

#################### Assignments ####################

@require_POST
@validateUserEdit(assignmentGroup)
def createAssignment(request, pk):
    form = assignmentForm(request.POST)

    if form.is_valid():
        newForm = form.save(commit=False)
        newForm.assignmentGroup = request.baseObject
        newForm.save()
        
        newForm.save_m2m() 
        
        return redirect('home')

@require_POST
@validateUserEdit(assignment)
def editAssignment(request, pk):
    form = assignmentForm(request.POST, instance=request.baseObject)

    if form.is_valid(): 
        form.save()

@require_POST
@validateUserEdit(assignment)
def deleteAssignment(request, pk):
    request.baseObject.delete()
    
    return redirect('home')

#################### Submissions ####################

@require_POST
@validateUserAccess(assignment)
def createSubmission(request, pk):
    # checks if assignment can be submitted
    if request.baseObject.assignment.assignmentType == 'unsubmittable':
        return HttpResponseForbidden(f"You may not submit: {request.baseObject.assignment.title}")
    
    # checks if the student already made a submission for an assignment that can only be submitted once
    if request.baseObject.group == 'submittable' and request.baseObject.assignment.submissions.filter(student=request.user).exists():
        return HttpResponseForbidden(f"You have already submitted: {request.baseObject.assignment.title}")
    
    # CDR
    uploadedFile = request.FILES.get('uploadedFile')

    # Initializing to prevent errors in the form saving (incase file does not exist)
    fileContent = ''
    fileName = ''

    if uploadedFile:
        fileName = uploadedFile.name

        try:
                fileBytes = uploadedFile.read()
                fileContent = fileBytes.decode('utf-8') 
        except UnicodeDecodeError:
                # some file types will fail, so resort to base64
                import base64
                fileContent = base64.b64encode(fileBytes).decode('utf-8')
    
    form = studentSubmissionForm(request.POST, request.FILES)

    if form.is_valid():
        newForm = form.save(commit=False)

        newForm.assignment = request.baseObject
        newForm.student = request.user
        newForm.submittedFileContent = fileContent
        newForm.originalFileName = fileName

        newForm.teacherFeedback = None

        newForm.save()
        newForm.save_m2m() 
        
        return redirect('home')


@require_POST
@validateUserEdit(submission)
def gradeSubmission(request, pk):
    form = teacherSubmissionForm(request.POST, instance=request.baseObject)

    if form.is_valid(): 
        form.save()

@require_GET
@validateUserAccess(submission)
def studentViewSubmission(request, pk):
    if not (request.groupObject.students.filter(id=request.user.id).exists()):
        return HttpResponseForbidden(f"You do not have permission to access: {request.groupObject._meta.verbose_name}")
    
    # return render stuff ####################################################################################################################

@require_GET
@validateUserEdit(submission)
def teacherViewSubmission(request, pk):
    return
    # return render stuff #####################################################################################################################