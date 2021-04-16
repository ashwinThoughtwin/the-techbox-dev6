from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from .models import TechItem
from .forms import TechItemUpload, AddEmp


# Create your views here.
@login_required
def dashboard(request):
    fm = TechItemUpload()
    fm2 = AddEmp
    item = TechItem.objects.all()
    context = {'items': item, 'form': fm, 'form2': fm2}
    return render(request, 'index.html', context)


def Loginview(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        else:
            messages.error(request, 'username or password not correct')
            return redirect('/')

    else:
        return render(request, 'login.html', )


class AddEmployee(FormView):
    form_class = AddEmp
    success_url = 'dashboard'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def item_upload(request):
    if request.method == 'POST':
        fm = TechItemUpload(request.POST, request.FILES)

        if fm.is_valid():
            post = fm.save()
            post.user = request.user
            post.save()
            return redirect('dashboard')


def delete_item(request, id):
    if request.method == 'POST':
        model_data = TechItem.objects.get(pk=id)
        model_data.delete()

    return redirect('dashboard')


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")


def error(request):
    return render(request, '404.html')
