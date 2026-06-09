from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from .forms import *
from .decorators import *
import base64
from collections import defaultdict

#################### Groups ####################

@require_POST
@login_required
@cleanKeys
def createGroup(request):
    form = groupForm(request.POST, user=request.user)

    if form.is_valid():
        newForm = form.save(commit=False)
        newForm.owner = request.user

        newForm.save()
        form.save_m2m()

        return redirect('home')
    
    return render(request, 'testForms.html', {'form': form})

@require_POST
@validateUserEdit(group)
@cleanKeys
def editGroup(request, pk):
    form = groupForm(request.POST, instance=request.groupObject)

    if form.is_valid(): 
        form.save()
        return redirect('home')
        
    return render(request, 'testForms.html', {'form': form})

@require_POST
@validateUserEdit(group)
def deleteGroup(request, pk):
    request.groupObject.delete()
    
    return redirect('home')

@require_GET
@validateUserAccess(group)
def viewGroup(request, pk):

    context = {
        'group': request.groupObject
    }

    if request.userRelation == 'owner':
        return render(request, 'groups/ownerGroup.html', context)
    elif request.userRelation == 'teacher':
        return render(request, 'groups/teacherGroup.html', context)
    return render(request, 'groups/studentGroup.html', context)

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
    
    latestSubmission = None

    if request.userRelation == 'student':

        latestSubmission = request.baseObject.submissions.filter(
        student=request.user
        ).only('submittedText', 'submittedFileContent').order_by('-submittedAt').first()

    submissionExists = latestSubmission is not None
    
    aType = request.baseObject.assignmentType

    if aType == 'unsubmittable':
        assignmentType = 'Not Submittable'
    elif aType == 'resubmittable':
        assignmentType = 'Can be Resubmitted'
    else:
        assignmentType = 'Can be Submitted Once'

    context = {
        'group': request.groupObject,
        'assignment': request.baseObject,
        'type': assignmentType
    }

    if submissionExists:
        context['latestSubmission'] = latestSubmission

    if aType != 'unsubmittable' and submissionExists:
        
        if aType == 'resubmittable' and not latestSubmission.isGraded:
            return render(request, 'groups/assignments/studentResubmissionView.html', context)
        else:
            return render(request, 'groups/assignments/gradedView.html', context)
    else:
        userType = request.groupObject.getUserRelation(request.user)
        if not userType or not (userType == 'owner' or userType == 'teacher'):
            return render(request, 'groups/assignments/studentAssignmentView.html', context)
        
        else:
            students = request.groupObject.students.all()
            studentData = []

            submissions = defaultdict(list)

            for s in request.baseObject.submissions.all().order_by('-submittedAt'):
                submissions[s.student_id].append(s)

            for student in students:
                studentSubmissions = submissions.get(student.id, [])

                studentData.append({
                    'student': student,
                    'submissions': studentSubmissions,
                    'latestSubmission': (
                        studentSubmissions[0] if studentSubmissions else None
                    )
                })

            context = {
                'group': request.groupObject,
                'assignment': request.baseObject,
                'type': assignmentType,
                'studentData': studentData
            }

            return render(request, 'groups/assignments/gradingDashboard.html', context)

#################### Submissions ####################

@require_POST
@validateUserAccess(assignment)
@cleanKeys
def createSubmission(request, pk):
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

        newForm.submittedFileContent = fileContent
        newForm.originalFileName = fileName

        newForm.save()
        form.save_m2m() 
        
    return redirect('home')


@require_POST
@validateUserEdit(submission)
@cleanKeys
def gradeSubmission(request, pk):

    object = request.baseObject

    object.grade = request.POST.get('grade')
    object.teacherFeedback = request.POST.get('teacherFeedback')
    object.isGraded = True

    object.save(update_fields=[
        'grade',
        'teacherFeedback',
        'isGraded'
    ])

    return redirect('home')