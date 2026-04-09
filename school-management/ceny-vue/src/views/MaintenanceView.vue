<template>
  <div class="maintenance-container">
    <h1>Sistema CENY - Gestão de Manutenção</h1>

    <!-- Navegação por abas -->
    <div class="tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        @click="activeTab = tab.id"
        :class="{ active: activeTab === tab.id }"
        class="tab-button"
      >
        {{ tab.label }}
      </button>
    </div>

    <!-- ABA: Empresas -->
    <section v-show="activeTab === 'empresas'" class="tab-content">
      <h2>Empresas</h2>
      <div class="form-group">
        <input 
          v-model="novaEmpresa" 
          placeholder="Nome da empresa"
          @keyup.enter="criarEmpresa"
        />
        <button @click="criarEmpresa">Adicionar Empresa</button>
      </div>
      <ul class="list">
        <li v-for="empresa in empresas" :key="empresa.id">
          {{ empresa.nome }}
        </li>
      </ul>
    </section>

    <!-- ABA: Setores -->
    <section v-show="activeTab === 'setores'" class="tab-content">
      <h2>Setores</h2>
      <div class="form-group">
        <select v-model="novoSetor.empresa_id">
          <option value="">Selecione uma empresa</option>
          <option v-for="empresa in empresas" :key="empresa.id" :value="empresa.id">
            {{ empresa.nome }}
          </option>
        </select>
        <input 
          v-model="novoSetor.nome" 
          placeholder="Nome do setor"
          @keyup.enter="criarSetor"
        />
        <button @click="criarSetor">Adicionar Setor</button>
      </div>
      <ul class="list">
        <li v-for="setor in setores" :key="setor.id">
          {{ setor.nome }} - {{ getEmpresaNome(setor.empresa) }}
        </li>
      </ul>
    </section>

    <!-- ABA: Equipamentos -->
    <section v-show="activeTab === 'equipamentos'" class="tab-content">
      <h2>Equipamentos</h2>
      <div class="form-group">
        <input 
          v-model="novoEquipamento.tag" 
          placeholder="TAG (ex: EQ-001)"
          @keyup.enter="criarEquipamento"
        />
        <input 
          v-model="novoEquipamento.nome" 
          placeholder="Nome do equipamento"
          @keyup.enter="criarEquipamento"
        />
        <select v-model="novoEquipamento.setor_id">
          <option value="">Selecione um setor</option>
          <option v-for="setor in setores" :key="setor.id" :value="setor.id">
            {{ setor.nome }}
          </option>
        </select>
        <button @click="criarEquipamento">Adicionar Equipamento</button>
      </div>

      <div class="equipment-grid">
        <div 
          v-for="equipamento in equipamentos" 
          :key="equipamento.id"
          :class="['equipment-card', `risk-${equipamento.nivel_risco}`]"
        >
          <div class="equipment-header">
            <h3>{{ equipamento.tag }}</h3>
            <span class="risk-badge" :class="`risk-${equipamento.nivel_risco}`">
              {{ equipamento.nivel_risco }}
            </span>
          </div>
          <p><strong>Nome:</strong> {{ equipamento.nome }}</p>
          <p><strong>Status:</strong> {{ equipamento.status }}</p>
          <p><strong>Setor:</strong> {{ getSetorNome(equipamento.setor) }}</p>
        </div>
      </div>
    </section>

    <!-- ABA: Ordens de Serviço -->
    <section v-show="activeTab === 'ordens'" class="tab-content">
      <h2>Ordens de Serviço</h2>

      <div class="form-group">
        <input 
          v-model="novaOS.titulo" 
          placeholder="Título da OS"
        />
        <select v-model="novaOS.equipamento_id">
          <option value="">Selecione um equipamento</option>
          <option v-for="equipamento in equipamentos" :key="equipamento.id" :value="equipamento.id">
            {{ equipamento.tag }} - {{ equipamento.nome }}
          </option>
        </select>
        <button @click="criarOS">Criar Ordem de Serviço</button>
      </div>

      <div class="os-list">
        <div 
          v-for="os in ordemServico" 
          :key="os.id"
          :class="['os-card', `status-${os.status.toLowerCase()}`]"
        >
          <div class="os-header">
            <h3>{{ os.titulo }}</h3>
            <span class="status-badge" :class="`status-${os.status.toLowerCase()}`">
              {{ os.status }}
            </span>
          </div>
          <p><strong>Equipamento:</strong> {{ os.equipamento_tag }} - {{ os.equipamento_nome }}</p>
          <p><strong>Abertura:</strong> {{ formatarData(os.data_abertura) }}</p>
          <p v-if="os.data_conclusao"><strong>Conclusão:</strong> {{ formatarData(os.data_conclusao) }}</p>

          <div class="os-actions">
            <button 
              v-if="os.status === 'Aberta'"
              @click="atualizarStatusOS(os.id, 'Em andamento')"
              class="btn-success"
            >
              Iniciar
            </button>
            <button 
              v-if="os.status === 'Em andamento'"
              @click="atualizarStatusOS(os.id, 'Concluída')"
              class="btn-success"
            >
              Concluir
            </button>
            <button 
              v-if="os.status === 'Aberta' || os.status === 'Em andamento'"
              @click="atualizarStatusOS(os.id, 'Aberta')"
              class="btn-warning"
            >
              Reabrir
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Mensagens de erro/sucesso -->
    <div v-if="mensagem" :class="['mensagem', mensagem.tipo]">
      {{ mensagem.texto }}
    </div>
  </div>
