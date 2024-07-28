from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.views import APIView

from web_project import TemplateLayout, TemplateHelper
from dashboards.forms.wallet_form import WalletForm
from .models import Wallet, WalletTransaction
from .wallet_transaction_serializer import WalletTransactionSerializer

"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to dashboards/urls.py file for more pages.
"""


class DashboardsView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        return context


class WalletDashboardsView(TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        form = WalletForm()
        context["form"] = form

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        wallets = Wallet.objects.all()

        context.update({"wallets": wallets})

        return render(request, self.template_name, context)


class AddWalletView(TemplateView):

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
            WalletTransaction.objects.create(wallet=wallet, user=user, transaction_type='credit',
                                             amount=wallet.initial_amount, related_wallet=None)
            return redirect('wallets')
        return self.render_to_response(self.get_context_data(form=form))


class WalletTransactionsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        wallet_transaction = WalletTransaction.objects.all()
        serializer = WalletTransactionSerializer(wallet_transaction, many=True)
        return Response({"data": serializer.data})
