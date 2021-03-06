from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django_tables2 import RequestConfig

from management.models import Students
from management.tables import StudentsTable
from management.forms import AddStudentForm
from management.forms import DeleteStudentForm

@login_required
def index(request):
    if request.user.is_admin:
        return redirect('management:admin')
    else:
        return redirect('management:home')

@login_required
def home(request):
    student = get_object_or_404(Students, account=request.user)

    context = {
            'student': student,
    }

    return render(request, 'management/student_home.html', context)
    # response = render(request, 'management/student_home.html', context)
    # response.set_cookie("cookie_example",1)
    # return response

@login_required
def admin(request):
    if request.user.is_admin:
        table = StudentsTable(Students.objects.all())
        RequestConfig(request, paginate={"per_page": 25}).configure(table)

        context = {
            'table': table,
        }

        return render(request, 'management/admin.html', context)
    else:
        raise PermissionDenied

@login_required
def student(request, student):
    if request.user.is_admin:
        student = get_object_or_404(Students, student_id=student)
        form = AddStudentForm(request.POST or None, request.FILES or None, instance=student)
        if request.POST and request.FILES and form.is_valid():
            student = form.save()
            form = AddStudentForm(instance=student)

        context = {
            'form': form,
            'student': student,
        }

        return render(request, 'management/student_home.html', context)
    else:
        raise PermissionDenied

@login_required
def add(request):
    if request.user.is_admin:
        title = 'Add new student'
        form = AddStudentForm(request.POST or None, request.FILES or None)
        if request.POST and request.FILES and form.is_valid():
            student = form.save()
            form = AddStudentForm()
            form.is_valid = True

        context = {
                'form': form,
                'title':title,
        }

        return render(request, 'management/forms/add.html', context)
    else:
        raise PermissionDenied

@login_required
def delete(request, student):
    if request.user.is_admin:
        student = get_object_or_404(Students, student_id=student)
        title = "Delete Student %s" % (student.get_full_name())
        form = DeleteStudentForm(request.POST or None, instance=student)
        if request.POST and form.is_valid():
            student.delete()
            return redirect('management:admin')

        context = {
                'student': student,
                'form': form,
                'title':title,
        }

        return render(request, 'management/forms/delete.html', context)
    else:
        raise PermissionDenied
