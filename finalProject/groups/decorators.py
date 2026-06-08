from functools import wraps
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden, HttpResponse

# login_required is built into validateUserAccess & validateUserEdit

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
            
            userType = groupObject.getUserRelation(request.user)
            if not userType or not (userType == 'owner' or userType == 'teacher' or userType == 'student'):
                return HttpResponseForbidden(f'You do not have permission to access: {groupObject._meta.verbose_name}')
            
            request.baseObject = baseObject
            request.groupObject = groupObject
            request.userRelation = userType

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


            userType = groupObject.getUserRelation(request.user)
            if not userType or not (userType == 'owner' or userType == 'teacher'):
                return HttpResponseForbidden(f'You do not have permission to access: {groupObject._meta.verbose_name}')
            
            request.baseObject = baseObject
            request.groupObject = groupObject
            request.userRelation = userType

            return viewFunc(request, *args, **kwargs)
        return _wrapped_view
    return decorator
    
def cleanKeys(viewFunc):
    def _wrapped_view(request, *args, **kwargs):
        if request.method == 'POST':
            postData = request.POST.copy()

            for key in list(postData.keys()):
                if postData[key] == "":
                    postData.pop(key)

            request.POST = postData

        return viewFunc(request, *args, **kwargs)

    return _wrapped_view