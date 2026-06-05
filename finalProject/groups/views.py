from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from .forms import *
from .decorators import *
import base64

#################### Groups ####################

@require_POST
@login_required
@cleanKeys
def createGroup(request):
    form = groupForm(request.POST)
    print('createGroup called')

    if form.is_valid():
        newForm = form.save(commit=False)
        newForm.owner = request.user

        newForm.save()
        form.save_m2m()
    else:
        ######################################## DEBUG ########################################
        print("Form Validation Failed!")
        print(form.errors.as_json())

    return redirect('home')

@require_POST
@validateUserEdit(group)
@cleanKeys
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
    return render(request, 'groups/group.html', context)

#################### Assignment Groups ####################

@require_POST
@validateUserEdit(group)
@cleanKeys
def createAssignmentGroup(request, pk):
    form = assignmentGroupForm(request.POST)

    if form.is_valid():
        newForm = form.save(commit=False)
        newForm.group = request.groupObject

        newForm.save()
        form.save_m2m() 
        
    return redirect('home')

@require_POST
@validateUserEdit(assignmentGroup)
@cleanKeys
def editAssignmentGroup(request, pk):
    form = assignmentGroupForm(request.POST, instance=request.baseObject)

    if form.is_valid(): 
        form.save()

    return redirect('home')

@require_POST
@validateUserEdit(assignmentGroup)
def deleteAssignmentGroup(request, pk):
    request.baseObject.delete()
    
    return redirect('home')

#################### Assignments ####################

@require_POST
@validateUserEdit(assignmentGroup)
@cleanKeys
def createAssignment(request, pk):
    form = assignmentForm(request.POST)

    if form.is_valid():
        newForm = form.save(commit=False)
        newForm.assignmentGroup = request.baseObject

        newForm.save()
        form.save_m2m() 
        
    return redirect('home')

@require_POST
@validateUserEdit(assignment)
@cleanKeys
def editAssignment(request, pk):
    form = assignmentForm(request.POST, instance=request.baseObject)

    if form.is_valid(): 
        form.save()

    return redirect('home')

@require_POST
@validateUserEdit(assignment)
def deleteAssignment(request, pk):
    request.baseObject.delete()
    
    return redirect('home')

@require_GET
@validateUserAccess(assignment)
def viewAssignment(request, pk):

    if request.baseObject.isHidden == True:
        return redirect('home')

    context = {
        'group': request.groupObject,
        'assignment': request.baseObject,
        'userRelation': request.userRelation
    }

    if request.baseObject.assignmentType != 'unsubmittable' and request.baseObject.submissions.filter(student=request.user).exists():
        return render(request, 'groups/submission.html', context)
    else:
        return render(request, 'groups/assignment.html', context)

#################### Submissions ####################

@require_POST
@validateUserAccess(assignment)
@cleanKeys
def createSubmission(request, pk, submittedTextContent=''):
    # checks if assignment can be submitted
    if request.baseObject.assignmentType == 'unsubmittable':
        return HttpResponseForbidden(f"You may not submit: {request.baseObject.title}")
    
    # checks if the student already made a submission for an assignment that can only be submitted once
    if request.baseObject.assignmentType == 'submittable' and request.baseObject.submissions.filter(student=request.user).exists():
        return HttpResponseForbidden(f"You have already submitted: {request.baseObject.title}")
    
    maxFileSize = 1048576  # 1 MB in bytes, 1024 * 1024

    # CDR
    uploadedFile = request.FILES.get('uploadedFile')

    if uploadedFile:
        if uploadedFile.size > maxFileSize:
            return JsonResponse({'error': 'File size exceeds the 1 MB limit.'}, status=400)
        
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
        form.save_m2m() 
        
    return redirect('home')


@require_POST
@validateUserEdit(submission)
@cleanKeys
def gradeSubmission(request, pk):
    form = teacherSubmissionForm(request.POST, instance=request.baseObject)

    if form.is_valid(): 
        newForm = form.save(commit=False)

        newForm.isGraded = True

        newForm.save()

    return redirect('home')