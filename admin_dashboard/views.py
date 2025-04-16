
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from .decorators import admin_only
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .decorators import admin_only, is_admin_or_teacher
from .models import Announcement, Advertisement, Group, User, TimeTable
from django.http import JsonResponse, Http404
from django.db.models import Q

User = get_user_model()

@login_required
@admin_only
def create_user(request):
    if request.method == 'POST':
        try:
            # Get form data
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            role = request.POST.get('role')
            is_active = request.POST.get('is_active') == 'on'
            
            # Validate required fields
            if not all([first_name, last_name, email, password, role]):
                raise ValueError("All fields are required")
            
            # Check if user already exists
            if User.objects.filter(email=email).exists():
                raise ValueError("A user with this email already exists")
            
            # Set is_staff based on role
            is_staff = (role == 'admin')
            
            # Create user
            user = User.objects.create_user(
                username=email,  # Using email as username
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_active=is_active,
                is_staff=is_staff,
                role=role
            )
            
            # Handle profile image upload
            if 'profile_image' in request.FILES:
                profile_image = request.FILES['profile_image']
                
                # Validate file size (5MB limit)
                if profile_image.size > 5 * 1024 * 1024:
                    raise ValueError("Profile image must be less than 5MB")
                
                # Validate file type
                allowed_types = ['image/jpeg', 'image/png', 'image/gif']
                if profile_image.content_type not in allowed_types:
                    raise ValueError("Only JPEG, PNG and GIF images are allowed")
                
                # Save image data
                user.profile_image_data = profile_image.read()
                user.profile_image_type = profile_image.content_type
                user.save()
            
            messages.success(request, f'User {email} created successfully.')
            return redirect('admin_dashboard:user_list')
            
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')
    
    return render(request, 'admin/user_create.html')

@login_required
@is_admin_or_teacher
def dashboard(request):
    if not (request.user.is_staff or request.user.role == 'teacher'):
        return render(request, '404.html', status=404)
    
    if request.user.is_staff:
        # Admin sees all statistics
        context = {
            'total_users': User.objects.all().count(),
            'total_announcements': Announcement.objects.count(),
            'active_announcements': Announcement.objects.filter(is_active=True).count(),
            'total_groups': Group.objects.count(),
            'total_timetables': TimeTable.objects.count(),
            'total_ads': Advertisement.objects.count(),
            'active_ads': Advertisement.objects.filter(is_active=True).count(),
        }
    else:
        # Teacher sees only their announcements
        teacher_announcements = Announcement.objects.filter(created_by=request.user)
        context = {
            'total_announcements': teacher_announcements.count(),
            'active_announcements': teacher_announcements.filter(is_active=True).count(),
            'is_teacher': True
        }
    
    return render(request, 'admin_dashboard/dashboard.html', context)

@login_required
@admin_only
def user_list(request):
    # Debug prints
    print("Executing user_list view")
    
    # Get all users
    users = User.objects.all().order_by('-date_joined')
    print(f"Total users found: {users.count()}")
    
    # Print each user for debugging
    for user in users:
        print(f"Found user: {user.email} (ID: {user.id})")
    
    # Get role filter
    role_filter = request.GET.get('role', 'all')
    
    # Apply filters
    if role_filter and role_filter != 'all':
        if role_filter == 'admin':
            users = users.filter(
                Q(is_staff=True) | 
                Q(is_superuser=True) |
                Q(role='admin')
            ).distinct()
        elif role_filter == 'teacher':
            users = users.filter(role='teacher')
        elif role_filter == 'user':
            users = users.filter(role='user')
    
    context = {
        'users': users,
        'current_filter': role_filter,
        'total_users': users.count()  # Add total count to context
    }
    
    return render(request, 'admin/user_list.html', context)

@login_required
@admin_only
def user_detail(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)
    return render(request, 'admin/user_detail.html', {'user': user})

