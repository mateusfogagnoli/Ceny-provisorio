from django.db import models
from django.core.exceptions import ValidationError

class Empresa(models.Model):
    nome = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Empresas"

    def __str__(self):
        return self.nome


class Setor(models.Model):
    nome = models.CharField(max_length=255)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='setores')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('nome', 'empresa')
        verbose_name_plural = "Setores"

    def __str__(self):
        return f"{self.nome} - {self.empresa.nome}"


class Equipamento(models.Model):
    STATUS_CHOICES = [
        ('operacional', 'Operacional'),
        ('manutencao', 'Em Manutenção'),
        ('parado', 'Parado'),
    ]

    tag = models.CharField(max_length=255, unique=True)
    nome = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='operacional')
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE, related_name='equipamentos')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Equipamentos"

    def __str__(self):
        return f"{self.tag} - {self.nome}"

    @property
    def nivel_risco(self):
        os_abertas = self.ordens_servico.filter(status__in=['Aberta', 'Em andamento']).count()
        if os_abertas == 0:
            return 'verde'
        elif os_abertas <= 2:
            return 'amarelo'
        else:
            return 'vermelho'


class OrdemServico(models.Model):
    STATUS_CHOICES = [
        ('Aberta', 'Aberta'),
        ('Em andamento', 'Em andamento'),
        ('Concluída', 'Concluída'),
    ]

    titulo = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Aberta')
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE, related_name='ordens_servico')
    data_abertura = models.DateTimeField(auto_now_add=True)
    data_conclusao = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ordem de Serviço"
        verbose_name_plural = "Ordens de Serviço"
        ordering = ['-data_abertura']

    def __str__(self):
        return f"{self.titulo} - {self.equipamento.tag}"

    def clean(self):
        if self.pk:
            old_status = OrdemServico.objects.get(pk=self.pk).status
            fluxo_valido = {
                'Aberta': ['Em andamento', 'Concluída'],
                'Em andamento': ['Concluída', 'Aberta'],
                'Concluída': [],
            }
            if self.status not in fluxo_valido.get(old_status, []):
                raise ValidationError(f"Transição de {old_status} para {self.status} não é permitida")
