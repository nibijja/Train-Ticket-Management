from django.urls import path
from .import views

urlpatterns = [
    path('', views.home),

    path('about', views.about),

    path('contact', views.contact),

    path('register', views.register),
    path('activation', views.activation),

    path('logout', views.logout),

    path('login', views.login),

    path('profile', views.profiling),

    path('recover', views.recover),
    path('recover_final', views.recover_final),
    
    path('maintain', views.maintain),
    
    path('stations', views.stations),
    path('station_view', views.station_view),

    path('trains', views.trains),
    path('train_view', views.train_view),
    
    path('delete/<int:train_id>', views.delete),

    path('edit/<int:train_id>', views.edit),
    path('edit/update', views.update),

    
    path('search', views.search),
    path('selection', views.selection),

    path('confirm', views.confirm),

    path('verification', views.verification),
    path('verify', views.verify),

    path('tickets', views.tickets),

    path('reset', views.reset),
]