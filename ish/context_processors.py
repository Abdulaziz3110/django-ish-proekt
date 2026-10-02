from .models import Xodim

def pending_xodimlar_processor(request):
    if request.user.is_authenticated and request.user.is_superuser:
        count = Xodim.objects.filter(is_approved=False).count()
        return {
            'pending_xodimlar_count': count
        }
    return {
        'pending_xodimlar_count': 0
    }
