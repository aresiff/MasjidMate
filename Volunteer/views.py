from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Admin, Committee, Volunteer, TaskApplication, Event
from django.contrib import messages
import datetime
import uuid
from django.utils import timezone

# Front page view
def index(request):
    return render(request, 'index.html')

# Admin redirect login page
def admin_login(request):
    return render(request, 'login_admin.html')

# Committee redirect login page
def committee_login(request):
    return render(request, 'login_committee.html')

# Volunteer redirect login page
def volunteer_login(request):
    return render(request, 'login_volunteer.html')




# Admin login page
def admin_login(request):
    if request.method == 'POST':
        adminid = request.POST['adminid']
        password = request.POST['password']
        try:
            admin = Admin.objects.get(adminid=adminid)
            if admin.password == password:
                request.session['adminid'] = admin.adminid
                return redirect('admin_dashboard')
        except Admin.DoesNotExist:
            pass  # Fall through to error message

        messages.error(request, 'Incorrect Admin ID or Password.')
    return render(request, 'login_admin.html')

# Committee login page
def committee_login(request):
    if request.method == 'POST':
        committeeid = request.POST['committeeid']
        password = request.POST['password']
        try:
            committee = Committee.objects.get(committeeid=committeeid)
            if committee.password == password:
                request.session['committeeid'] = committee.committeeid
                return redirect('committee_dashboard')
        except Committee.DoesNotExist:
            pass  # Continue to error below

        messages.error(request, 'Incorrect Committee ID or Password.')
    return render(request, 'login_committee.html')


# Volunteer Login Page
def volunteer_login(request):
    if request.method == 'POST':
        volunteerid = request.POST['volunteerid']
        password = request.POST['password']
        try:
            volunteer = Volunteer.objects.get(volunteerid=volunteerid)
            if volunteer.password == password:
                request.session['volunteerid'] = volunteer.volunteerid
                return redirect('volunteer_dashboard')
        except Volunteer.DoesNotExist:
            pass  # Avoid separate error

        messages.error(request, 'Incorrect Volunteer ID or Password.')
    return render(request, 'login_volunteer.html')




# Committee Sign Up
def committee_signup(request):
    if request.method == 'POST':
        committeeid = request.POST['committeeid']
        name = request.POST['name']
        position = request.POST['position']
        contactno = request.POST['contactno']
        email = request.POST['email']
        role = request.POST['role']
        password = request.POST['password']
        if Committee.objects.filter(committeeid=committeeid).exists():
            messages.error(request, "Committee ID already exists.")
        else:
            Committee.objects.create(
                committeeid=committeeid,
                name=name,
                position=position,
                contactno=contactno,
                email=email,
                role=role,
                password=password
            )
            messages.success(request, "Registration successful. Please log in.")
            return redirect('committeelogin')
    return render(request, 'signup_committee.html')

# Volunteer Sign Up
def volunteer_signup(request):
    if request.method == 'POST':
        volunteerid = request.POST['volunteerid']
        name = request.POST['name']
        age = request.POST['age']
        gender = request.POST['gender']
        contactno = request.POST['contactno']
        email = request.POST['email']
        address = request.POST['address']
        skills = request.POST['skills']
        password = request.POST['password']

        if Volunteer.objects.filter(volunteerid=volunteerid).exists():
            messages.error(request, "Volunteer ID already exists.")
        else:
            Volunteer.objects.create(
                volunteerid=volunteerid,
                name=name,
                age=age,
                gender=gender,
                contactno=contactno,
                email=email,
                address=address,
                skills=skills,
                password=password
            )
            messages.success(request, "Registration successful. Please log in.")
            return redirect('volunteerlogin')
    return render(request, 'signup_volunteer.html')



# Dashboard
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def committee_dashboard(request):
    return render(request, 'committee_dashboard.html')

def volunteer_dashboard(request):
    return render(request, 'volunteer_dashboard.html')



# Dashboard View
def volunteer_dashboard(request):
    # Get volunteer ID from session (you must set this on login)
    volunteerid = request.session.get('volunteerid')
    if not volunteerid:
        messages.error(request, "You must be logged in to access this page.")
        return redirect('volunteerlogin')

    try:
        volunteer = Volunteer.objects.get(volunteerid=volunteerid)
    except Volunteer.DoesNotExist:
        messages.error(request, "Volunteer not found.")
        return redirect('volunteerlogin')

    return render(request, 'volunteer_dashboard.html', {'volunteer': volunteer})

