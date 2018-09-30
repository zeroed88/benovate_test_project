from rest_framework import serializers

from benovate_test_project.users import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'inn', 'balance', 'username')


class LoanSerializer(serializers.ModelSerializer):
    inns = serializers.ListField(
        child=serializers.CharField(max_length=12, min_length=12)
    )

    borrower_ids = serializers.ListField(
        required=False,
        child=serializers.IntegerField(),
    )

    def validate(self, data):
        creditor = data.get('creditor')
        sum = data.get('sum')

        instance = models.Loan(creditor=creditor, sum=sum)

        if instance.creditor.inn in data.get('inns'):
            raise serializers.ValidationError('Кредитор не может быть заемщиком одновременно!')
        return data

    def create(self, validated_data):
        inns = validated_data.pop('inns')
        instance = models.Loan.objects.create_with_transactions_by_inns(inns=inns, **validated_data)
        return instance

    class Meta:
        model = models.Loan
        fields = ('id', 'creditor', 'sum', 'inns', 'borrower_ids')


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = ('id', 'loan', 'sum', 'borrower')
