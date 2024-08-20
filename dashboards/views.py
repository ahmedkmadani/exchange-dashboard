from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.views import APIView

from web_project import TemplateLayout, TemplateHelper
from dashboards.forms.wallet_form import WalletForm, WalletTransactionForm
from .models import Wallet, Transaction, transfer_money
from .wallet_transaction_serializer import TransactionSerializer

"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to dashboards/urls.py file for more pages.
"""


class DashboardsView(LoginRequiredMixin, TemplateView):
    login_url = 'auth-login'
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        wallet_transactions_form = WalletTransactionForm()
        form = WalletForm()
        context['form'] = form
        context["wallet_transactions_form"] = wallet_transactions_form

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        wallets = Wallet.objects.all()

        context.update({"wallets": wallets})

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        wallet_transactions_form = WalletTransactionForm(request.POST)
        if wallet_transactions_form.is_valid():
            from_wallet = wallet_transactions_form.cleaned_data['from_wallet']
            to_wallet = wallet_transactions_form.cleaned_data['to_wallet']
            amount = wallet_transactions_form.cleaned_data['amount']
            exchange_rate = wallet_transactions_form.cleaned_data['rate']

            if from_wallet == to_wallet:
                messages.error(request, "Source and destination wallets cannot be the same.")
            elif from_wallet.currency != to_wallet.currency and not exchange_rate:
                messages.error(request, "Exchange rate is required for transfers between different currencies.")
            else:
                try:
                    transaction = transfer_money(from_wallet, to_wallet, amount, exchange_rate, user=request.user)
                    messages.success(request, f"Successfully transferred {amount} from {from_wallet} to {to_wallet}.")
                    return redirect('index')
                except Exception as e:
                    messages.error(request, f"Error creating transaction: {e}")

        else:
            wallet_transactions_form = WalletTransactionForm()
            return self.render_to_response(self.get_context_data(form=wallet_transactions_form))


class WalletDashboardsView(LoginRequiredMixin, TemplateView):
    login_url = 'auth-login'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        form = WalletForm()
        wallet_transactions_form = WalletTransactionForm()
        context["form"] = form
        context["wallet_transactions_form"] = wallet_transactions_form

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        wallets = Wallet.objects.all()

        context.update({"wallets": wallets})

        return render(request, self.template_name, context)


# class WalletTransactionView(LoginRequiredMixin, TemplateView):
#     login_url = 'auth-login'
#
#     def get_context_data(self, **kwargs):
#         """Initialize view context with a LoginForm and layout."""
#         context = TemplateLayout.init(self, super().get_context_data(**kwargs))
#         context.update(
#             {"layout_path": TemplateHelper.set_layout("layout_blank.html", context)}
#         )
#
#         return context
#
#     def post(self, request, *args, **kwargs):
#         wallet_transactions_form = WalletTransactionForm(request.POST)
#         if wallet_transactions_form.is_valid():
#             from_wallet = wallet_transactions_form.cleaned_data['from_wallet']
#             to_wallet = wallet_transactions_form.cleaned_data['to_wallet']
#             amount = wallet_transactions_form.cleaned_data['amount']
#             exchange_rate = wallet_transactions_form.cleaned_data['rate']
#
#             if from_wallet == to_wallet:
#                 messages.error(request, "Source and destination wallets cannot be the same.")
#             elif from_wallet.currency != to_wallet.currency and not exchange_rate:
#                 messages.error(request, "Exchange rate is required for transfers between different currencies.")
#             else:
#                 try:
#                     transaction = transfer_money(from_wallet, to_wallet, amount, exchange_rate, user=request.user)
#                     messages.success(request, f"Successfully transferred {amount} from {from_wallet} to {to_wallet}.")
#                     return redirect('index')
#                 except Exception as e:
#                     messages.error(request, f"Error creating transaction: {e}")
#
#         else:
#             wallet_transactions_form = WalletTransactionForm()
#             return self.render_to_response(self.get_context_data(form=wallet_transactions_form))


class AddWalletView(LoginRequiredMixin, TemplateView):
    login_url = 'auth-login'
    def get_context_data(self, **kwargs):
        """Initialize view context with a LoginForm and layout."""
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context.update(
            {"layout_path": TemplateHelper.set_layout("layout_blank.html", context)}
        )

        return context

    def post(self, request, *args, **kwargs):
        try:
            user = get_object_or_404(User, pk=request.user.id)
        except User.DoesNotExist:
            return redirect('auth-login')
        form = WalletForm(request.POST)
        if form.is_valid():
            wallet = form.save(commit=False)
            wallet.user = request.user
            wallet.save()
            return redirect('wallets')
        return self.render_to_response(self.get_context_data(form=form))


class WalletTransactionsAPIView(LoginRequiredMixin, APIView):
    login_url = 'auth-login'
    def get(self, request, *args, **kwargs):
        transaction = Transaction.objects.all()
        serializer = TransactionSerializer(transaction, many=True)
        return Response({"data": serializer.data})
