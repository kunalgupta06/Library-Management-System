// eventBus.js
import { reactive } from 'vue';

export const eventBus = reactive({
  isAuthenticated: !!localStorage.getItem('user'),
  user: JSON.parse(localStorage.getItem('user')) || null,
  role: localStorage.getItem('role') || null,

  login(user, role) {
    this.isAuthenticated = true;
    this.user = user;
    this.role = role;
    localStorage.setItem('user', JSON.stringify(user));
    localStorage.setItem('role', role);
  },

  logout() {
    this.isAuthenticated = false;
    this.user = null;
    this.role = null;
    localStorage.removeItem('user');
    localStorage.removeItem('role');
  }
});
