from django.contrib import admin
from .models import Film, UserFilmStatus, RatingFilm, Genre, RatingStar, Review, FilmCollection
# Register your models here.
class CreatingSlugAdmin(admin.ModelAdmin):
    prepopulated_fields = {'url': ('title',)}

admin.site.register(Film, CreatingSlugAdmin)
admin.site.register(UserFilmStatus)
admin.site.register(RatingFilm)
admin.site.register(RatingStar)
admin.site.register(Genre, CreatingSlugAdmin)
admin.site.register(Review)
admin.site.register(FilmCollection)
