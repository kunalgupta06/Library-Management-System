   <template>
    <nav class="navbar">
      <div class="container">
        <router-link to="/" class="logo">OneClickLibrary</router-link>
        <ul class="nav-links">
          <li><router-link to="/">Home</router-link></li>
          <li><router-link to="/LibBook">Books</router-link></li>
          <li><router-link to="/members">Members</router-link></li>
          
          <li v-if="user && user.role === 'admin'">
            <router-link to="/adminPage">Admin Dashboard</router-link>
            <router-link to="/BookRequest">Book Request</router-link>
          </li>
        </ul>
        <div class="buttons">
          <span v-if="user">
            Welcome, {{ user.username }}
            
            <button @click="logout" class="button">Logout</button>
          </span>
          <router-link v-show="!user" to="/loginPage" class="button">Login</router-link>
          <router-link v-show="!user" to="/registerPage" class="button">Register</router-link>
        </div>
        <div class="hamburger" @click="toggleMenu">
          <div class="line" :class="{ 'open': isOpen }"></div>
          <div class="line" :class="{ 'open': isOpen }"></div>
          <div class="line" :class="{ 'open': isOpen }"></div>
        </div>
      </div>
      <div class="mobile-menu" :class="{ 'open': isOpen }">
        <router-link to="/" @click="toggleMenu">Home</router-link>
        <router-link to="/LibBook" @click="toggleMenu">Books</router-link>
        <router-link to="/members" @click="toggleMenu">Members</router-link>
        <router-link to="/settings" @click="toggleMenu">Settings</router-link>
        <router-link v-show="!user" to="/loginPage" @click="toggleMenu">Login</router-link>
        <router-link v-show="!user" to="/registerPage" @click="toggleMenu">Register</router-link>
      </div>
    </nav>
  </template>
  
  <script>
  export default {
    name: 'NavBar',
    data() {
      return {
        user: null,
        isOpen: false
      };
    },
    mounted() {
      this.checkUser();
      this.$router.afterEach(() => {
        // Refresh user data after route changes
        this.checkUser();
      });
    },
    methods: {
      checkUser() {
        const storedUser = localStorage.getItem('user');
        if (storedUser) {
          try {
            this.user = JSON.parse(storedUser);
          } catch (e) {
            console.error('Error parsing user from localStorage:', e);
          }
        } else {
          this.user = null;
        }
      },
      logout() {
        localStorage.removeItem('user');
        this.user = null;
        this.$router.push('/loginPage');
      },
      toggleMenu() {
        this.isOpen = !this.isOpen;
      }
    }
  };
  </script>
  
  <style scoped>
  .navbar {
    background: #0a5550;
    color: white;
    padding: 1rem 2rem;
    position: fixed;
    width: 100%;
    top: 0;
    left: 0;
    z-index: 1000;
  }
  
  .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .logo {
    font-size: 1.5rem;
    font-weight: bold;
    text-decoration: none;
    color: white;
  }
  
  .nav-links {
    display: flex;
    list-style: none;
    gap: 1.5rem;
    margin-left: 1rem; /* Adjust as needed */
  }
  
  .nav-links li a {
    text-decoration: none;
    color: white;
    font-weight: 500;
  }
  
  .nav-links li a:hover {
    color: #2ecc71;
  }
  
  .buttons {
    display: flex;
    gap: 1rem;
    margin-right: 3rem;
  }
  
  .button {
    text-decoration: none;
    color: white;
    padding: 0.5rem 1rem;
    background-color: transparent;
    border: 1px solid white;
    border-radius: 5px;
    transition: background-color 0.3s ease;
  }
  
  .button:hover {
    background-color: rgba(255, 255, 255, 0.1);
  }
  
  .hamburger {
    display: none;
    flex-direction: column;
    cursor: pointer;
    gap: 0.3rem;
  }
  
  .hamburger .line {
    width: 25px;
    height: 3px;
    background: white;
    transition: all 0.3s ease;
  }
  
  .hamburger.open .line:nth-child(1) {
    transform: translateY(8px) rotate(45deg);
  }
  
  .hamburger.open .line:nth-child(2) {
    opacity: 0;
  }
  
  .hamburger.open .line:nth-child(3) {
    transform: translateY(-8px) rotate(-45deg);
  }
  
  .mobile-menu {
    display: none;
    flex-direction: column;
    background: #3498db;
    position: absolute;
    top: 60px;
    width: 100%;
    left: 0;
    text-align: center;
  }
  
  .mobile-menu a {
    padding: 1rem;
    text-decoration: none;
    color: white;
    font-weight: 500;
    border-bottom: 1px solid white;
  }
  
  .mobile-menu a:hover {
    background: #2ecc71;
  }
  
  .mobile-menu.open {
    display: flex;
  }
  </style>
  