from django.urls import path
from . import views
                    
urlpatterns = [
    path('', views.index),
    path('new_user', views.addUser),
    path('old_user', views.checkOldUser),
    path('books', views.successful),
    path('clear', views.clear),
    path('book/add', views.addBookPage),
    path('book/create_book', views.addBook),
    path('book/create_review/<int:val>', views.addReview),
    path('book/create_review/<int:val>', views.addReview),
    path('book/<int:val>', views.showBook),
    path('user/<int:val>', views.showUser),
    path('book/delete/<int:val>', views.deleteReview),
]