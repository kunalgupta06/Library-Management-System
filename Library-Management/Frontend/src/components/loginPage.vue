<!-- <template>
    <link
      rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"
    />
    <div class="login">
      <div class="input-container">
        <label for="usernameOrEmail">Username or Email</label>
        <div class="input-box">
          <input
            type="text"
            v-model="usernameOrEmail"
            id="usernameOrEmail"
            placeholder="Enter Your Username or E-Mail"
            class="input-field"
          />
          <i class="fas fa-user"></i>
        </div>
      </div>
      <div class="input-container">
        <label for="password">Password</label>
        <div class="input-box">
          <input
            type="password"
            v-model="password"
            id="password"
            placeholder="Enter Password"
            class="input-field"
          />
          <i class="fas fa-lock"></i>
        </div>
      </div>
      <button @click="login" class="login-button">Login</button>
      <div class="register-link">
        <p>Don't have an account?<a href="/registerPage"> Click Here</a></p>
      </div>
      <div class="toggle-switch">
        <span :class="{'active': role === 'user'}" @click="toggleRole('user')">User</span>
        <span :class="{'active': role === 'admin'}" @click="toggleRole('admin')">Admin</span>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  export default {
    name: 'loginPage',
    data() {
      return {
        usernameOrEmail: '',
        password: '',
        role: 'user',
        error: ''
      };
    },
    methods: {
      async login() {
        try {
          const response = await axios.post('http://127.0.0.1:5000/login', {
            usernameOrEmail: this.usernameOrEmail,
            password: this.password,
            role: this.role  // Send role information
          });
          if (response && response.data && this.role=="user") {
            console.log(response.data);
            this.$router.push('/homePage');}
          if (response && response.data && this.role=="admin") {
            console.log(response.data);
            this.$router.push('/adminPage'); // Redirect to home page on successful login
          } else {
            console.error('Unexpected response structure:', response);
            //'alert('An unexpected error occurred. Please try again later.');
          }}catch (error) {
          if (error.response && error.response.data && error.response.data.message) {
            console.error('Error logging in:', error.response.data.message);
            alert(error.response.data.message);
          } else {
            console.error('An unknown error occurred:', error);
            alert('An unknown error occurred. Please try again later.');
          }
        }
      },
      toggleRole(selectedRole) {
        this.role = selectedRole;
      }
    }
  };
  </script>
  
  <style scoped>
  .login {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    background-color: #ffffff;
    border-radius: 20px;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
    text-align: center;
    margin-top: 150px;
  }
  
  .input-container {
    text-align: left;
    margin-bottom: 15px;
  }
  
  .input-container label {
    display: block;
    margin-bottom: 5px;
    font-size: 16px;
    font-weight: bold;
  }
  
  .input-box {
    position: relative;
    width: 100%;
  }
  
  .input-field {
    width: 100%;
    padding: 10px;
    padding-right: 40px; /* Make room for the icon */
    border: 1px solid #ccc;
    border-radius: 8px;
    box-sizing: border-box;
    font-size: 16px;
  }
  
  .input-box i {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 20px;
    color: #888;
  }
  
  .login-button {
    width: 100%;
    padding: 12px 0;
    border: none;
    border-radius: 8px;
    background-color: hsl(122, 39%, 49%);
    color: white;
    font-size: 18px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .login-button:hover {
    background-color: #45a049;
  }
  
  .register-link {
    position: auto;
  }
  
  .toggle-switch {
    display: flex;
    justify-content: center;
    margin-top: 20px;
  }
  
  .toggle-switch span {
    margin: 0 10px;
    padding: 10px 20px;
    border: 1px solid #45a049;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.3s ease, color 0.3s ease;
  }
  
  .toggle-switch span.active {
    background-color: #4CAF50;
    color: white;
  }
  
  .toggle-switch span:not(.active):hover {
    background-color: #f0f0f0;
  }
  </style>
   -->


   <!-- <template>
    <link
      rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"
    />
    <div class="login">
      <div class="input-container">
        <label for="usernameOrEmail">Username or Email</label>
        <div class="input-box">
          <input
            type="text"
            v-model="usernameOrEmail"
            id="usernameOrEmail"
            placeholder="Enter Your Username or E-Mail"
            class="input-field"
          />
          <i class="fas fa-user"></i>
        </div>
      </div>
      <div class="input-container">
        <label for="password">Password</label>
        <div class="input-box">
          <input
            type="password"
            v-model="password"
            id="password"
            placeholder="Enter Password"
            class="input-field"
          />
          <i class="fas fa-lock"></i>
        </div>
      </div>
      <button @click="login" class="login-button">Login</button>
      <div class="register-link">
        <p>Don't have an account?<a href="/registerPage"> Click Here</a></p>
      </div>
      <div class="toggle-switch">
        <span :class="{'active': role === 'user'}" @click="toggleRole('user')">User</span>
        <span :class="{'active': role === 'admin'}" @click="toggleRole('admin')">Admin</span>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  export default {
    name: 'loginPage',
    data() {
      return {
        usernameOrEmail: '',
        password: '',
        role: 'user',
        error: ''
      };
    },
    methods: {
      async login() {
        try {
          const response = await axios.post('http://127.0.0.1:5000/login', {
            usernameOrEmail: this.usernameOrEmail,
            password: this.password,
            role: this.role
          });
          if (response && response.data) {
            console.log(response.data);
            localStorage.setItem('user', JSON.stringify(response.data.user));
            if (this.role == "user") {
              this.$router.push('/homePage');
            } else if (this.role == "admin") {
              this.$router.push('/adminPage');
            }
          } else {
            console.error('Unexpected response structure:', response);
            alert('An unexpected error occurred. Please try again later.');
          }
        } catch (error) {
          if (error.response && error.response.data && error.response.data.message) {
            console.error('Error logging in:', error.response.data.message);
            alert(error.response.data.message);
          } else {
            console.error('An unknown error occurred:', error);
            alert('An unknown error occurred. Please try again later.');
          }
        }
      },
      toggleRole(selectedRole) {
        this.role = selectedRole;
      }
    }
  };
  </script>
  
  <style scoped>
  /* Styles omitted for brevity */

  .login {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    background-color: #ffffff;
    border-radius: 20px;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
    text-align: center;
    margin-top: 150px;
  }
  
  .input-container {
    text-align: left;
    margin-bottom: 15px;
  }
  
  .input-container label {
    display: block;
    margin-bottom: 5px;
    font-size: 16px;
    font-weight: bold;
  }
  
  .input-box {
    position: relative;
    width: 100%;
  }
  
  .input-field {
    width: 100%;
    padding: 10px;
    padding-right: 40px; /* Make room for the icon */
    border: 1px solid #ccc;
    border-radius: 8px;
    box-sizing: border-box;
    font-size: 16px;
  }
  
  .input-box i {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 20px;
    color: #888;
  }
  
  .login-button {
    width: 100%;
    padding: 12px 0;
    border: none;
    border-radius: 8px;
    background-color: hsl(122, 39%, 49%);
    color: white;
    font-size: 18px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .login-button:hover {
    background-color: #45a049;
  }
  
  .register-link {
    position: auto;
  }
  
  .toggle-switch {
    display: flex;
    justify-content: center;
    margin-top: 20px;
  }
  
  .toggle-switch span {
    margin: 0 10px;
    padding: 10px 20px;
    border: 1px solid #45a049;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.3s ease, color 0.3s ease;
  }
  
  .toggle-switch span.active {
    background-color: #4CAF50;
    color: white;
  }
  
  .toggle-switch span:not(.active):hover {
    background-color: #f0f0f0;
  }
  </style>
   -->


   <template>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" />
    <div class="login">
      <div class="input-container">
        <label for="usernameOrEmail">Username or Email</label>
        <div class="input-box">
          <input type="text" v-model="usernameOrEmail" id="usernameOrEmail" placeholder="Enter Your Username or E-Mail" class="input-field" />
          <i class="fas fa-user"></i>
        </div>
      </div>
      <div class="input-container">
        <label for="password">Password</label>
        <div class="input-box">
          <input type="password" v-model="password" id="password" placeholder="Enter Password" class="input-field" />
          <i class="fas fa-lock"></i>
        </div>
      </div>
      <button @click="login" class="login-button">Login</button>
      <div class="register-link">
        <p>Don't have an account? <a href="/registerPage"> Click Here</a></p>
      </div>
      <div class="toggle-switch">
        <span :class="{'active': role === 'user'}" @click="toggleRole('user')">User</span>
        <span :class="{'active': role === 'admin'}" @click="toggleRole('admin')">Admin</span>
      </div>
    </div>
  </template>

<script>
import axios from 'axios';

export default {
  name: 'loginPage',
  data() {
    return {
      usernameOrEmail: '',
      password: '',
      role: 'user',
      error: ''
    };
  },
  methods: {
  async login() {
    try {
      const response = await axios.post('http://127.0.0.1:5000/login', {
        usernameOrEmail: this.usernameOrEmail,
        password: this.password,
        role: this.role
      });
      if (response && response.data) {
        console.log(response.data);
        localStorage.setItem('user', JSON.stringify(response.data.user));  // Store the user with ID
        this.$eventBus.login(response.data.user, this.role);
        localStorage.setItem('role', this.role);  // Store role in localStorage
        if (this.role === "user") {
          this.$router.push('/homePage');
        } else if (this.role === "admin") {
          this.$router.push('/adminPage');
        }
      } else {
        console.error('Unexpected response structure:', response);
        alert('An unexpected error occurred. Please try again later.');
      }
    } catch (error) {
      if (error.response && error.response.data && error.response.data.message) {
        console.error('Error logging in:', error.response.data.message);
        alert(error.response.data.message);
      } else {
        console.error('An unknown error occurred:', error);
        alert('An unknown error occurred. Please try again later.');
      }
    }
  },
  toggleRole(selectedRole) {
    this.role = selectedRole;
  }
}
};
</script>
<style scoped>
.login {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 20px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
  text-align: center;
  margin-top: 150px;
}

.input-container {
  text-align: left;
  margin-bottom: 15px;
}

.input-container label {
  display: block;
  margin-bottom: 5px;
  font-size: 16px;
  font-weight: bold;
}

.input-box {
  position: relative;
  width: 100%;
}

.input-field {
  width: 100%;
  padding: 10px;
  padding-right: 40px; /* Make room for the icon */
  border: 1px solid #ccc;
  border-radius: 8px;
  box-sizing: border-box;
  font-size: 16px;
}

.input-box i {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 20px;
  color: #888;
}

.login-button {
  width: 100%;
  padding: 12px 0;
  border: none;
  border-radius: 8px;
  background-color: hsl(122, 39%, 49%);
  color: white;
  font-size: 18px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.login-button:hover {
  background-color: #45a049;
}

.register-link {
  position: auto;
}

.toggle-switch {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.toggle-switch span {
  margin: 0 10px;
  padding: 10px 20px;
  border: 1px solid #45a049;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.toggle-switch span.active {
  background-color: #4CAF50;
  color: white;
}

.toggle-switch span:not(.active):hover {
  background-color: #f0f0f0;
}
</style>

  