from django.contrib import admin
from .models import Empresa, Setor, Equipamento, OrdemServico

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'created_at')
    search_fields = ('nome',)

@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'empresa', 'created_at')
    list_filter = ('empresa',)
    search_fields = ('nome',)

@admin.register(Equipamento)
class EquipamentoAdmin(admin.ModelAdmin):
    list_display = ('tag', 'nome', 'status', 'setor', 'nivel_risco')
    list_filter = ('status', 'setor')
    search_fields = ('tag', 'nome')

@admin.register(OrdemServico)
class OrdemServicoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'status', 'equipamento', 'data_abertura', 'data_conclusao')
    list_filter = ('status', 'data_abertura')
    search_fields = ('titulo', 'equipamento__tag')
    readonly_fields = ('data_abertura', 'data_conclusao', 'created_at', 'updated_at')