</template>

<script>
import api from '../services/api';

export default {
  name: 'MaintenanceView',
  data() {
    return {
      activeTab: 'empresas',
      tabs: [
        { id: 'empresas', label: 'Empresas' },
        { id: 'setores', label: 'Setores' },
        { id: 'equipamentos', label: 'Equipamentos' },
        { id: 'ordens', label: 'Ordens de Serviço' },
      ],
      empresas: [],
      setores: [],
      equipamentos: [],
      ordemServico: [],
      novaEmpresa: '',
      novoSetor: { nome: '', empresa_id: '' },
      novoEquipamento: { tag: '', nome: '', setor_id: '' },
      novaOS: { titulo: '', equipamento_id: '' },
      mensagem: null,
    };
  },
  mounted() {
    this.carregarDados();
  },
  methods: {
    async carregarDados() {
      try {
        const [empresasRes, setoresRes, equipamentosRes, osRes] = await Promise.all([
          api.getEmpresas(),
          api.getSetores(),
          api.getEquipamentos(),
          api.getOrdensServico(),
        ]);

        this.empresas = empresasRes.data;
        this.setores = setoresRes.data;
        this.equipamentos = equipamentosRes.data;
        this.ordemServico = osRes.data;
      } catch (erro) {
        this.mostrarMensagem('Erro ao carregar dados', 'erro');
      }
    },
    async criarEmpresa() {
      if (!this.novaEmpresa.trim()) return;
      try {
        const res = await api.createEmpresa({
          nome: this.novaEmpresa,
        });
        this.empresas.push(res.data);
        this.novaEmpresa = '';
        this.mostrarMensagem('Empresa criada!', 'sucesso');
      } catch (erro) {
        this.mostrarMensagem('Erro ao criar empresa', 'erro');
      }
    },
    async criarSetor() {
      if (!this.novoSetor.nome.trim() || !this.novoSetor.empresa_id) return;
      try {
        const res = await api.createSetor({
          nome: this.novoSetor.nome,
          empresa: this.novoSetor.empresa_id,
        });
        this.setores.push(res.data);
        this.novoSetor = { nome: '', empresa_id: '' };
        this.mostrarMensagem('Setor criado!', 'sucesso');
      } catch (erro) {
        this.mostrarMensagem('Erro ao criar setor', 'erro');
      }
    },
    async criarEquipamento() {
      if (!this.novoEquipamento.tag.trim() || !this.novoEquipamento.nome.trim() || !this.novoEquipamento.setor_id) return;
      try {
        const res = await api.createEquipamento({
          tag: this.novoEquipamento.tag,
          nome: this.novoEquipamento.nome,
          setor: this.novoEquipamento.setor_id,
          status: 'operacional',
        });
        this.equipamentos.push(res.data);
        this.novoEquipamento = { tag: '', nome: '', setor_id: '' };
        this.mostrarMensagem('Equipamento criado!', 'sucesso');
      } catch (erro) {
        this.mostrarMensagem('Erro ao criar equipamento', 'erro');
      }
    },
    async criarOS() {
      if (!this.novaOS.titulo.trim() || !this.novaOS.equipamento_id) return;
      try {
        const res = await api.createOrdemServico({
          titulo: this.novaOS.titulo,
          equipamento: this.novaOS.equipamento_id,
          status: 'Aberta',
        });
        this.ordemServico.push(res.data);
        this.novaOS = { titulo: '', equipamento_id: '' };
        this.mostrarMensagem('Ordem de Serviço criada!', 'sucesso');
      } catch (erro) {
        this.mostrarMensagem('Erro ao criar OS', 'erro');
      }
    },
    async atualizarStatusOS(osId, novoStatus) {
      try {
        const res = await api.updateOrdemServico(osId, {
          status: novoStatus,
        });
        const index = this.ordemServico.findIndex(o => o.id === osId);
        if (index !== -1) {
          this.ordemServico[index] = res.data;
        }
        this.mostrarMensagem('Status atualizado!', 'sucesso');
      } catch (erro) {
        this.mostrarMensagem('Erro ao atualizar status', 'erro');
      }
    },
    getEmpresaNome(empresaId) {
      const empresa = this.empresas.find(e => e.id === empresaId);
      return empresa ? empresa.nome : 'Desconhecida';
    },
    getSetorNome(setorId) {
      const setor = this.setores.find(s => s.id === setorId);
      return setor ? setor.nome : 'Desconhecido';
    },
    formatarData(data) {
      return new Date(data).toLocaleDateString('pt-BR');
    },
    mostrarMensagem(texto, tipo) {
      this.mensagem = { texto, tipo };
      setTimeout(() => {
        this.mensagem = null;
      }, 3000);
    },
  },
};
</script>

