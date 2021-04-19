from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from django.views.generic.edit import FormView
from .models import TechItem, Employee, AllottedItem
from .forms import TechItemUpload, AddEmp, AllotItems
from django.utils.decorators import method_decorator


# Create your views here.
class DashBoardView(View):

    @method_decorator(login_required(login_url="login"))
    def get(self, request):
        fm = TechItemUpload()
        fm2 = AddEmp()
        item = TechItem.objects.all()
        item_count = TechItem.objects.all().count()
        employee_count = Employee.objects.all().count()
        context = {
            'items': item,
            'form': fm,
            'form2': fm2,
            'item_count': item_count,
            'employee_count': employee_count,
        }
        return render(request, 'index.html', context)


class Loginview(View):

    def post(self, request):

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        else:
            messages.error(request, 'username or password not correct')
            return redirect('login')

    def get(self, request):
        return render(request, 'login.html')


class ItemUpload(View):

    def post(self, request):
        fm = TechItemUpload(request.POST, request.FILES)

        if fm.is_valid():
            post = fm.save()
            post.user = request.user
            post.save()
            return redirect('dashboard')

    @method_decorator(login_required(login_url="login"))
    def get(self, request):
        fm1 = TechItemUpload()
        context = {'form': fm1}
        return render(request, 'additem.html', context)


class AddEmployee(FormView):
    form_class = AddEmp
    success_url = 'employee'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class EmployeeTable(View):

    @method_decorator(login_required(login_url="login"))
    def get(self, request):
        employee = Employee.objects.all()
        fm2 = AddEmp()
        context = {'employee': employee, 'form': fm2}
        return render(request, 'employee.html', context)


class AllotItem(View):

    def post(self, request):
        form = AllotItems(request.POST)
        if form.is_valid():
            post = form.save()
            post.user = request.user
            post.save()
            return redirect('allot-items')

    @method_decorator(login_required(login_url="login"))
    def get(self, request):
        form = AllotItems()
        items = AllottedItem.objects.all()
        context = {'item': items, 'forms': form}
        return render(request, 'allotitem.html', context)


def delete_item(request, id):
    if request.method == 'POST':
        model_data = TechItem.objects.get(pk=id)
        model_data.delete()

    return redirect('dashboard')


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")


def handler404(request, exception=None):
    return render(request, '404.html')
