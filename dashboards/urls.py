from django.urls import path

from .views import DashboardsView, WalletDashboardsView, AddWalletView, WalletTransactionsAPIView, WalletTransactionView

urlpatterns = [
    path(
        "dashboard",
        DashboardsView.as_view(template_name="dashboard.html"),
        name="index",
    ),
    path(
        "dashboard-wallets", WalletDashboardsView.as_view(template_name="dashboard-wallets.html"), name="wallets"
    ),
    path(
        "create-wallets-tranaction", WalletTransactionView.as_view(template_name="dashboard-wallets.html"), name="wallets-transactions"
    ),
    path(
        "create-wallet", AddWalletView.as_view(template_name="dashboard-wallets.html"), name="create_wallet"
    ),
    path("api/v1/wallet-transactions-list", WalletTransactionsAPIView.as_view(), name="wallet-transactions-list")
]
