import pytest

from django.core.exceptions import ValidationError

from benovate_test_project.users import models
from benovate_test_project.users.tests.factories import UserFactory


class TestUser:
    pytestmark = pytest.mark.django_db

    def test_first_balance(self):
        user_1 = UserFactory()
        user_2 = UserFactory()
        user_3 = UserFactory()

        assert user_1.balance == 0

    def test_loan_without_creditor(self):
        user_1 = UserFactory()

        models.Loan.objects.create_with_transactions(sum=100, borrower_ids=[user_1.id])

        assert user_1.balance == 100

    def test_loan_with_same_creditor_and_borrower(self):
        user_1 = UserFactory()

        models.Loan.objects.create_with_transactions(sum=100, borrower_ids=[user_1.id])

        with pytest.raises(ValidationError) as excinfo:
            models.Loan.objects.create_with_transactions(creditor=user_1, sum=10, borrower_ids=[user_1.id])

        assert 'сам у себя!' in str(excinfo.value)

    def test_loan_sum_above_limit(self):
        user_1 = UserFactory()
        user_2 = UserFactory()

        with pytest.raises(ValidationError) as excinfo:
            models.Loan.objects.create_with_transactions(creditor=user_1, sum=100, borrower_ids=[user_2.id])

        assert 'превышать сумму' in str(excinfo.value)

    def test_loan_by_inns(self):
        user_1 = UserFactory()

        models.Loan.objects.create_with_transactions_by_inns(sum=100, inns=[user_1.inn])

        assert user_1.balance == 100












