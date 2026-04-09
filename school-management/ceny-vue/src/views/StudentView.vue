<template>
  <div class="container">
    <h1>Acadêmico - Gestão de Alunos</h1>

    <div class="card">
      <h3>{{ form.id ? 'Editar Registro' : 'Novo Aluno' }}</h3>
      <div class="form-group">
        <input v-model="form.name" placeholder="Nome completo" />
        <input v-model="form.date_of_birth" type="date" />
        <button @click="save" :disabled="!form.name">Gravar</button>
        <button v-if="form.id" @click="reset">Cancelar</button>
      </div>
    </div>

    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Nome</th>
          <th>Nascimento</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="s in students" :key="s.id">
          <td>#{{ s.id }}</td>
          <td>{{ s.name }}</td>
          <td>{{ formatDate(s.date_of_birth) }}</td>
          <td>
            <button @click="edit(s)">✏️</button>
            <button @click="remove(s.id)" class="btn-del">🗑️</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../services/api';

const students = ref([]);
const form = ref({ id: null, name: '', date_of_birth: '' });

const load = async () => {
  try {
    const res = await api.getStudents();
    // Ajuste para Django (com ou sem paginação)
    students.value = res.data.results ? res.data.results : res.data;
  } catch (err) {
    console.error("Erro na API Django:", err);
  }
};

const save = async () => {
  try {
    if (form.value.id) {
      await api.updateStudent(form.value.id, form.value);
    } else {
      await api.createStudent(form.value);
    }
    reset();
    load();
  } catch (err) {
    alert("Erro ao processar requisição.");
  }
};

const edit = (row) => {
  form.value = { ...row };
};

const remove = async (id) => {
  if (confirm("Excluir aluno?")) {
    await api.deleteStudent(id);
    load();
  }
};

const reset = () => {
  form.value = { id: null, name: '', date_of_birth: '' };
};

// Formatação de data para o padrão BR
const formatDate = (dateStr) => {
  if (!dateStr) return '';
  const [year, month, day] = dateStr.split('-');
  return `${day}/${month}/${year}`;
};

onMounted(load);
</script>

<style scoped>
/* Um pouco de estilo para o Laboratório */
.container { max-width: 800px; margin: 0 auto; font-family: sans-serif; }
.card { background: #f4f4f4; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
.form-group { display: flex; gap: 10px; }
table { width: 100%; border-collapse: collapse; }
th, td { border-bottom: 1px solid #ddd; padding: 12px; text-align: left; }
.btn-del { background: #ff4d4d; color: white; border: none; padding: 5px 10px; cursor: pointer; }
button { cursor: pointer; }
</style>