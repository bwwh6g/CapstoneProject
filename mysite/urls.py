
from django.contrib import admin
from django.urls import path
from bookrecommender import indexpage,rating,recommand

urlpatterns = [
    # path('',indexpage.csv2db),
    path('',indexpage.index),
    path('login',indexpage.login),
    path('getid',indexpage.getid),
    path('getRatingPage',rating.getRatingPage),
    path('rating',rating.getRatingBooks),
    path('saveRating',rating.saveRating),
    path('getRecom',recommand.recomBook),
    path('logout',rating.logout),
]