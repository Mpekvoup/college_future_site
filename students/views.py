from django.shortcuts import render
from django.http import HttpResponse
from .models import Club, Group, Student
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.contrib import messages


def student_list(request):
    students = Student.objects.all()
    return render(request, "index.html", {"students": students})


def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    groups = Group.objects.all()
    clubs = Club.objects.all()
    return render(request, "detail.html", {"student": student,"groups":groups,"clubs":clubs})


def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        student.first_name = request.POST.get("first_name")
        student.last_name = request.POST.get("last_name")
        student.age = request.POST.get("age")

        group_id = request.POST.get("group")
        club_ids = request.POST.getlist("club")

        student.group = Group.objects.get(id=group_id)
        student.save()

        student.club.clear()
        if club_ids:
            clubs = Club.objects.filter(id__in=club_ids)
            student.club.add(*clubs)

        return redirect("student_list")

    groups = Group.objects.all()
    clubs = Club.objects.all()

    return render(request, "edit.html", {
        "student": student,
        "groups": groups,
        "clubs": clubs
    })


def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect("student_list")

def create_student(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        age = request.POST.get('age')
        group_id = request.POST.get('group')
        club_ids = request.POST.getlist('club')

        group = Group.objects.get(id=group_id)
        student = Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            age=age,
            group=group
        )

        if club_ids:
            clubs = Club.objects.filter(id__in=club_ids)
            student.club.add(*clubs)

        return redirect('student_list')

    groups = Group.objects.all()
    clubs = Club.objects.all()
    return render(request, 'create.html', {'groups': groups, 'clubs': clubs})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"]
            )
            messages.success(request, "Регистрация прошла успешно! Теперь войдите в систему.")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "reg.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("student_list")
        else:
            messages.error(request, "Неверное имя пользователя или пароль.")
    return render(request, "login.html")

def user_logout(request):
    logout(request)
    return redirect("login")
