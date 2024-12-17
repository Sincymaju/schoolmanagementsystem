from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from schoolapp.models import Student, CustomUser, LibraryHistory, FeesHistory
from schoolapp.serializer import StudentSerializer, LibraryHistorySerializer, FeesHistorySerializer, CustomUserSerializer

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirect based on user role
            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'staff':
                return redirect('staff_dashboard')
            elif user.role == 'librarian':
                return redirect('librarian_dashboard')
        else:
            # Invalid credentials
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect the user to the login page after logging out


# Views for Admin Functionalities
@login_required
def admin_dashboard(request):
    staff_count = CustomUser.objects.filter(role='staff').count()
    librarian_count = CustomUser.objects.filter(role='librarian').count()
    student_count = Student.objects.count()
    history_count = LibraryHistory.objects.count()
    feehistory_count = FeesHistory.objects.count()

    context = {
        'staff_count': staff_count,
        'librarian_count': librarian_count,
        'student_count': student_count,
        'history_count': history_count,
        'feehistory_count' : feehistory_count,
    }

    return render(request, 'admin_dashboard.html', context)


# CRUD for Students
# List all students
@login_required
def list_students(request):
    students = Student.objects.all()  # Get all students from the database
    return render(request, 'list_students.html', {'students': students})

@login_required
def create_student(request):
    if request.method == 'POST':
        name = request.POST['name']
        age = request.POST['age']
        grade = request.POST['grade']
        Student.objects.create(name=name, age=age, grade=grade)
        return redirect('list_students')  # Redirect to the list of students after creating
    return render(request, 'create_student.html')



@login_required
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.name = request.POST['name']
        student.age = request.POST['age']
        student.grade = request.POST['grade']
        student.save()
        return redirect('list_students')  # Redirect to the list of students after editing
    return render(request, 'edit_student.html', {'student': student})



@login_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return redirect('admin_dashboard')  # Redirect to the list of students after deletion




# Manage Staff and Librarians
from django.contrib import messages  # For user feedback messages

from django.utils.datastructures import MultiValueDictKeyError
@login_required
def list_users(request, role=None):
    """
    List all users, optionally filtered by role (e.g., 'staff' or 'librarian').
    """
    if role:
        users = CustomUser.objects.filter(role=role)  # Filter by role if provided
    else:
        users = CustomUser.objects.all()  # Retrieve all users if no role is specified
    
    return render(request, 'list_users.html', {'users': users, 'role': role})


@login_required
def create_user(request, role):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']
            phone_number = request.POST.get('phone_number', '')  # Optional field
            address = request.POST.get('address', '')  # Optional field
        except MultiValueDictKeyError as e:
            messages.error(request, f"Missing field: {str(e)}")
            return render(request, 'create_user.html', {'role': role})

        # Validate unique username and email
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'create_user.html', {'role': role})
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, 'create_user.html', {'role': role})

        # Create the user
        CustomUser.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            phone_number=phone_number,
            address=address,
            role=role,
        )
        messages.success(request, f"{role.capitalize()} created successfully.")
        return redirect('list_users', role=role)  # Redirect to the filtered user list
    return render(request, 'create_user.html', {'role': role})


from django.utils.datastructures import MultiValueDictKeyError

@login_required
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        try:
            user.username = request.POST['username']
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.phone_number = request.POST.get('phone_number', '')  # Optional field
            user.address = request.POST.get('address', '')  # Optional field
            user.save()
            messages.success(request, "User details updated successfully.")
            return redirect('list_users', role=user.role)  # Redirect to the filtered user list
        except MultiValueDictKeyError as e:
            messages.error(request, f"Missing field: {str(e)}")
            return render(request, 'edit_user.html', {'user': user})
    return render(request, 'edit_user.html', {'user': user})



@login_required
def delete_user(request, user_id):
    """
    Admin can delete a staff or librarian account.
    """
    user = get_object_or_404(CustomUser, id=user_id)
    role = user.role
    user.delete()
    messages.success(request, "User deleted successfully.")
    return redirect('list_users', role=role)  # Redirect to the filtered user list

    

@login_required
def list_library_history(request):
    """
    View to list all library histories.
    """
    histories = LibraryHistory.objects.select_related('student').all()
    return render(request, 'list_library_history.html', {'histories': histories})


@login_required
def create_library_history(request):
    """
    View to create a new library history entry.
    """
    if request.method == 'POST':
        student_id = request.POST['student_id']
        book_title = request.POST['book_title']
        issue_date = request.POST['issue_date']
        return_date = request.POST['return_date']

        # Fetch the student object
        student = get_object_or_404(Student, id=student_id)

        # Create a new library history record
        LibraryHistory.objects.create(
            student=student,
            book_title=book_title,
            issue_date=issue_date,
            return_date=return_date
        )
        return redirect('list_library_history')

    students = Student.objects.all()
    return render(request, 'create_library_history.html', {'students': students})


