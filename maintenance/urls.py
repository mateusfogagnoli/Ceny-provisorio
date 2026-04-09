from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmpresaViewSet,
    SetorViewSet,
    EquipamentoViewSet,
    OrdemServicoViewSet,
)

router = DefaultRouter()
router.register(r'empresas', EmpresaViewSet)
router.register(r'setores', SetorViewSet)
router.register(r'equipamentos', EquipamentoViewSet)
router.register(r'ordens-servico', OrdemServicoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
