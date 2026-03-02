from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name="books.index"),
    path('list_books/', views.list_books, name="books.list_books"),
    path('aboutus/', views.aboutus, name="books.aboutus"),
    path('<int:bookId>/', views.viewbook, name="books.view_one_book"),

    path('index2/<int:val1>/', views.index2),
    path('index2/<str:val1>/', views.index2_text),
    path('lab3/<int:bookId>/', views.viewbook_lab3),
    path('lab3_index/', views.index_lab3),
]