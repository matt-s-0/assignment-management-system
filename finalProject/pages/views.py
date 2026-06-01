from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from groups.models import group

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