# My Profile (View & Edit)
def volunteer_profile(request):
    volunteerid = request.session.get('volunteerid')
    if not volunteerid:
        return redirect('volunteerlogin')
    
    volunteer = Volunteer.objects.get(volunteerid=volunteerid)

    if request.method == 'POST':
        volunteer.name = request.POST['name']
        volunteer.age = request.POST['age']
        volunteer.gender = request.POST['gender']
        volunteer.contactno = request.POST['contactno']
        volunteer.email = request.POST['email']
        volunteer.address = request.POST['address']
        volunteer.skills = request.POST['skills']
        volunteer.password = request.POST['password']
        volunteer.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('volunteer_dashboard')

    return render(request, 'profile_volunteer.html', {'volunteer': volunteer})

# Task Details Page (View applications)
def volunteer_taskdetails(request):
    volunteerid = request.session.get('volunteerid')
    if not volunteerid:
        return redirect('volunteerlogin')
    
    applications = TaskApplication.objects.filter(volunteerid=volunteerid)
    return render(request, 'volunteer_taskdetails.html', {'applications': applications})

# Mosque Event List Page (View & Apply - just render page for now)
def volunteer_mosquevent(request):
    events = Event.objects.all()
    return render(request, 'volunteer_mosquevent.html', {'events': events})


# Committee Dashboard
def committee_dashboard(request):
    committeeid = request.session.get('committeeid')
    if not committeeid:
        messages.error(request, "You must be logged in to access this page.")
        return redirect('committeelogin')
    
    try:
        committee = Committee.objects.get(committeeid=committeeid)
    except Committee.DoesNotExist:
        messages.error(request, "Committee not found.")
        return redirect('committeelogin')

    return render(request, 'committee_dashboard.html', {'committee': committee})

# Committee Profile View & Edit
def committee_profile(request):
    committeeid = request.session.get('committeeid')
    if not committeeid:
        return redirect('committeelogin')

    committee = Committee.objects.get(committeeid=committeeid)

    if request.method == 'POST':
        committee.name = request.POST['name']
        committee.position = request.POST['position']
        committee.contactno = request.POST['contactno']
        committee.email = request.POST['email']
        committee.role = request.POST['role']
        committee.password = request.POST['password']
        committee.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('committee_dashboard')

    return render(request, 'profile_committee.html', {'committee': committee})

# Placeholder View: Approve Volunteer Applications
def committee_approveVol(request):
    return render(request, 'committee_approveVol.html')

# Placeholder View: Record Volunteer Performance
def committee_recordperformance(request):
    return render(request, 'committee_recordperformance.html')

# Placeholder View: Record Mosque Event
def committee_recordevent(request):
    return render(request, 'committee_recordevent.html')



# Committee creates a mosque event
def committee_recordevent(request):
    if request.method == 'POST':
        eventid = request.POST['eventid']
        eventname = request.POST['eventname']
        eventdate = request.POST['eventdate']
        tasks = request.POST['tasks']
        volcapacity = request.POST['volcapacity']
        token = request.POST['token']

        committeeid = request.session.get('committeeid')
        committee = Committee.objects.get(committeeid=committeeid)

        if Event.objects.filter(eventid=eventid).exists():
            messages.error(request, "Event ID already exists.")
        else:
            Event.objects.create(
                eventid=eventid,
                eventname=eventname,
                eventdate=eventdate,
                tasks=tasks,
                volcapacity=volcapacity,
                token=token,
                created_by=committee
            )
            messages.success(request, "Event created successfully.")

    return render(request, 'committee_recordevent.html')


# Committee History Event Record
def committee_historyEvent(request):
    events = Event.objects.select_related('created_by').all()
    return render(request, 'committee_historyEvent.html', {'events': events})


# Mosque Event
# Show all available events
def volunteer_mosquevent(request):
    volunteerid = request.session.get('volunteerid')
    if not volunteerid:
        messages.error(request, "Please login first.")
        return redirect('volunteerlogin')

    events = Event.objects.all()
    volunteer = Volunteer.objects.get(volunteerid=volunteerid)

    # Get event IDs that this volunteer has already applied to
    applied_event_ids = TaskApplication.objects.filter(volunteerid=volunteer).values_list('eventid__eventid', flat=True)

    # Get event IDs that are full (approved >= capacity)
    full_events = []
    for event in events:
        approved_count = TaskApplication.objects.filter(eventid=event, status='Approved').count()
        if approved_count >= event.volcapacity:
            full_events.append(event.eventid)

    return render(request, 'volunteer_mosquevent.html', {
        'events': events,
        'applied_event_ids': applied_event_ids,
        'full_events': full_events
    })

