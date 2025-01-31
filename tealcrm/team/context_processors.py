# from .models import Team

# def active_team(request):
#     if request.user.is_authenticated:
#         active_team = Team.objects.filter(created_by=request.user)[0]
#     else:
#         active_team= None
#     return {'active_team':active_team}

# above is Hardcoded part



from .models import Team

def active_team(request):
    active_team = None  # Default to None
    if request.user.is_authenticated:
        user_profile = getattr(request.user, 'userprofile', None)  # Safely access userprofile
        if user_profile and user_profile.active_team:
            active_team = user_profile.active_team
        else:
            # Get the first team created by the user, if available
            active_team = Team.objects.filter(created_by=request.user).first()
    return {'active_team': active_team}
