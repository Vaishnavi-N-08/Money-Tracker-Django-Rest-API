from django.urls import path
from .import views
from .views import RegisterView,LoginView,UserView,LogoutView
urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('get_users/', views.Get_UsersView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('add_transaction/', views.Add_TransactionView.as_view()),
    path('delete_transaction/<int:id>/',views.Delete_TransactionView.as_view()),
    path('update_transaction/<int:id>/',views.Update_TransactionView.as_view()),
    path('get_transactions/',views.Get_TransactionsView.as_view()),
    path('get_traninfo/',views.Get_TransactionInfoView.as_view()),
]