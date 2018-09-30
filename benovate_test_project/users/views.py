from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.urls import reverse

from rest_framework import viewsets

from benovate_test_project.users.models import Loan, Transaction
from benovate_test_project.users.serializers import UserSerializer, TransactionSerializer, LoanSerializer

User = get_user_model()

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    ordering_fields = ('id', 'inn')


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()


class LoanViewSet(viewsets.ModelViewSet):
    serializer_class = LoanSerializer
    queryset = Loan.objects.exclude(creditor__isnull=True)