@login_required
@admin_only
def user_edit(request, user_id):
    try:
        # Get the specific user to edit using the user_id parameter
        user_to_edit = get_object_or_404(User, id=user_id)
        
        if request.method == 'POST':
            try:
                # Get form data
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                email = request.POST.get('email')
                role = request.POST.get('role')
                is_active = request.POST.get('is_active') == 'on'
                
                # Validate required fields
                if not all([first_name, last_name, email, role]):
                    raise ValueError("All fields are required")
                
                # Check if email exists for other users
                if User.objects.filter(email=email).exclude(id=user_id).exists():
                    raise ValueError("A user with this email already exists")
                
                # Update the specific user (user_to_edit)
                user_to_edit.first_name = first_name
                user_to_edit.last_name = last_name
                user_to_edit.email = email
                user_to_edit.username = email
                user_to_edit.role = role
                user_to_edit.is_active = is_active
                user_to_edit.save()
                
                messages.success(request, 'User updated successfully.')
                return redirect('admin_dashboard:user_list')
                
            except ValueError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, f'Error updating user: {str(e)}')
        
        # Pass the specific user to the template
        context = {
            'user_to_edit': user_to_edit,
            'roles': User.ROLE_CHOICES
        }
        return render(request, 'admin/user_edit.html', context)
        
    except Exception as e:
        messages.error(request, f'Error accessing user: {str(e)}')
        return redirect('admin_dashboard:user_list')

@login_required
@admin_only
def site_settings(request):
    return render(request, 'admin/site_settings.html')

@login_required
@admin_only
def logs(request):
    return render(request, 'admin/logs.html')

@login_required
@is_admin_or_teacher
def announcement_list(request):
    announcements = Announcement.objects.all().order_by('-created_at')
    
    # Get filter parameters
    is_active = request.GET.get('is_active')
    group_id = request.GET.get('group')
    
    # Apply filters
    if is_active:
        announcements = announcements.filter(is_active=is_active == 'true')
    if group_id:
        announcements = announcements.filter(group_id=group_id)
    
    groups = Group.objects.all()
    
    context = {
        'announcements': announcements,
        'groups': groups,
    }
    
    return render(request, 'admin/announcements.html', context)

@login_required
@admin_only
def announcement_detail(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)
    return render(request, 'admin/announcement_detail.html', {'announcement': announcement})

@login_required
@is_admin_or_teacher
def create_announcement(request):
    # Get all groups including "All Groups"
    groups = Group.objects.all().order_by('name')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        group_id = request.POST.get('group')
        
        if not all([title, description, group_id]):
            messages.error(request, 'All fields are required.')
            return render(request, 'admin/create_announcement.html', {'groups': groups})
        
        try:
            group = Group.objects.get(id=group_id)
            announcement = Announcement(
                title=title,
                description=description,
                created_by=request.user,
                is_active=True,
                group=group
            )
            announcement.save()
            messages.success(request, 'Announcement created successfully.')
            return redirect('admin_dashboard:announcement_list')
        except Group.DoesNotExist:
            messages.error(request, 'Selected group does not exist.')
            return render(request, 'admin/create_announcement.html', {'groups': groups})
    
    return render(request, 'admin/create_announcement.html', {'groups': groups})

@login_required
@is_admin_or_teacher
def edit_announcement(request, announcement_id):
    # Get the announcement and verify ownership for teachers
    announcement = get_object_or_404(Announcement, id=announcement_id)
    
    # Check if user is teacher and owns the announcement
    if not request.user.is_staff and announcement.created_by != request.user:
        messages.error(request, 'You can only edit your own announcements.')
        return redirect('admin_dashboard:announcement_list')
    
    groups = Group.objects.all()
    
    if request.method == 'POST':
        # Get form data
        title = request.POST.get('title')
        description = request.POST.get('description')
        is_active = request.POST.get('is_active') == 'on'
        group_id = request.POST.get('group')
        
        # Only update the fields that are provided
        if title:
            announcement.title = title
        if description:
            announcement.description = description
        
        announcement.is_active = is_active
        
        if group_id:
            try:
                group = Group.objects.get(id=group_id)
                announcement.group = group
            except Group.DoesNotExist:
                messages.error(request, 'Selected group does not exist.')
                return render(request, 'admin/edit_announcement.html', {
                    'announcement': announcement,
                    'groups': groups
                })
        else:
            announcement.group = None
        
        announcement.save()
        messages.success(request, 'Announcement updated successfully.')
        return redirect('admin_dashboard:announcement_list')
    
    return render(request, 'admin/edit_announcement.html', {
        'announcement': announcement,
        'groups': groups
    })

@login_required
@is_admin_or_teacher
def delete_announcement(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)
    
    # Check if user is teacher and owns the announcement
    if not request.user.is_staff and announcement.created_by != request.user:
        messages.error(request, 'You can only delete your own announcements.')
        return redirect('admin_dashboard:announcement_list')
    
    announcement.delete()
    messages.success(request, 'Announcement deleted successfully.')
    return redirect('admin_dashboard:announcement_list')

