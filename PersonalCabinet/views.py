from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from Cinema.models import UserFilmStatus, Film, Genre
from PersonalCabinet.forms import UserPrivacyForm
from PersonalCabinet.models import UserPrivacy


# Create your views here.
class PersonalCabinetView(TemplateView):
    template_name = 'PersonalCabinet/personal_cabinet.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['userPrivacyForm'] = UserPrivacyForm()
        context['userPrivacyForm'].fields['isPrivacy'].initial = UserPrivacy.objects.get(user=kwargs['userId']).isPrivacy
        context['userPrivacy'] = UserPrivacy.objects.get(user=kwargs['userId']).isPrivacy
        context['genres'] = Genre.objects.all()
        user = kwargs['userId']
        context['currentUser'] = self.request.user
        context['requiredUser'] = User.objects.get(id=user)
        context['isCabinetOwner'] = False
        if self.request.user.id == user:
            context['isCabinetOwner'] = True
        status_p_films = UserFilmStatus.objects.filter(userId=user, status='p')
        context['status_p_films'] = status_p_films
        status_l_films = UserFilmStatus.objects.filter(userId=user, status='l')
        context['status_l_films'] = status_l_films
        status_t_films = UserFilmStatus.objects.filter(userId=user, status='t')
        context['status_t_films'] = status_t_films
        return context

    def post(self, request, *args, **kwargs):
        form = UserPrivacyForm(request.POST)

        if form.is_valid():
            obj = UserPrivacy.objects.get(user=request.user)
            obj.isPrivacy = form.instance.isPrivacy
            obj.save()

        return redirect('cabinet', request.user.id)


def deleteFilmStatus(request, filmId):
    obj = UserFilmStatus.objects.get(userId=request.user, filmId=filmId)
    obj.delete()
    return redirect('cabinet', request.user.id)


def setFilmStatus(request, filmId):
    if request.user.is_authenticated:
        status = request.POST['selectFilmStatus']
        if UserFilmStatus.objects.filter(userId=request.user, filmId=filmId).exists():
            obj = UserFilmStatus.objects.get(filmId=filmId, userId=request.user)
            obj.status = status
            obj.save()
        else:
            obj = UserFilmStatus()
            obj.status = status
            obj.filmId = Film.objects.get(id=filmId)
            obj.userId = request.user
            obj.save()

        return redirect('cabinet', request.user.id)
    else:
        return redirect('index')
