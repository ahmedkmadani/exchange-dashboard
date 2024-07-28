from rest_framework import serializers
from .models import WalletTransaction


class WalletTransactionSerializer(serializers.ModelSerializer):
    wallet_name = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    formatted_amount = serializers.SerializerMethodField()

    class Meta:
        model = WalletTransaction
        fields = "__all__"

    def get_wallet_name(self, obj):
        return obj.wallet.name

    def get_user_name(self, obj):
        return obj.user.first_name

    def get_formatted_amount(self, obj):
        currency_symbol = obj.wallet.currency.symbol if obj.wallet and obj.wallet.currency else ''
        return f'{obj.amount} {currency_symbol}'

