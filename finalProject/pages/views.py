from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.db.models import Q
from groups.models import group

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
    return render(request, 'testForms.html')