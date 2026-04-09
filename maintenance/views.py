from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Empresa, Setor, Equipamento, OrdemServico
from .serializers import (
    EmpresaSerializer,
    SetorSerializer,
    EquipamentoSerializer,
    OrdemServicoSerializer,
    OrdemServicoCreateUpdateSerializer,
)


class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


class SetorViewSet(viewsets.ModelViewSet):
    queryset = Setor.objects.all()
    serializer_class = SetorSerializer

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


class EquipamentoViewSet(viewsets.ModelViewSet):
    queryset = Equipamento.objects.all()
    serializer_class = EquipamentoSerializer

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

    @action(detail=False, methods=['get'])
    def por_setor(self, request):
        setor_id = request.query_params.get('setor_id')
        if not setor_id:
            return Response(
                {'erro': 'setor_id é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        equipamentos = Equipamento.objects.filter(setor_id=setor_id)
        serializer = self.get_serializer(equipamentos, many=True)
        return Response(serializer.data)


class OrdemServicoViewSet(viewsets.ModelViewSet):
    queryset = OrdemServico.objects.all()
    serializer_class = OrdemServicoSerializer

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return OrdemServicoCreateUpdateSerializer
        return OrdemServicoSerializer

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

    @action(detail=False, methods=['get'])
    def por_equipamento(self, request):
        equipamento_id = request.query_params.get('equipamento_id')
        if not equipamento_id:
            return Response(
                {'erro': 'equipamento_id é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        ordens = OrdemServico.objects.filter(equipamento_id=equipamento_id)
        serializer = self.get_serializer(ordens, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def abertas(self, request):
        ordens = OrdemServico.objects.filter(status__in=['Aberta', 'Em andamento'])
        serializer = self.get_serializer(ordens, many=True)
        return Response(serializer.data)