# Confirmation page before applying
def volunteer_confirmapply(request):
    volunteerid = request.session.get('volunteerid')
    if not volunteerid:
        messages.error(request, "Please login first.")
        return redirect('volunteerlogin')

    eventid = request.GET.get('eventid')
    try:
        event = Event.objects.get(eventid=eventid)
    except Event.DoesNotExist:
        messages.error(request, "Event not found.")
        return redirect('volunteer_mosquevent')

    # Check capacity
    approved_count = TaskApplication.objects.filter(eventid=event, status='Approved').count()
    if approved_count >= event.volcapacity:
        messages.error(request, "Sorry, this event is already full.")
        return redirect('volunteer_mosquevent')

    return render(request, 'volunteer_confirmationapplied.html', {'event': event})

# Final apply confirmation
def volunteer_apply_confirmed(request):
    if request.method == 'POST':
        volunteerid = request.session.get('volunteerid')
        eventid = request.POST['eventid']

        if not volunteerid:
            return redirect('volunteerlogin')

        volunteer = Volunteer.objects.get(volunteerid=volunteerid)
        event = Event.objects.get(eventid=eventid)

        # Check if already applied for this event
        if TaskApplication.objects.filter(volunteerid=volunteer, eventid=event).exists():
            messages.warning(request, "You have already applied for this event.")
            return redirect('volunteer_mosquevent')

        # Create application
        TaskApplication.objects.create(
            applicationid=uuid.uuid4(),
            volunteerid=volunteer,
            eventid=event,
            taskid="",  # will be filled in later by committee
            status='Pending',
            attendance=False,
            performancerating=None,
            tokensearned=""  # now a string
        )

        messages.success(request, "You have successfully applied for the event!")
        return redirect('volunteer_mosquevent')
    
def volunteer_taskdetails(request):
    volunteerid = request.session.get('volunteerid')
    if not volunteerid:
        return redirect('volunteerlogin')

    applications = TaskApplication.objects.filter(volunteerid=volunteerid)
    return render(request, 'volunteer_taskdetails.html', {'applications': applications})



# Committee Approval Event Page
def committee_approveVol(request):
    applications = TaskApplication.objects.filter(status='Pending').select_related('volunteerid', 'eventid')

    if request.method == 'POST':
        app_id = request.POST['applicationid']
        action = request.POST['action']
        task_desc = request.POST.get('taskdesc', '')

        try:
            application = TaskApplication.objects.get(applicationid=app_id)
            event = application.eventid

            if action == 'approve':
                # Count approved applications for this event
                approved_count = TaskApplication.objects.filter(eventid=event, status='Approved').count()

                if approved_count >= event.volcapacity:
                    messages.error(request, f"Cannot approve. Event '{event.eventname}' is already full.")
                else:
                    application.status = 'Approved'
                    application.taskid = task_desc
                    application.save()
                    messages.success(request, f"Application {app_id} has been approved.")
            elif action == 'reject':
                application.status = 'Rejected'
                application.save()
                messages.success(request, f"Application {app_id} has been rejected.")

        except TaskApplication.DoesNotExist:
            messages.error(request, "Application not found.")

        return redirect('committee_approveVol')

    return render(request, 'committee_approveVol.html', {'applications': applications})


# Committee Record Performance
def committee_recordperformance(request):
    # Only include approved applications
    applications = TaskApplication.objects.filter(status='Approved').select_related('volunteerid', 'eventid')

    if request.method == 'POST':
        applicationid = request.POST['applicationid']
        attendance = request.POST.get('attendance') == 'on'
        rating = request.POST.get('performancerating') or None
        token = request.POST.get('tokensearned') or ""

        try:
            app = TaskApplication.objects.get(applicationid=applicationid)
            app.attendance = attendance
            app.performancerating = rating
            app.tokensearned = token
            app.save()
            messages.success(request, f"✅ Performance recorded for {app.volunteerid.name}.")
        except TaskApplication.DoesNotExist:
            messages.error(request, "❌ Application not found.")

        return redirect('committee_recordperformance')

    return render(request, 'committee_recordperformance.html', {
        'applications': applications
    })

