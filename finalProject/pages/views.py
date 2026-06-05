from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.db.models import Q
from groups.models import group
import json

@require_GET
@login_required
def mainDashboard(request):
    userGroups = group.objects.filter(
        Q(students=request.user) | 
        Q(teachers=request.user) | 
        Q(owner=request.user)
    ).distinct().prefetch_related('assignmentGroups__assignments')
    
    context = {
        'groups': userGroups
    }
    return render(request, 'home.html', context)

@require_GET
@login_required
def testDashboard(request):
    allowedGroups = group.objects.filter(
        Q(owner=request.user) | Q(teachers=request.user)
    ).distinct()

    groupData = {}
    for g in allowedGroups:
        groupData[g.id] = {
            'title': g.title,
            'description': getattr(g, 'description', ''), 
            'openGradeBook': getattr(g, 'openGradeBook', False),
            'teachers': ", ".join([t.email for t in g.teachers.all()]),
            'students': ", ".join([s.email for s in g.students.all()]),
        }

    context = {
        'allowedGroups': allowedGroups,

        'groupsJson': json.dumps(groupData), 
    }
    return render(request, 'testForms.html', context)