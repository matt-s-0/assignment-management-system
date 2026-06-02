from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import *
from .decorators import *
import base64

#################### Groups ####################

@require_POST
@login_required
def createGroup(request):
    form = groupForm(request.POST)

    if form.is_valid():
        newForm = form.save(commit=False)
        newForm.owner = request.user
        newForm.save()
        newForm.save_m2m()
        return redirect('home')

@require_POST
@validateUserEdit(group)
def editGroup(request, pk):
    form = groupForm(request.POST, instance=request.groupObject)

    if form.is_valid(): 
        form.save()

        return redirect('home')

@require_POST
@validateUserEdit(group)
def deleteGroup(request, pk):
    request.groupObject.delete()
    
    return redirect('home')

@require_GET
@validateUserAccess(group)
def viewGroup(request, pk):
    context = {
        'group': request.groupObject,
        'userRelation': request.userRelation
    }
    return render(request, 'group.html', context)

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

@require_GET
@validateUserAccess(assignment)
def viewAssignment(request, groupPK, pk):
    context = {
        'group': request.groupObject,
        'assignment': request.baseObject,
        'userRelation': request.userRelation,
        'isSubmission': False
    }
    return render(request, 'assignment.html', context)

#################### Submissions ####################

@require_POST
@validateUserAccess(assignment)
def createSubmission(request, pk, submittedTextContent=''):
    # checks if assignment can be submitted
    if request.baseObject.assignment.assignmentType == 'unsubmittable':
        return HttpResponseForbidden(f"You may not submit: {request.baseObject.assignment.title}")
    
    # checks if the student already made a submission for an assignment that can only be submitted once
    if request.baseObject.group == 'submittable' and request.baseObject.assignment.submissions.filter(student=request.user).exists():
        return HttpResponseForbidden(f"You have already submitted: {request.baseObject.assignment.title}")
    
    # CDR
    uploadedFile = request.FILES.get('uploadedFile')

    if uploadedFile:
        fileName = uploadedFile.name
        fileContent = base64.b64encode(uploadedFile.read()).decode('utf-8')
    else:
        fileName = ''
        fileContent = ''
    
    form = studentSubmissionForm(request.POST, request.FILES)

    if form.is_valid():
        newForm = form.save(commit=False)

        newForm.assignment = request.baseObject
        newForm.student = request.user

        newForm.submittedText = submittedTextContent
        newForm.submittedFileContent = fileContent
        newForm.originalFileName = fileName

        newForm.save()
        newForm.save_m2m() 
        
    return redirect('home')


@require_POST
@validateUserEdit(submission)
def gradeSubmission(request, pk):
    form = teacherSubmissionForm(request.POST, instance=request.baseObject)

    if form.is_valid(): 
        newForm = form.save(commit=False)

        newForm.isGraded = True

        newForm.save()

    return redirect('home')

@require_GET
@validateUserAccess(submission)
def viewSubmission(request, pk):
    context = {
        'group': request.groupObject,
        'submission': request.baseObject,
        'userRelation': request.userRelation,
        'isSubmission': True
    }
    return render(request, 'assignment.html', context)