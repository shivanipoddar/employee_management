from django.shortcuts import render, redirect
from django.views import View
from .forms import TaskForm
from .models import *


class TaskView(View):
    template_name = "task.html"

    def get(self, request):
        if request.session.get('is_admin'):
            form = TaskForm
            return render(request, self.template_name, {'form': form})
        else:
            return redirect('user')

    # def delete(self, request):
    #     id = request.GET['id']
    #     UserModel.objects.raw("DELETE FROM users_usermodel WHERE id = {}".format(id))
    #     return JsonResponse({"status": "success", 'message': 'data deleted'})

    # def put(self, request, user_id):
    #     data = convert_to_json(request.body)
    #     UserModel.objects.raw("UPDATE employee_employeemodel SET first_name = '{}', last_name = '{}',"
    #                                          " email = '{}', phone = '{}', address = '{}' WHERE id = {}".format(data['fname'],
    #                                             data['lname'], data['email'], data['phone'], data['address'], user_id))
    #     return JsonResponse({"status": "success", 'message': 'data updated'})

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["assign_to"]
            task = form.cleaned_data["task"]

            # add_user_data_to_db(fname, lname, email, phone, address, password, document)
            TaskModel.objects.create(assign_to=user, task=task)
        return redirect('user')


# class AddTaskView(View):
#     template_name = "task.html"
#
#     def get(self, request):
#         form = TaskForm
#         return render(request, self.template_name, {'form': form})
#
#     # def delete(self, request):
#     #     id = request.GET['id']
#     #     UserModel.objects.raw("DELETE FROM users_usermodel WHERE id = {}".format(id))
#     #     return JsonResponse({"status": "success", 'message': 'data deleted'})
#
#     # def put(self, request, user_id):
#     #     data = convert_to_json(request.body)
#     #     UserModel.objects.raw("UPDATE employee_employeemodel SET first_name = '{}', last_name = '{}',"
#     #                                          " email = '{}', phone = '{}', address = '{}' WHERE id = {}".format(data['fname'],
#     #                                             data['lname'], data['email'], data['phone'], data['address'], user_id))
#     #     return JsonResponse({"status": "success", 'message': 'data updated'})
#
#     def post(self, request, *args, **kwargs):
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             user = form.cleaned_data["assign_to"]
#             task = form.cleaned_data["task"]
#
#             # add_user_data_to_db(fname, lname, email, phone, address, password, document)
#             TaskModel.objects.create(assign_to=user, task=task)
#         return redirect('user')


