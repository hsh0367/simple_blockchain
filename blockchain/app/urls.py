from django.urls import include, path
from app.views import (
    TransactionsNewView,
    MineView,
    FullChainView,
    NodeRegisterView,
    # NodeResolveView,
)

urlpatterns = [
    path("transactions/new", TransactionsNewView.as_view(), name="transactions_new"),
    path("mine", MineView.as_view(), name="mine"),
    path("chain", FullChainView.as_view(), name="full_chain"),
    path("nodes/register", NodeRegisterView.as_view(), name="nodes_register"),
    # path("nodes/resolve", NodeResolveView.as_view(), name="nodes_resolve"),
]
