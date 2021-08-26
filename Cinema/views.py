from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Film, Genre, Review, RatingStar, RatingFilm
from .forms import ReviewForm
from django.db.models import Avg


# Create your views here.
def set_rating(request, value):
    current_film = Film.objects.get(id=request.session['current_film'])
    star = RatingStar.objects.get(value=value)
    user = request.user
    if request.user.is_authenticated:
        if not RatingFilm.objects.filter(filmId=current_film, userId=user).exists():
            newRating = RatingFilm()
            newRating.filmId = current_film
            newRating.userId = request.user
            newRating.stars = star
            newRating.save()
        else:
            updateRating = RatingFilm.objects.get(filmId=current_film, userId=user)
            updateRating.stars = star
            updateRating.save()

        updateRatingValue(request, current_film)

        return redirect('detail', url=current_film.url)
    else:
        return redirect('detail', url=current_film.url)


def updateRatingValue(request, film):
    aggr_value = RatingFilm.objects.filter(filmId=film).aggregate(Avg('stars__value'))
    film.rating = aggr_value['stars__value__avg']
    film.save()


def give_review(request, url):
    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            form.instance.user = request.user
            form.instance.film = Film.objects.get(url=url)
            form.save()

    return redirect('detail', url)


class CinemaView(TemplateView):
    template_name = 'Cinema/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['films'] = Film.objects.all()
        context['genres'] = Genre.objects.all()
        context['bestFilms'] = Film.objects.all()[0:3]

        return context


class CinemaDetailView(DetailView):
    template_name = 'Cinema/detail.html'
    model = Film
    slug_url_kwarg = 'url'
    slug_field = 'url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviewsAreExists'] = False
        context['films'] = Film.objects.all()
        context['genres'] = Genre.objects.all()
        self.request.session['current_film'] = Film.objects.get(url=self.kwargs['url']).id
        context['reviews'] = Review.objects.filter(film=Film.objects.get(url=self.kwargs['url']).id)

        if len(context['reviews']) != 0:
            context['reviewsAreExists'] = True

        try:
            goldenStars = RatingFilm.objects.get(filmId__url=self.kwargs['url'], userId=self.request.user).stars.value
        except:
            goldenStars = 0


        try:
            if RatingFilm.objects.filter(filmId__url=self.kwargs['url'], userId=self.request.user).exists():
                context['goldenStars'] = RatingStar.objects.all()[0:goldenStars]
                context['emptyStars'] = RatingStar.objects.all()[goldenStars:5]
            else:
                context['emptyStars'] = RatingStar.objects.all()
        except Exception as e:
                context['emptyStars'] = RatingStar.objects.all()

        context['filmCollection'] = Film.objects.filter(filmCollection=Film.objects.get(url=self.kwargs['url']).filmCollection)
        context['reviewForm'] = ReviewForm()

        return context

class CinemaByGenreView(ListView):
    template_name = 'Cinema/by_genre.html'
    context_object_name = 'filmsByGenre'

    def get_queryset(self):
        obj = Genre.objects.get(url=self.kwargs['url'])
        return Film.objects.filter(genres=obj)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['current_genre'] = Genre.objects.get(url=self.kwargs['url'])

        return context