# Admin Dashbooard

def admin_dashboard(request):
    adminid = request.session.get('adminid')
    if not adminid:
        return redirect('adminlogin')

    admin = Admin.objects.get(adminid=adminid)
    return render(request, 'admin_dashboard.html', {'admin': admin})

#temporary
def profile_admin(request):
    return render(request, 'profile_admin.html')

def profile_admin(request):
    return render(request, 'profile_admin.html')

def admin_manageVol(request):
    return render(request, 'admin_manageVol.html')

def admin_manageEvents(request):
    return render(request, 'admin_manageEvents.html')

def admin_generateReport(request):
    return render(request, 'admin_generateReport.html')

# Admin Profile Page
from django.contrib import messages

def profile_admin(request):
    adminid = request.session.get('adminid')
    if not adminid:
        return redirect('adminlogin')

    admin = Admin.objects.get(adminid=adminid)

    if request.method == 'POST':
        admin.name = request.POST['name']
        admin.position = request.POST['position']
        admin.contactno = request.POST['contactno']
        admin.email = request.POST['email']
        admin.password = request.POST['password']
        admin.save()
        messages.success(request, "Profile updated successfully!")

    return render(request, 'profile_admin.html', {'admin': admin})

# Admin Manage Volunteer Page
def admin_manageVol(request):
    volunteer_list = Volunteer.objects.all()
    selected_volunteer = None

    if request.method == 'POST':
        if 'select_volunteer' in request.POST:
            selected_id = request.POST['volunteerid']
            selected_volunteer = Volunteer.objects.get(volunteerid=selected_id)

        elif 'update_volunteer' in request.POST:
            selected_id = request.POST['volunteerid']
            selected_volunteer = Volunteer.objects.get(volunteerid=selected_id)
            selected_volunteer.name = request.POST['name']
            selected_volunteer.password = request.POST['password']
            selected_volunteer.age = request.POST['age']
            selected_volunteer.gender = request.POST['gender']
            selected_volunteer.contactno = request.POST['contactno']
            selected_volunteer.email = request.POST['email']
            selected_volunteer.address = request.POST['address']
            selected_volunteer.skills = request.POST['skills']
            selected_volunteer.save()
            messages.success(request, f"Volunteer {selected_volunteer.volunteerid} updated successfully!")

        elif 'delete_volunteer' in request.POST:
            selected_id = request.POST['volunteerid']
            Volunteer.objects.filter(volunteerid=selected_id).delete()
            messages.success(request, f"Volunteer {selected_id} has been deleted.")
            selected_volunteer = None  # clear form after deletion

    return render(request, 'admin_manageVol.html', {
        'volunteer_list': volunteer_list,
        'selected_volunteer': selected_volunteer
    })

# Admin Manage Events Page

def admin_manageEvents(request):
    event_list = Event.objects.all()
    selected_event = None

    if request.method == 'POST':
        if 'select_event' in request.POST:
            selected_id = request.POST['eventid']
            selected_event = Event.objects.get(eventid=selected_id)

        elif 'update_event' in request.POST:
            selected_id = request.POST['eventid']
            selected_event = Event.objects.get(eventid=selected_id)
            selected_event.eventname = request.POST['eventname']
            selected_event.eventdate = request.POST['eventdate']
            selected_event.tasks = request.POST['tasks']
            selected_event.volcapacity = request.POST['volcapacity']
            selected_event.token = request.POST['token']
            selected_event.save()
            messages.success(request, f"Event {selected_event.eventid} updated successfully!")

        elif 'delete_event' in request.POST:
            selected_id = request.POST['eventid']
            Event.objects.filter(eventid=selected_id).delete()
            messages.success(request, f"Event {selected_id} has been deleted.")
            selected_event = None

    return render(request, 'admin_manageEvents.html', {
        'event_list': event_list,
        'selected_event': selected_event
    })

# Admin Generate Report Page
def admin_generateReport(request):
    events = Event.objects.all()
    selected_event = None
    applications = []

    if request.method == 'POST':
        eventid = request.POST.get('eventid')
        selected_event = Event.objects.get(eventid=eventid)
        applications = TaskApplication.objects.filter(eventid=selected_event).select_related('volunteerid')

    return render(request, 'admin_generateReport.html', {
        'events': events,
        'selected_event': selected_event,
        'applications': applications
    })
