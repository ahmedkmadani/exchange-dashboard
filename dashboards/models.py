from django.db import models
from django.contrib.auth.models import User
from django.db import transaction


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=5, null=True, blank=True)
    flag_code = models.CharField(max_length=2, blank=True, null=True)  # Add this line

    def __str__(self):
        return f"{self.name} ({self.code}) {self.symbol}"


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=19, decimal_places=1, default=0.00)  # Increased precision
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.currency.code})"


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'),
    )

    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sender_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='sent_transactions', null=True,
                                      blank=True)
    recipient_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='received_transactions')
    amount = models.DecimalField(max_digits=19, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add=True)
    exchange_rate = models.DecimalField(max_digits=19, decimal_places=4, null=True, blank=True)

    def __str__(self):
        return (f"{self.get_transaction_type_display()} of {self.amount} from {self.sender_wallet} to "
                f"{self.recipient_wallet} by {self.user}")


def add_money_to_wallet(wallet, amount):
    """
    Adds money to a wallet.

    Args:
        wallet: The Wallet instance.
        amount: The amount to add.
    """

    with transaction.atomic():
        transaction_process = Transaction.objects.create(
            sender_wallet=None,
            recipient_wallet=wallet,
            amount=amount,
            transaction_type='deposit'
        )
        wallet.balance += amount
        wallet.save()
        return transaction_process


def transfer_money(sender_wallet, recipient_wallet, amount, exchange_rate, user):
    """
    Transfers money between wallets with a custom exchange rate.

    Args:
        sender_wallet: The sender's wallet.
        recipient_wallet: The recipient's wallet.
        amount: The amount to transfer in the sender's wallet currency.
        exchange_rate: The exchange rate from sender's currency to recipient's currency (optional).
    """

    if not exchange_rate and sender_wallet.currency != recipient_wallet.currency:
        raise ValueError("Exchange rate required for transfers between different currencies.")

    with transaction.atomic():
        converted_amount = amount * exchange_rate if exchange_rate else amount
        sender_wallet.balance -= amount
        sender_wallet.save()

        recipient_wallet.balance += converted_amount
        recipient_wallet.save()

        transaction_process = Transaction.objects.create(
            sender_wallet=sender_wallet,
            recipient_wallet=recipient_wallet,
            amount=amount,
            exchange_rate=exchange_rate,
            transaction_type='transfer',
            user=user
        )

        return transaction_process
