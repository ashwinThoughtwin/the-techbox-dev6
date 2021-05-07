from django.conf import settings
import datetime
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic.base import View
from django.views.generic.edit import FormView

from the_tech_box.settings import STRIPE_PRIVATE_KEY
from .models import TechItem, Employee, AllottedItem
from .forms import TechItemUpload, AddEmp, AllotItems, UpdateEmp
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from .tasks import send_email_task, send_remember_task
from django.views.decorators.cache import cache_page
import stripe

stripe.api_key = 'sk_test_51InHHySHe26ILC3WN3MX4uoOYN9fu51hxV1oX9bHcag4D888kFxhKNcPt7eVHLMyhsKm0Od9VUEGgrpAhbMku0u500S56eI9nY'


# Create your views here.

class DashBoardView(View):

    # @method_decorator(cache_page(60 * 30))
    @method_decorator(login_required(login_url="login"))
    def get(self, request):
        fm = TechItemUpload()
        fm2 = AddEmp()
        item = TechItem.objects.all()
        item_count = TechItem.objects.all().count()
        employee_count = Employee.objects.all().count()
        issued_tool = AllottedItem.objects.all().count()
        context = {
            'items': item,
            'form': fm,
            'form2': fm2,
            'item_count': item_count,
            'employee_count': employee_count,
            'issued_tool': issued_tool,
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

        if request.user.is_authenticated:
            return redirect('dashboard')

        else:
            return render(request, 'login.html')


class ItemUpload(View):

    def post(self, request):
        fm = TechItemUpload(request.POST, request.FILES)

        if fm.is_valid():
            post = fm.save()
            post.user = request.user
            post.save()
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

    @method_decorator(login_required(login_url="login"))
    def get(self, request):
        fm1 = TechItemUpload()
        item = TechItem.objects.all()
        context = {'form': fm1, 'item': item}
        return render(request, 'additem.html', context)


# class AddEmployee(FormView):
#     form_class = AddEmp
#     success_url = 'employee'
#
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)
class AddEmployee(View):

    def post(self, request):
        print(request.POST)
        form = AddEmp(request.POST)
        print(form)
        if form.is_valid():
            name = request.POST['name']
            email = request.POST['email']
            address = request.POST['address']
            mobile = request.POST['mobile']
            team = request.POST['team']
            emp = Employee.objects.create(name=name, email=email, address=address,
                                          mobile=mobile, team=team)

            emp.save()
            data = {
                'employee': emp
            }
            return render(request, 'newemployee.html', data)
        else:
            return JsonResponse({'status': 0})


class UpdateEmployee(View):

    @method_decorator(login_required(login_url="login"))
    def get(self, request, id):
        try:
            model_data = Employee.objects.get(pk=id)
            fm = UpdateEmp(instance=model_data)
            return render(request, 'updateemployee.html', {'form': fm})

        except Employee.DoesNotExist:
            return render(request, '404.html')

    def post(self, request, id):
        model_data = Employee.objects.get(pk=id)
        fm = UpdateEmp(request.POST, instance=model_data)
        if fm.is_valid:
            fm.save()
            return redirect('employee_table')


# class UpdateEmployee(View):
#
#     def post(self, request, id):
#         model_data = Employee.objects.get(pk=id)
#         fm = UpdateEmp(request.POST, instance=model_data)
#         if fm.is_valid:
#             fm.save()
#             return redirect('employee_table')


class EmployeeTable(View):

    @method_decorator(login_required(login_url="login"))
    def get(self, request, ):
        employee = Employee.objects.all()
        fm2 = AddEmp

        form2 = UpdateEmp()
        context = {'employee': employee, 'form': fm2, 'form2': form2}
        return render(request, 'employee.html', context)


class AllotItem(View):

    def post(self, request):
        form = AllotItems(request.POST)
        if form.is_valid():
            techitem = form.cleaned_data['tech_item']
            issuedate = form.cleaned_data['issue_date']
            enddate = form.cleaned_data['end_date']
            # import pdb;
            # pdb.set_trace()
            form.save()
            emp = Employee.objects.get(id=request.POST.get('employee_name'))
            email = emp.email
            print(email)

            scheduled_date = AllottedItem.objects.latest('nowdate')
            a = scheduled_date.issue_date
            b = scheduled_date.end_date
            c = (b - a).total_seconds()
            print(c)

            subject = f'Confirmation Email from TheTechBox '
            message = f'Hello {emp.name}, We have allotted "{techitem}" to you , Please collect your Techitem ' \
                      f'on the Date "{issuedate}" . ' \
                      f'The end date of your Techitem is "{enddate}"\n \n' \
                      f'Thankyou,\n' \
                      f'TheTechBox'

            subject_remember = f'Remembring Email from TheTechBox '
            message_remember = f'Hello {emp.name},' \
                               f' Your time for submitting "{techitem}" is end on "{enddate}" ' \
                               f' Please submit your techitem on time.\n \n ' \
                               f'Thankyou,\n' \
                               f'TheTechBox'

            send_email_task.delay(subject, message, email)
            # send_email_task.apply_async((subject, message, email), countdown=0)

            send_remember_task.apply_async((subject_remember, message_remember, email), countdown=c)
            return redirect('allot-items')

    @method_decorator(login_required(login_url="login"))
    def get(self, request):
        form = AllotItems()
        items = AllottedItem.objects.all()
        context = {'item': items, 'forms': form}
        return render(request, 'allotitem.html', context)


class AllottedItemsDelete(View):

    def post(self, request):
        allot_id = request.POST.get('del_id')
        tool = AllottedItem.objects.get(pk=allot_id)
        tool.delete()
        return redirect('allot-items')


class DeleteEmployee(View):

    def post(self, request):
        emp_id = request.POST.get('del_id')
        model_data = Employee.objects.get(pk=emp_id)
        model_data.delete()
        return redirect('employee_table')


class DeleteItem(View):

    def post(self, request):
        item_id = request.POST.get('del_id')
        model_data = TechItem.objects.get(pk=item_id)
        model_data.delete()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


class DonationPage(View):

    def get(self, request):
        return render(request, 'donation.html')


class Charge(View):

    def post(self, request):
        amount = int(request.POST['amount'])
        print('data:', request.POST)
        customer = stripe.Customer.create(
                email=request.POST['email'],
                name=request.POST['name'],
                source=request.POST['stripeToken'],
            )
        charge = stripe.Charge.create(
            customer=customer,
            amount=amount*100,
            currency='inr',
            description="Donation"
        )

        return redirect(reverse('success', args=[amount]))


class Success(View):

    def get(self, request, args):
        amount = args
        return render(request, 'success.html', {'amount': amount})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")


def handler404(request, exception=None):
    return render(request, '404.html')
