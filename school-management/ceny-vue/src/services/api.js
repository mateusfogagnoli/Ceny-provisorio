import axios from 'axios'

const apiClient = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/maintenance',
    headers:{
        'Content-Type':'application/json'
    }
});

export default{

    // ====== EMPRESAS ======
    getEmpresas(){
        return apiClient.get('/empresas/');
    },

    getEmpresa(id){
        return apiClient.get(`/empresas/${id}/`);
    },

    createEmpresa(data){
        return apiClient.post('/empresas/', data);
    },

    updateEmpresa(id, data){
        return apiClient.put(`/empresas/${id}/`, data);
    },

    deleteEmpresa(id){
        return apiClient.delete(`/empresas/${id}/`);
    },

    // ====== SETORES ======
    getSetores(){
        return apiClient.get('/setores/');
    },

    getSetor(id){
        return apiClient.get(`/setores/${id}/`);
    },

    createSetor(data){
        return apiClient.post('/setores/', data);
    },

    updateSetor(id, data){
        return apiClient.put(`/setores/${id}/`, data);
    },

    deleteSetor(id){
        return apiClient.delete(`/setores/${id}/`);
    },

    // ====== EQUIPAMENTOS ======
    getEquipamentos(){
        return apiClient.get('/equipamentos/');
    },

    getEquipamento(id){
        return apiClient.get(`/equipamentos/${id}/`);
    },

    createEquipamento(data){
        return apiClient.post('/equipamentos/', data);
    },

    updateEquipamento(id, data){
        return apiClient.patch(`/equipamentos/${id}/`, data);
    },

    deleteEquipamento(id){
        return apiClient.delete(`/equipamentos/${id}/`);
    },

    getEquipamentosPorSetor(setorId){
        return apiClient.get(`/equipamentos/por_setor/?setor_id=${setorId}`);
    },

    // ====== ORDENS DE SERVIÇO ======
    getOrdensServico(){
        return apiClient.get('/ordens-servico/');
    },

    getOrdemServico(id){
        return apiClient.get(`/ordens-servico/${id}/`);
    },

    createOrdemServico(data){
        return apiClient.post('/ordens-servico/', data);
    },

    updateOrdemServico(id, data){
        return apiClient.patch(`/ordens-servico/${id}/`, data);
    },

    deleteOrdemServico(id){
        return apiClient.delete(`/ordens-servico/${id}/`);
    },

    getOrdensAbertas(){
        return apiClient.get('/ordens-servico/abertas/');
    },

    getOrdensPorEquipamento(equipamentoId){
        return apiClient.get(`/ordens-servico/por_equipamento/?equipamento_id=${equipamentoId}`);
    }

}