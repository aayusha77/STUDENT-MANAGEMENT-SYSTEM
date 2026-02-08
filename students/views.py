from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from .models import Student
from .forms import StudentForm

@login_required
def student_list(request):
    # Show all students to everyone
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})

@login_required
def create_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.created_by = request.user
            student.save()
            messages.success(request, "Student created successfully.")
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'students/create_student.html', {'form': form})

@login_required
def update_student(request, id):
    student = get_object_or_404(Student, id=id)

    # Allow admins/staff OR the creator to edit
    if not request.user.is_staff and student.created_by != request.user:
        messages.error(request, "You are not allowed to edit this student.")
        return redirect('student_list')

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully.")
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)

    return render(request, 'students/update_student.html', {'form': form})

@login_required
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)

    # Allow admins/staff OR the creator to delete
    if not request.user.is_staff and student.created_by != request.user:
        messages.error(request, "You are not allowed to delete this student.")
        return redirect('student_list')

    if request.method == 'POST':
        student.delete()
        messages.success(request, "Student deleted successfully.")
        return redirect('student_list')

    return render(request, 'students/delete_student.html', {'student': student})