@login_required
@admin_only
def delete_user(request, user_id):
    try:
        user = get_object_or_404(User, id=user_id)
        
        # Prevent self-deletion
        if user.id == request.user.id:
            messages.error(request, 'You cannot delete your own account.')
            return redirect('admin_dashboard:user_list')
            
        # Prevent deletion of superuser accounts
        if user.is_superuser:
            messages.error(request, 'Superuser accounts cannot be deleted.')
            return redirect('admin_dashboard:user_list')
        
        # Store email for success message
        email = user.email
        
        # Delete the user
        user.delete()
        
        messages.success(request, f'User "{email}" was deleted successfully.')
        return redirect('admin_dashboard:user_list')
        
    except Exception as e:
        messages.error(request, f'Error deleting user: {str(e)}')
        return redirect('admin_dashboard:user_list')

@login_required
@admin_only
def group_list(request):
    groups = Group.objects.all()
    return render(request, 'admin/groups.html', {'groups': groups})

@login_required
@admin_only
def create_group(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            try:
                Group.objects.create(name=name)
                messages.success(request, 'Group created successfully.')
                return redirect('admin_dashboard:group_list')
            except Exception as e:
                messages.error(request, f'Error creating group: {str(e)}')
    return render(request, 'admin/create_group.html')

@login_required
@admin_only
def edit_group(request, group_id):
    if group_id == 1:  # Prevent editing of "All Groups"
        messages.error(request, 'The "All Groups" group cannot be edited.')
        return redirect('admin_dashboard:group_list')
        
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            try:
                group.name = name
                group.save()
                messages.success(request, 'Group updated successfully.')
                return redirect('admin_dashboard:group_list')
            except Exception as e:
                messages.error(request, f'Error updating group: {str(e)}')
    return render(request, 'admin/edit_group.html', {'group': group})  # Remove 'templates/' from path

@login_required
@admin_only
def delete_group(request, group_id):
    if group_id == 1:  # Prevent deletion of "All Groups"
        messages.error(request, 'The "All Groups" group cannot be deleted.')
        return redirect('admin_dashboard:group_list')
        
    group = get_object_or_404(Group, id=group_id)
    group.delete()
    messages.success(request, 'Group deleted successfully.')
    return redirect('admin_dashboard:group_list')

@login_required
@admin_only
def ad_list(request):
    ads = Advertisement.objects.all()
    return render(request, 'admin/ads.html', {'ads': ads})

@login_required
@admin_only
def create_ad(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        if title and description:
            Advertisement.objects.create(
                title=title,
                description=description,
                created_by=request.user
            )
            messages.success(request, 'Advertisement created successfully.')
            return redirect('admin_dashboard:ad_list')
    return render(request, 'admin/create_ad.html')

@login_required
@admin_only
def edit_ad(request, ad_id):
    ad = get_object_or_404(Advertisement, id=ad_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        is_active = request.POST.get('is_active') == 'on'
        
        if title and description:
            ad.title = title
            ad.description = description
            ad.is_active = is_active
            ad.save()
            messages.success(request, 'Advertisement updated successfully.')
            return redirect('admin_dashboard:ad_list')
    
    return render(request, 'admin/edit_ad.html', {'ad': ad})

@login_required
@admin_only
def delete_ad(request, ad_id):
    ad = get_object_or_404(Advertisement, id=ad_id)
    ad.delete()
    messages.success(request, 'Advertisement deleted successfully.')
    return redirect('admin_dashboard:ad_list')

@login_required
@admin_only
def timetable_list(request):
    timetables = TimeTable.objects.all()
    return render(request, 'admin/timetables.html', {'timetables': timetables})

@login_required
@admin_only
def upload_timetable(request):
    groups = Group.objects.all()
    
    if request.method == 'POST':
        group_id = request.POST.get('group')
        pdf_file = request.FILES.get('pdf_file')
        
        if group_id and pdf_file:
            # Validate file is PDF
            if not pdf_file.name.endswith('.pdf'):
                messages.error(request, 'Please upload a PDF file.')
                return redirect('admin_dashboard:upload_timetable')
                
            try:
                group = Group.objects.get(id=group_id)
                
                # Deactivate old timetable if exists
                TimeTable.objects.filter(group=group, is_active=True).update(is_active=False)
                
                # Read the PDF file content
                pdf_content = pdf_file.read()
                
                # Create new timetable with PDF stored in database
                timetable = TimeTable.objects.create(
                    group=group,
                    pdf_data=pdf_content,
                    pdf_name=pdf_file.name,
                    is_active=True
                )
                
                messages.success(request, 'Timetable uploaded successfully.')
                return redirect('admin_dashboard:timetable_list')
            except Group.DoesNotExist:
                messages.error(request, 'Selected group does not exist.')
            except Exception as e:
                messages.error(request, f'Error uploading timetable: {str(e)}')
    
    return render(request, 'admin/upload_timetable.html', {'groups': groups})

@login_required
@admin_only
def view_timetable(request, timetable_id):
    """New view to serve PDF directly from database"""
    from django.http import HttpResponse
    
    timetable = get_object_or_404(TimeTable, id=timetable_id)
    response = HttpResponse(timetable.pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{timetable.pdf_name}"'
    return response

@login_required
@admin_only
def delete_timetable(request, timetable_id):
    try:
        timetable = TimeTable.objects.get(id=timetable_id)
        timetable.delete()
        messages.success(request, 'Timetable deleted successfully.')
    except TimeTable.DoesNotExist:
        messages.error(request, 'Timetable not found.')
    return redirect('admin_dashboard:timetable_list')

def home(request):
    # Get all announcements
    announcements = Announcement.objects.all()
    
    # Debug prints
    print("DEBUG INFO:")
    print(f"Total announcements in database: {announcements.count()}")
    for ann in announcements:
        print(f"- Title: {ann.title}")
        print(f"- Description: {ann.description}")
        print(f"- Created by: {ann.created_by}")
        print(f"- Group: {ann.group}")
        print("---")
    
    # Get all groups
    groups = Group.objects.all()
    
    # Get selected group filter
    selected_group = request.GET.get('group')
    if selected_group:
        announcements = announcements.filter(group_id=selected_group)
    
    context = {
        'announcements': announcements,
        'groups': groups,
        'total_announcements': announcements.count(),
        'selected_group': selected_group,
    }
    
    # Debug print context
    print("Context being sent to template:")
    print(f"Total announcements in context: {len(context['announcements'])}")
    
    return render(request, 'home.html', context)

@login_required
@admin_only
def ad_detail_api(request, ad_id):
    ad = get_object_or_404(Advertisement, id=ad_id)
    return JsonResponse({
        'title': ad.title,
        'description': ad.description,
        'created_by': f"{ad.created_by.first_name} {ad.created_by.last_name}",
        'is_active': ad.is_active,
        'created_at': ad.created_at.strftime("%B %d, %Y")
    })

@login_required
@is_admin_or_teacher
def announcement_detail_api(request, announcement_id):
    try:
        announcement = get_object_or_404(Announcement, id=announcement_id)
        
        # Add debug print
        print(f"Found announcement: {announcement.id} - {announcement.title}")
        
        data = {
            'title': announcement.title,
            'description': announcement.description,
            'created_by': f"{announcement.created_by.first_name} {announcement.created_by.last_name}",
            'is_active': announcement.is_active,
            'created_at': announcement.created_at.strftime("%B %d, %Y"),
            'group': announcement.group.name if announcement.group else None
        }
        return JsonResponse(data)
    except Announcement.DoesNotExist:
        return JsonResponse({'error': 'Announcement not found'}, status=404)
    except Exception as e:
        print(f"Error in announcement_detail_api: {str(e)}")  # Add debug print
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@admin_only
def get_user_details_api(request, user_id):
    try:
        user = get_object_or_404(User, id=user_id)
        data = {
            'full_name': f"{user.first_name} {user.last_name}".strip() or "N/A",
            'email': user.email,
            'username': user.username,
           
            'role_display': user.get_role_display(),
            'is_active': user.is_active,
            'date_joined': user.date_joined.strftime("%B %d, %Y"),
            'last_login': user.last_login.strftime("%B %d, %Y %H:%M") if user.last_login else "Never"
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def get_announcement(request, pk):
    try:
        announcement = get_object_or_404(Announcement, pk=pk)
        data = {
            'id': announcement.id,
            'title': announcement.title,
            'description': announcement.description,
            'created_by': f"{announcement.created_by.first_name} {announcement.created_by.last_name}",
            'created_at': announcement.created_at.strftime('%Y-%m-%d'),
            'is_active': announcement.is_active,
            'group': announcement.group.name if announcement.group else 'All Groups'
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)