@login_required
def edit_library_history(request, history_id):
    """
    View to edit an existing library history entry.
    """
    history = get_object_or_404(LibraryHistory, id=history_id)

    if request.method == 'POST':
        try:
            history.book_title = request.POST['book_title']
            history.issue_date = request.POST['issue_date']
            history.return_date = request.POST['return_date']
            history.save()
            messages.success(request, "Library history updated successfully.")
            return redirect('list_library_history')
        except KeyError as e:
            messages.error(request, f"Missing field: {str(e)}")
            return render(request, 'edit_library_history.html', {'history': history})

    return render(request, 'edit_library_history.html', {'history': history})


@login_required
def delete_library_history(request, history_id):
    """
    View to delete a library history entry.
    """
    history = get_object_or_404(LibraryHistory, id=history_id)
    history.delete()
    messages.success(request, "Library history deleted successfully.")
    return redirect('list_library_history')


# CRUD for Fees History
# List all fees history
@login_required
def list_fees_history(request):
    fees_history = FeesHistory.objects.all()  # Get all fees history from the database
    return render(request, 'list_fees_history.html', {'fees_history': fees_history})

# Create a new fees history entry
@login_required
def create_fees_history(request):
    if request.method == 'POST':
        student_id = request.POST['student_id']
        amount = request.POST['amount']
        payment_date = request.POST['payment_date']
        student = get_object_or_404(Student, id=student_id)
        
        # Create new fees history entry
        FeesHistory.objects.create(student=student, amount=amount, payment_date=payment_date)
        
        # Redirect to the fees history list
        return redirect('list_fees_history')

    # Fetch all students to show in the dropdown list
    students = Student.objects.all()
    return render(request, 'create_fees_history.html', {'students': students})



# Edit a specific fees history
@login_required
def edit_fees_history(request, history_id):
    history = get_object_or_404(FeesHistory, id=history_id)
    if request.method == 'POST':
        history.amount = request.POST['amount']
        history.payment_date = request.POST['payment_date']
        history.save()
        return redirect('list_fees_history')
    return render(request, 'edit_fees_history.html', {'history': history})



@login_required
def delete_fees_history(request, history_id):
    history = get_object_or_404(FeesHistory, id=history_id)
    history.delete()
    return redirect('list_fees_history')    

#staff dashboard


from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
'''
# Restrict access to staff role
def staff_only(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'staff':  # Ensure the user is a staff member
            return HttpResponseForbidden("You do not have permission to access this page.")
        return view_func(request, *args, **kwargs)
    return wrapper
'''
@login_required
#@staff_only
def staff_dashboard(request):
    return render(request, 'staff_dashboard.html')

@login_required
def list_students_for_staff(request):
    students = Student.objects.all()
    return render(request, 'list_studentsforstaff.html', {'students': students})
@login_required
def library_historyforstaff(request):
    history = LibraryHistory.objects.select_related('student').all()
    return render(request, 'library_historyforstaff.html', {'history': history})
    

@login_required
def list_fees_for_staff(request):
    fees = FeesHistory.objects.select_related('student').all()
    return render(request, 'list_feesforstaff.html', {'fees': fees})
@login_required
def add_feeforstaff(request):
    if request.method == 'POST':
        student_id = request.POST['student_id']
        amount = request.POST['amount']
        payment_date = request.POST['payment_date']

        student = get_object_or_404(Student, id=student_id)
        FeesHistory.objects.create(student=student, amount=amount, payment_date=payment_date)
        return redirect('list_feesforstaff')

    students = Student.objects.all()  # For selecting a student
    return render(request, 'add_feeforstaff.html', {'students': students})
@login_required
def delete_feeforstaff(request, fee_id):
    fee = get_object_or_404(FeesHistory, id=fee_id)
    fee.delete()
    return redirect('list_feesforstaff')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from schoolapp.models import FeesHistory, Student

@login_required
#@staff_only
def edit_feeforstaff(request, fee_id):
    # Retrieve the fee record by ID
    fee = get_object_or_404(FeesHistory, id=fee_id)

    if request.method == 'POST':
        # Update fee record with the new data
        student_id = request.POST['student_id']
        amount = request.POST['amount']
        payment_date = request.POST['payment_date']

        # Fetch the updated student record
        student = get_object_or_404(Student, id=student_id)

        # Update fee details
        fee.student = student
        fee.amount = amount
        fee.payment_date = payment_date
        fee.save()

        # Redirect to the fees management page
        return redirect('list_feesforstaff')

    # Fetch all students for the dropdown list
    students = Student.objects.all()

    return render(request, 'edit_feeforstaff.html', {'fee': fee, 'students': students})

