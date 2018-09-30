from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from benovate_test_project.users.forms import UserChangeForm, UserCreationForm
from benovate_test_project.users.models import Loan, Transaction

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("name", "inn")}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "name", "is_superuser", 'balance']
    search_fields = ["name"]


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('id', 'creditor', 'sum')
    list_filter = ('creditor',)
    raw_id_fields = ('borrowers',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'loan', 'sum', 'borrower')
    list_filter = ('loan', 'borrower')
