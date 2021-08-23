from django.shortcuts import render
from django.views.generic.edit import CreateView
from .forms import RegistrationUserForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import redirect


# Create your views here.
class RegistrationUserView(CreateView):
    template_name = 'registration/registration.html'
    form_class = RegistrationUserForm

    def post(self, request, *args, **kwargs):
        form = RegistrationUserForm(request.POST)

        if form.is_valid():
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']

            if password == password2:
                user = User.objects.create_user(username=username, email=email, password=password)

                if user is not None:
                    login(request, user)
                    return redirect('index')

        return render(request, 'register')
