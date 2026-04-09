from rest_framework import serializers
from .models import Empresa, Setor, Equipamento, OrdemServico
from django.utils import timezone


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ['id', 'nome', 'created_at', 'updated_at']


class SetorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setor
        fields = ['id', 'nome', 'empresa', 'created_at', 'updated_at']


class EquipamentoSerializer(serializers.ModelSerializer):
    nivel_risco = serializers.SerializerMethodField()

    class Meta:
        model = Equipamento
        fields = ['id', 'tag', 'nome', 'status', 'setor', 'nivel_risco', 'created_at', 'updated_at']

    def get_nivel_risco(self, obj):
        return obj.nivel_risco


class OrdemServicoCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdemServico
        fields = ['id', 'titulo', 'status', 'equipamento', 'data_abertura', 'data_conclusao']
        read_only_fields = ['data_abertura', 'data_conclusao']

    def validate_equipamento(self, value):
        if not value:
            raise serializers.ValidationError("Equipamento é obrigatório")
        return value

    def validate(self, data):
        if self.instance:
            old_status = self.instance.status
            new_status = data.get('status', old_status)
            
            fluxo_valido = {
                'Aberta': ['Em andamento', 'Concluída'],
                'Em andamento': ['Concluída', 'Aberta'],
                'Concluída': [],
            }
            
            if new_status not in fluxo_valido.get(old_status, []):
                raise serializers.ValidationError(
                    f"Transição de '{old_status}' para '{new_status}' não é permitida"
                )
            
            if new_status == 'Concluída' and old_status != 'Concluída':
                data['data_conclusao'] = timezone.now()
        
        return data


class OrdemServicoSerializer(serializers.ModelSerializer):
    equipamento_tag = serializers.CharField(source='equipamento.tag', read_only=True)
    equipamento_nome = serializers.CharField(source='equipamento.nome', read_only=True)

    class Meta:
        model = OrdemServico
        fields = ['id', 'titulo', 'status', 'equipamento', 'equipamento_tag', 'equipamento_nome', 
                  'data_abertura', 'data_conclusao', 'created_at', 'updated_at']
        read_only_fields = ['data_abertura', 'data_conclusao', 'created_at', 'updated_at']
