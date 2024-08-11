from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    sender_wallet_name = serializers.SerializerMethodField()
    recipient_wallet_name = serializers.SerializerMethodField()
    amount_with_symbol = serializers.SerializerMethodField()
    user_full_name = serializers.SerializerMethodField()
    exchange_rate_rounded = serializers.SerializerMethodField()
    recipient_amount_with_symbol = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Transaction
        fields = '__all__'

    def get_sender_wallet_name(self, obj):
        return obj.sender_wallet.name if obj.sender_wallet else None

    def get_recipient_wallet_name(self, obj):
        return obj.recipient_wallet.name

    def get_amount_with_symbol(self, obj):
        currency_symbol = obj.sender_wallet.currency.symbol
        return f"{currency_symbol}{obj.amount:.2f}"

    def get_user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def get_recipient_amount_with_symbol(self, obj):
        if obj.exchange_rate and obj.recipient_wallet:
            recipient_currency_symbol = obj.recipient_wallet.currency.symbol
            recipient_amount = obj.amount * obj.exchange_rate
            return f"{recipient_currency_symbol}{recipient_amount:.2f}"
        return None

    def get_exchange_rate_rounded(self, obj):
        exchange_rate = obj.exchange_rate  # assuming the exchange rate is a field in the Transaction model
        rounded_rate = round(exchange_rate, 5)
        return rounded_rate