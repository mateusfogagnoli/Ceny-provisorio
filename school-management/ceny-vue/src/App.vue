<template>
  <nav class="navbar">
    <div class="navbar-brand">
      <router-link to="/" class="brand-link">
        CENY
      </router-link>
    </div>
    <div class="navbar-menu">
      <router-link to="/" class="nav-link">Início</router-link>
      <router-link to="/maintenance" class="nav-link">Sistema de Manutenção</router-link>
    </div>
  </nav>

  <RouterView />
</template>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 30px;
  background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
  border-bottom: 3px solid #2563EB;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.navbar-brand {
  flex: 1;
}

.brand-link {
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: transform 0.3s ease;
}

.brand-link:hover {
  transform: scale(1.05);
}

.navbar-menu {
  display: flex;
  gap: 20px;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-weight: 500;
  font-size: 1rem;
  transition: all 0.3s ease;
  padding: 8px 15px;
  border-radius: 4px;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.nav-link.router-link-active {
  background: rgba(255, 255, 255, 0.3);
  text-decoration: underline;
}

@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    gap: 15px;
  }

  .navbar-menu {
    width: 100%;
    justify-content: center;
  }
}
</style>
