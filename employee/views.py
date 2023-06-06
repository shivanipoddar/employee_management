from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from .models import *
from django.db import connection
from .forms import *
import re


def convert_to_json(form_data):
    pattern = r'name="(.*?)"\r\n\r\n(.*?)\r\n'
    matches = re.findall(pattern, form_data.decode())
    data_dict = {key: value for key, value in matches}
    return data_dict


def add_employee_data_to_db(fname, lname, email, phone, address):
    with connection.cursor() as cursor:
        query = "INSERT INTO employee_employeemodel (first_name, last_name, email, phone, address) VALUES (%s, %s, %s, %s, %s)"
        values = (fname, lname, email, phone, address)
        cursor.execute(query, values)
        connection.commit()


class EmployeeView(View):
    template_name = "employee.html"

    def get(self, request, emp_id=0):
        if emp_id != 0:
            employee = EmployeeModel.objects.raw("SELECT id, first_name, last_name, email, phone, address FROM "
                                                 "employee_employeemodel WHERE id = {}".format(emp_id))
            return render(request, 'employee_update.html', {'employees': employee})
        else:
            employee = EmployeeModel.objects.raw("SELECT * FROM employee_employeemodel")
            form = EmpoyeeForm()
            return render(request, self.template_name, {'employees': employee, "form": form})

    def delete(self, request):
        employee = EmployeeModel.objects.raw("DELETE FROM employee_employeemodel WHERE id = {}".format(request.GET['id']))
        return JsonResponse({"status": "success", 'message': 'data deleted'})

    def put(self, request, emp_id):
        data = convert_to_json(request.body)
        EmployeeModel.objects.raw("UPDATE employee_employeemodel SET first_name = '{}', last_name = '{}',"
                                             " email = '{}', phone = '{}', address = '{}' WHERE id = {}".format(data['fname'],
                                                data['lname'], data['email'], data['phone'], data['address'], emp_id))
        return JsonResponse({"status": "success", 'message': 'data updated'})

    def post(self, request, *args, **kwargs):
        form = EmpoyeeForm(request.POST)
        if form.is_valid():
            fname = form.cleaned_data["first_name"]
            lname = form.cleaned_data["last_name"]
            email = request.POST["email"]
            phone = request.POST["phone"]
            address = request.POST["address"]
            add_employee_data_to_db(fname, lname, email, phone, address)
        return redirect('employee')