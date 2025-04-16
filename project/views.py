from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from admin_dashboard.models import Announcement, Group, TimeTable, Advertisement
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from accounts.models import User  # Import your User model
from django.contrib import messages

def home_view(request):
    # Check for login success message in session
    if request.session.pop('login_success', False):
        messages.success(request, 'Login successful!')
    
    # Get active advertisements
    advertisements = Advertisement.objects.filter(is_active=True).order_by('-created_at')
    
    # Get selected group filter
    selected_group = request.GET.get('group')
    
    # Get announcements based on filter - only show active ones
    announcements_list = Announcement.objects.filter(is_active=True)
    
    # Apply group filter only if a specific group is selected and it's not "All Groups"
    if selected_group and selected_group.strip() and int(selected_group) != Group.get_all_groups_id():
        announcements_list = announcements_list.filter(group_id=selected_group)
    
    # Apply related field optimization
    announcements_list = announcements_list.select_related('group', 'created_by')
    
    # Sort by created_at in descending order
    announcements_list = announcements_list.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(announcements_list, 10)
    page = request.GET.get('page')
    announcements = paginator.get_page(page)
    
    # Get all groups except "All Groups" for the filter dropdown
    groups = Group.objects.exclude(id=Group.get_all_groups_id()).order_by('name')
    
    context = {
        'advertisements': advertisements,
        'groups': groups,
        'all_groups': Group.objects.get(id=Group.get_all_groups_id()),
        'selected_group': selected_group,
        'announcements': announcements,
    }
    
    return render(request, 'home.html', context)

def timetables_view(request):
    # Get only active timetables
    timetables = TimeTable.objects.filter(is_active=True).order_by('group__name')
    
    context = {
        'timetables': timetables,
    }
    
    return render(request, 'timetables.html', context)

def view_timetable_public(request, timetable_id):
    timetable = get_object_or_404(TimeTable, id=timetable_id, is_active=True)
    response = HttpResponse(timetable.pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{timetable.pdf_name}"'
    return response

@login_required
def get_user_details(request, user_id):
    try:
        user = get_object_or_404(User, id=user_id)
        data = {
            'full_name': f"{user.first_name} {user.last_name}".strip() or "N/A",
            'email': user.email,
            'username': user.username,
            'role': user.get_role_display() if hasattr(user, 'get_role_display') else str(user.role),
            'is_active': user.is_active,
            'date_joined': user.date_joined.strftime("%B %d, %Y"),
            'last_login': user.last_login.strftime("%B %d, %Y %H:%M") if user.last_login else "Never"
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def user_detail_api(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        data = {
            'full_name': f"{user.first_name} {user.last_name}".strip(),
            'email': user.email,
            'is_superuser': user.is_superuser,
            'is_staff': user.is_staff,
            'is_active': user.is_active,
            'last_login': user.last_login.strftime("%B %d, %Y %H:%M") if user.last_login else None,
            'profile_image_url': user.get_profile_image_url() if hasattr(user, 'get_profile_image_url') else None,
        }
        return JsonResponse(data)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)


