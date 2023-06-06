from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from .models import *
from employee.models import EmployeeModel
from task.models import *
from django.db import connection
from .forms import *


def add_employee_data_to_db(fname, lname, email, phone, address, user):
    with connection.cursor() as cursor:
        query = "INSERT INTO employee_employeemodel (first_name, last_name, email, phone, address, user_id) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (fname, lname, email, phone, address, user)
        cursor.execute(query, values)
        connection.commit()


class AddUserView(View):
    template_name = "add_user.html"

    def get(self, request):
        form = UserForm()
        return render(request, self.template_name, {"form": form})


class UserView(View):
    template_name = "user.html"

    def get(self, request):
        if request.session.get('user'):
            if request.session.get('is_admin'):
                users = EmployeeModel.objects.raw("SELECT * FROM employee_employeemodel")
                task = TaskModel.objects.raw("SELECT * FROM task_taskmodel")
                form = UserForm()
                return render(request, self.template_name, {"form": form, "users": users, 'tasks': task})
            else:
                task = TaskModel.objects.filter(assign_to__first_name=request.session.get('user'))
                return render(request, self.template_name, {'tasks': task})
        else:
            return redirect('login')

    def delete(self, request):
        user_id = request.GET['id']
        EmployeeModel.objects.raw("DELETE FROM employee_employeemodel WHERE id = {}".format(user_id))
        return JsonResponse({"status": "success", 'message': 'data deleted'})

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            fname = form.cleaned_data["first_name"]
            lname = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            phone = form.cleaned_data["phone"]
            address = form.cleaned_data["address"]
            password = form.cleaned_data["password"]
            document = request.FILES["document"]
            user = UserModel.objects.create(first_name=fname, last_name=lname, email=email, phone=phone, address=address,
                                     password=password, document=document)
            add_employee_data_to_db(fname, lname, email, phone, address, user.id)
        return redirect('user')


class LoginView(View):
    template_name = "login.html"

    def get(self, request):
        if request.session.get('user'):
            return redirect('user')
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        try:
            user = UserModel.objects.filter(email=request.POST['email'])[0]
            password = request.POST['password']
            if user:
                if user.password == password:
                    request.session['user'] = user.first_name
                    request.session['is_admin'] = user.is_admin
                    return redirect('user')
            return render(request, self.template_name)
        except:
            return redirect('login')


class RegisterView(View):
    template_name = "register.html"

    def get(self, request):
        if request.session.get('user'):
            return redirect('user')
        form = UserForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            fname = form.cleaned_data["first_name"]
            lname = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            phone = form.cleaned_data["phone"]
            address = form.cleaned_data["address"]
            password = form.cleaned_data["password"]
            document = request.FILES["document"]
            user = UserModel.objects.create(first_name=fname, last_name=lname, email=email, phone=phone, address=address,
                                     password=password, document=document)
            add_employee_data_to_db(fname, lname, email, phone, address, user.id)
        return redirect('user')


class LogoutView(View):
    template_name = "login.html"

    def get(self, request):
        request.session['user'] = None
        return redirect('login')