<style scoped>
.maintenance-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu;
  background: #F9FAFB;
  min-height: 100vh;
}

h1 {
  text-align: center;
  color: #111827;
  margin-bottom: 30px;
  font-weight: 600;
}

.tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  border-bottom: 2px solid #E5E7EB;
}

.tab-button {
  padding: 10px 20px;
  border: none;
  background: none;
  cursor: pointer;
  color: #6B7280;
  font-weight: 500;
  border-bottom: 3px solid transparent;
  transition: all 0.3s;
}

.tab-button.active {
  color: #3B82F6;
  border-bottom-color: #3B82F6;
}

.tab-content {
  animation: fadeIn 0.2s;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.form-group {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.form-group input,
.form-group select {
  flex: 1;
  min-width: 150px;
  padding: 10px;
  border: 1px solid #E5E7EB;
  border-radius: 4px;
  font-size: 14px;
  background: #FFFFFF;
  color: #111827;
}

.form-group button {
  padding: 10px 20px;
  background: #3B82F6;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s;
}

.form-group button:hover {
  background: #2563EB;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.list {
  list-style: none;
  padding: 0;
}

.list li {
  padding: 10px;
  background: #F9FAFB;
  margin-bottom: 10px;
  border-radius: 4px;
  border-left: 4px solid #3B82F6;
  color: #111827;
  border-top: 1px solid #E5E7EB;
}

.equipment-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 15px;
  margin-top: 20px;
}

.equipment-card {
  padding: 15px;
  border-radius: 8px;
  border-left: 5px solid;
  background: #FFFFFF;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border-top: 1px solid #E5E7EB;
}

.equipment-card.risk-verde {
  border-left-color: #10B981;
  background: #F0FDF4;
}

.equipment-card.risk-amarelo {
  border-left-color: #F59E0B;
  background: #FFFBEB;
}

.equipment-card.risk-vermelho {
  border-left-color: #EF4444;
  background: #FEF2F2;
}

.equipment-card h3 {
  margin: 0 0 10px 0;
  color: #111827;
  font-weight: 600;
}

.equipment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.risk-badge {
  padding: 4px 8px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: bold;
  text-transform: uppercase;
}

.risk-verde { background: #10B981; color: #111827; }
.risk-amarelo { background: #F59E0B; color: #111827; }
.risk-vermelho { background: #EF4444; color: white; }

.os-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 15px;
  margin-top: 20px;
}

.os-card {
  padding: 15px;
  border-radius: 8px;
  border-left: 5px solid;
  background: #FFFFFF;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border-top: 1px solid #E5E7EB;
}

.os-card.status-aberta {
  border-left-color: #F59E0B;
  background: #FFFBEB;
}

.os-card.status-em\ andamento {
  border-left-color: #3B82F6;
  background: #F0F9FF;
}

.os-card.status-concluída {
  border-left-color: #10B981;
  background: #F0FDF4;
}

.os-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.os-header h3 {
  margin: 0;
  color: #111827;
  font-weight: 600;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: bold;
  text-transform: uppercase;
}

.status-aberta { background: #F59E0B; color: #111827; }
.status-em\ andamento { background: #3B82F6; color: white; }
.status-concluída { background: #10B981; color: #111827; }

.os-actions {
  display: flex;
  gap: 5px;
  margin-top: 10px;
  flex-wrap: wrap;
}

.os-actions button {
  padding: 6px 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 500;
  transition: all 0.3s;
}

.btn-success {
  background: #10B981;
  color: white;
}

.btn-success:hover {
  background: #059669;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.btn-warning {
  background: #F59E0B;
  color: #111827;
  transition: all 0.3s;
}

.btn-warning:hover {
  background: #D97706;
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
}

.mensagem {
  position: fixed;
  bottom: 20px;
  right: 20px;
  padding: 15px 20px;
  border-radius: 4px;
  color: white;
  animation: slideIn 0.3s;
  font-weight: 500;
}

.mensagem.sucesso {
  background: #10B981;
}

.mensagem.erro {
  background: #EF4444;
}

@keyframes slideIn {
  from {
    transform: translateX(400px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}
</style>
