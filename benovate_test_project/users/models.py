from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import CharField, Sum, Value as V
from django.db.models.functions import Coalesce
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):

    name = CharField(_("Name of User"), blank=True, max_length=255)
    inn = models.CharField("ИНН", max_length=12, db_index=True, blank=True)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    @property
    def balance(self):
        transactions = Transaction.objects.filter(borrower=self).aggregate(total=Coalesce(Sum('sum'), V(0)))
        loans = Loan.objects.filter(creditor=self).aggregate(total=Coalesce(Sum('sum'), V(0)))
        return transactions['total'] - loans['total']


class LoanManager(models.Manager):
    def create_with_transactions(self, **kwargs):
        borrower_ids = kwargs.pop('borrower_ids')
        loan = Loan.objects.create(**kwargs)
        loan.borrowers.set(borrower_ids)
        loan.create_transactions()
        return loan

    def create_with_transactions_by_inns(self, **kwargs):
        inns = kwargs.pop('inns')
        borrower_ids = list(User.objects.filter(inn__in=inns).values_list('pk', flat=True))
        return self.create_with_transactions(borrower_ids=borrower_ids, **kwargs)


class Loan(models.Model):

    creditor = models.ForeignKey(User, verbose_name="Кредитор", on_delete=models.PROTECT, related_name='loans', blank=True, null=True)
    sum = models.DecimalField("Сумма", max_digits=12, decimal_places=2, help_text="в рублях")
    borrowers = models.ManyToManyField(User, verbose_name='Заемщики')

    objects = LoanManager()

    @property
    def inns(self):
        return [dude.inn for dude in self.borrowers.all()]

    @property
    def borrower_ids(self):
        return [dude.pk for dude in self.borrowers.all()]

    def clean(self):
        if self.creditor and self.creditor.balance < self.sum:
            raise ValidationError('Сумма займа для выдачи не может превышать сумму средств на счёте!')

        if self.pk and self.creditor in self.borrowers.all():
            raise ValidationError('Кредитор не может быть заемщиком сам у себя!')

    def __get_sum_per_borrower(self, sum, borrowers):
        return Decimal(sum/len(borrowers)).quantize(Decimal('.01'))

    def create_transactions(self):
        self.clean()
        borrowers = self.borrowers.all()

        if Transaction.objects.filter(loan=self).exists() or not borrowers:
            return

        sum = self.__get_sum_per_borrower(self.sum, borrowers)
        for borrower in borrowers:
            Transaction.objects.create(loan=self, sum=sum, borrower=borrower)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Transaction(models.Model):

    loan = models.ForeignKey(Loan, verbose_name='Заём', on_delete=models.PROTECT, related_name='transactions')
    sum = models.DecimalField("Сумма", max_digits=12, decimal_places=2, help_text="в рублях", validators=[MinValueValidator(0),])
    borrower = models.ForeignKey(User, verbose_name='Заёмщик', on_delete=models.PROTECT, related_name='takes')



