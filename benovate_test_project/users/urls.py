from django.urls import include, path

from rest_framework import routers

from benovate_test_project.users import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, 'Users')
router.register(r'transactions', views.TransactionViewSet, 'Transactions')
router.register(r'loans', views.LoanViewSet, 'Loans')

app_name = "users"
urlpatterns = [
    path('', include(router.urls))
]
