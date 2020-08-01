from django.db.models import F, Sum
from django.utils import timezone

def user_data(req):
    userData = req.user
    print(userData.groups.filter(name='Library_Admin').exists())
    if(userData.is_authenticated):
        user_id = userData.id
        return {
            'is_authenticated': userData.is_authenticated,
            'user': userData,
            'is_admin': userData.groups.filter(name='Library_Admin').exists(),
            'user_id': user_id
        }
    else:
        return {
            'is_authenticated': userData.is_authenticated
        }