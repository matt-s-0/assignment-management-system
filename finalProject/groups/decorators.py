from functools import wraps
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden

# login_required is built into every decorator (in this file)

def validateUserAccess(model):
    def decorator(viewFunc):
        @wraps(viewFunc)

        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')

            pk = kwargs.get('pk')
            baseObject = get_object_or_404(model, pk=pk)

            if hasattr(baseObject, 'owner'):
                groupObject = baseObject

            elif hasattr(baseObject, 'group'):
                groupObject = baseObject.group

            elif hasattr(baseObject, 'assignmentGroup'):
                groupObject = baseObject.assignmentGroup.group

            elif hasattr(baseObject, 'assignment'):
                groupObject = baseObject.assignment.assignmentGroup.group

            else:
                return HttpResponseForbidden('Resource configuration error: Group relationship not found.')

            user = request.user

            if not (groupObject.owner == request.user or groupObject.teachers.filter(id=user.id).exists() or groupObject.students.filter(id=user.id).exists()):
                return HttpResponseForbidden(f'You do not have permission to access: {groupObject._meta.verbose_name}')
            
            request.baseObject = baseObject
            request.groupObject = groupObject

            return viewFunc(request, *args, **kwargs)
        return _wrapped_view
    return decorator
    
def validateUserEdit(model):
    def decorator(viewFunc):
        @wraps(viewFunc)

        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            pk = kwargs.get('pk')
            baseObject = get_object_or_404(model, pk=pk)

            if hasattr(baseObject, 'owner'):
                groupObject = baseObject

            elif hasattr(baseObject, 'group'):
                groupObject = baseObject.group

            elif hasattr(baseObject, 'assignmentGroup'):
                groupObject = baseObject.assignmentGroup.group

            elif hasattr(baseObject, 'assignment'):
                groupObject = baseObject.assignment.assignmentGroup.group

            else:
                return HttpResponseForbidden('Resource configuration error: Group relationship not found.')

            user = request.user

            if not (groupObject.owner == request.user or groupObject.teachers.filter(id=user.id).exists()):
                return HttpResponseForbidden(f'You do not have permission to access: {groupObject._meta.verbose_name}')
            
            request.baseObject = baseObject
            request.groupObject = groupObject

            return viewFunc(request, *args, **kwargs)
        return _wrapped_view
    return decorator