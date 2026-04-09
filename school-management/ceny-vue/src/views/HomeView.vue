<template>
  <div class="home-container">
    <header>
      <h1>CENY</h1>
      <p>Sistema de Gestão de Manutenção Industrial</p>
    </header>

    <main>
      <router-link to="/maintenance" class="btn-start">
        🔧 Acessar Sistema
      </router-link>
    </main>
  </div>
</template>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 80vh;
  text-align: center;
  background: linear-gradient(135deg, #F9FAFB 0%, #F3F4F6 100%);
}

h1 { 
  font-size: 4rem; 
  color: #3B82F6; 
  margin-bottom: 10px;
  font-weight: bold;
}

p { 
  font-size: 1.2rem; 
  color: #374151; 
  margin-bottom: 40px;
  letter-spacing: 0.5px;
}

.btn-start {
  background-color: #3B82F6;
  color: white;
  padding: 18px 40px;
  text-decoration: none;
  border-radius: 12px;
  font-weight: bold;
  font-size: 1.2rem;
  transition: all 0.3s ease;
  display: inline-block;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.btn-start:hover {
  transform: scale(1.08);
  background-color: #2563EB;
  box-shadow: 0 8px 24px rgba(37, 99, 235, 0.4);
}
</style>