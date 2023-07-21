from rest_framework import permissions


#allow read for any user and update delete for admin user
class AdminOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        admin_permission=bool(request.user and request.user.is_staff)#checks admin user or not
        
        if request.method in permissions.SAFE_METHODS:#safe method means get
            return True
        else:
            return admin_permission
            
        
            
    
    

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:#safe method means get
            return True

        # Instance must have an attribute named `owner`.
        else:
            return (obj.review_user == request.user) or request.user.is_staff
             