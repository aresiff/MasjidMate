from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='homepage'),

     # Login views
    path('adminlogin/', views.admin_login, name='adminlogin'),
    path('committeelogin/', views.committee_login, name='committeelogin'),
    path('volunteerlogin/', views.volunteer_login, name='volunteerlogin'),

    # Dashboard redirects
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('committee/dashboard/', views.committee_dashboard, name='committee_dashboard'),
    path('volunteer/dashboard/', views.volunteer_dashboard, name='volunteer_dashboard'),

    # Signup views
    path('committeesignup/', views.committee_signup, name='committeesignup'),
    path('volunteersignup/', views.volunteer_signup, name='volunteersignup'),

    # Volunteer Urls
    path('volunteer/profile/', views.volunteer_profile, name='volunteer_profile'),
    path('volunteer/taskdetails/', views.volunteer_taskdetails, name='volunteer_taskdetails'),
    path('volunteer/mosquevent/', views.volunteer_mosquevent, name='volunteer_mosquevent'),
    path('volunteer/mosquevent/confirm/', views.volunteer_confirmapply, name='volunteer_confirmapply'),
    path('volunteer/mosquevent/confirmed/', views.volunteer_apply_confirmed, name='volunteer_apply_confirmed'),

    # Committee Urls
    path('committee/dashboard/', views.committee_dashboard, name='committee_dashboard'),
    path('committee/profile/', views.committee_profile, name='committee_profile'),
    path('committee/approve/', views.committee_approveVol, name='committee_approveVol'),
    path('committee/recordperformance/', views.committee_recordperformance, name='committee_recordperformance'),
    path('committee/recordevent/', views.committee_recordevent, name='committee_recordevent'),
    path('committee/historyevent/', views.committee_historyEvent, name='committee_historyEvent'),

    # Admin Urls
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/profile/', views.profile_admin, name='profile_admin'),
    path('admin/managevol/', views.admin_manageVol, name='admin_manageVol'),  # placeholder
    path('admin/manageevents/', views.admin_manageEvents, name='admin_manageEvents'),  # placeholder
    path('admin/generatereport/', views.admin_generateReport, name='admin_generateReport'),

]