'''
#librarian dashboard
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from schoolapp.models import Student, LibraryHistory
from django.urls import reverse
from django.http import HttpResponseRedirect

@login_required
def librarian_dashboard(request):
    return render(request, 'librarian_dashboard.html')

# View all students
@login_required
def list_students_for_librarian(request):
    students = Student.objects.all()
    return render(request, 'list_students_for_librarian/list_studentsforlib.html', {'students': students})

# List library history
@login_required
def list_library_history_for_librarian(request):
    history = LibraryHistory.objects.all()
    return render(request, 'librarian/library_historyforlib.html', {'history': history})

# Create library history
@login_required
def create_library_history_for_librarian(request):
    students = Student.objects.all()

    if request.method == 'POST':
        student_id = request.POST['student_id']
        book_title = request.POST['book_title']
        issue_date = request.POST['issue_date']
        return_date = request.POST.get('return_date', None)

        student = get_object_or_404(Student, id=student_id)
        LibraryHistory.objects.create(
            student=student,
            book_title=book_title,
            issue_date=issue_date,
            return_date=return_date,
        )
        return redirect('list_library_history')

    return render(request, 'librarian/add_library_historyforlib.html', {'students': students})

# Edit library history
@login_required
def edit_library_history_for_librarian(request, pk):
    history = get_object_or_404(LibraryHistory, id=pk)
    students = Student.objects.all()

    if request.method == 'POST':
        history.student = get_object_or_404(Student, id=request.POST['student_id'])
        history.book_title = request.POST['book_title']
        history.issue_date = request.POST['issue_date']
        history.return_date = request.POST.get('return_date', None)
        history.save()
        return redirect('list_library_history')

    return render(request, 'librarian/edit_library_historyforlib.html', {'history': history, 'students': students})

# Delete library history
@login_required
def delete_library_history_for_librarian(request, pk):
    history = get_object_or_404(LibraryHistory, id=pk)

    if request.method == 'POST':
        history.delete()
        return redirect('list_library_history')

    return render(request, 'librarian/delete_library_history.html', {'history': history})
'''




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from schoolapp.models import LibraryHistory, Student
from django.http import HttpResponseRedirect
from django.urls import reverse

# Librarian Dashboard
@login_required
def librarian_dashboard(request):
    return render(request, 'librarian_dashboard.html')

# List Students for Librarian
@login_required
def list_students_for_librarian(request):
    students = Student.objects.all()
    return render(request, 'list_studentsforlib.html', {'students': students})

# List Library History for Librarian
@login_required
def list_library_history_for_librarian(request):
    history = LibraryHistory.objects.all()
    return render(request, 'library_historyforlib.html', {'history': history})

from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

@login_required
def create_library_history_for_librarian(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        book_title = request.POST.get('book_title')
        issue_date = request.POST.get('issue_date')
        return_date = request.POST.get('return_date')

        # Fetch the student object
        student = get_object_or_404(Student, id=student_id)

        try:
            # Handle empty return_date field
            if not return_date:
                return_date = None  # Allow null values for optional dates

            # Create a new library history record
            LibraryHistory.objects.create(
                student=student,
                book_title=book_title,
                issue_date=issue_date,
                return_date=return_date
            )

            # Add success message
            messages.success(request, "Library history added successfully.")
            return redirect('list_library_history')  # Redirect to the list page
        except ValidationError as e:
            messages.error(request, f"Error: {e.messages}")

    # Pass students to the form for selection
    students = Student.objects.all()
    return render(request, 'add_library_historyforlib.html', {'students': students})


# Edit Library History
@login_required
def edit_library_history_for_librarian(request, pk):
    library_history = get_object_or_404(LibraryHistory, pk=pk)

    if request.method == 'POST':
        library_history.student_id = request.POST.get('student_id')
        library_history.book_title = request.POST.get('book_title')
        library_history.issue_date = request.POST.get('issue_date')
        library_history.return_date = request.POST.get('return_date')
        library_history.save()

        return redirect('library_historyforlib.html')

    students = Student.objects.all()
    return render(request, 'edit_library_historyforlib.html', {
        'library_history': library_history,
        'students': students
    })

# Delete Library History
@login_required
def delete_library_history_for_librarian(request, pk):
    library_history = get_object_or_404(LibraryHistory, pk=pk)
    library_history.delete()
    return redirect('library_historyforlib.html')
