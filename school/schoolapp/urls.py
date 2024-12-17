from django.urls import path
from django.contrib.auth import views as auth_views
from .views import login_view, admin_dashboard, staff_dashboard, librarian_dashboard, create_student, edit_student, delete_student, create_user, delete_user 
from .views import edit_user, create_library_history, edit_library_history, delete_library_history, create_fees_history, edit_fees_history, delete_fees_history
from .views import list_students, list_users,list_library_history, list_fees_history, logout_view
from .views import list_students_for_staff, library_historyforstaff, list_fees_for_staff, add_feeforstaff, delete_feeforstaff, edit_feeforstaff
from .views import list_students_for_librarian, list_library_history_for_librarian, create_library_history_for_librarian, edit_library_history_for_librarian, delete_library_history_for_librarian
urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'), 
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('students/', list_students, name='list_students'),
    path('create_student/', create_student, name='create_student'),
    path('edit_student/<int:student_id>/', edit_student, name='edit_student'),
    path('delete_student/<int:student_id>/', delete_student, name='delete_student'),
    path('users/<str:role>/', list_users, name='list_users'),
    path('create_user/<str:role>/', create_user, name='create_user'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('edit_user/<int:user_id>/', edit_user, name='edit_user'),
    # Library History Management
    path('library-history/', list_library_history, name='list_library_history'),
    path('create_library_history/', create_library_history, name='create_library_history'),
    path('edit_library_history/<int:history_id>/', edit_library_history, name='edit_library_history'),
    path('delete_library_history/<int:history_id>/', delete_library_history, name='delete_library_history'),

    # Fees History Management
    path('fees-history/', list_fees_history, name='list_fees_history'),
    path('create_fees_history/', create_fees_history, name='create_fees_history'),
    path('edit_fees_history/<int:history_id>/', edit_fees_history, name='edit_fees_history'),
    path('delete_fees_history/<int:history_id>/', delete_fees_history, name='delete_fees_history'),

    path('staff_dashboard/', staff_dashboard, name='staff_dashboard'),
    path('student/', list_students_for_staff, name='list_studentsforstaff'),
    path('library_history_staff/', library_historyforstaff, name='library_history_staff'),
    
    path('list_feesforstaff/', list_fees_for_staff, name='list_feesforstaff'),

    path('fees/add/', add_feeforstaff, name='add_fee'),
    path('fees/delete/<int:fee_id>/', delete_feeforstaff, name='delete_fee'),
    path('fees/edit/<int:fee_id>/', edit_feeforstaff, name='edit_fee'),


    path('librarian_dashboard/', librarian_dashboard, name='librarian_dashboard'),
    path('list_students_for_librarian/', list_students_for_librarian, name='list_students_for_librarian'),
    path('list_library_history/', list_library_history_for_librarian, name='list_library_history'),

    path('add_library_history/', create_library_history_for_librarian, name='add_library_history'),
    path('edit_library_history/<int:pk>/', edit_library_history_for_librarian, name='edit_library_history'),
    path('delete_library_history/<int:pk>/', delete_library_history_for_librarian, name='delete_library_history'),
]
