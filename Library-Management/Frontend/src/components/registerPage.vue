<template>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" />
  <div class="register">
    <div class="input-container">
      <label for="name">Name</label>
      <div class="input-box">
        <input type="text" v-model="name" id="name" placeholder="Enter Your Name" class="input-field" />
      </div>
    </div>
    <div class="input-container">
      <label for="email">E-Mail</label>
      <div class="input-box">
        <input type="text" v-model="email" id="email" placeholder="Enter Your E-Mail" class="input-field" />
      </div>
    </div>
    <div class="input-container">
      <label for="phonenumber">PhoneNumber</label>
      <div class="input-box">
        <input type="text" v-model="phonenumber" id="phonenumber" placeholder="Enter Your Phone Number" class="input-field" length="10"/>
      </div>
    </div>
    <div class="input-container">
      <label for="username">Username</label>
      <div class="input-box">
        <input type="text" v-model="username" id="username" placeholder="Enter a Username" class="input-field" />
      </div>
    </div>
    <div class="input-container">
      <label for="password">Password</label>
      <div class="input-box">
        <input type="password" v-model="password" id="password" placeholder="Enter Password" class="input-field" />
      </div>
    </div>
    <div class="input-container">
      <label for="confirmpassword">Confirm Password</label>
      <div class="input-box">
        <input type="password" v-model="confirmpassword" id="confirmpassword" placeholder="Enter Confirm Password" class="input-field" />
      </div>
    </div>
    <button @click="register" class="register-button">Register</button>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  name: 'registerPage',
  data() {
    return {
      name: '',
      email: '',
      phonenumber: '',
      username: '',
      password: '',
      confirmpassword: '',
      error: '',
    };
  },
  methods: {
    async register() {
      this.error = '';
      if (!this.name || !this.email || !this.phonenumber || !this.username || !this.password || !this.confirmpassword) {
        this.error = 'Please fill in all fields';
        return;
      }
      if (!this.validateEmail(this.email)) {
        this.error = 'Please enter a valid email address';
        return;
      }
      if (this.password !== this.confirmpassword) {
        this.error = 'Passwords do not match';
        return;
      }
      
      const newuser = {
        name: this.name,
        email: this.email,
        phonenumber: this.phonenumber,
        username: this.username,
        password: this.password,
        confirmpassword: this.confirmpassword
      };

      try {
        const response = await axios.post('http://127.0.0.1:5000/register', newuser);
        console.log(response.data); // Handle success response
      
        if (response && response.data) {
          console.log(response.data);
          this.$router.push('/loginPage'); // Redirect to login page on successful registration
        } else {
          console.error('Unexpected response structure:', response);
          alert('An unexpected error occurred. Please try again later.');}}
      catch (error) {
        console.error('Error registering user:', error); // Handle error
      }
    },
    validateEmail(email) {
      const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return re.test(email);
    }
  }
}
</script>

<style>
    .register {
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
    margin-top:8px;
  }
  
  .input-box {
    position: flex;
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
  
  .register-button {
    width: 100%;
    padding: 12px 0;
    border: none;
    border-radius: 8px;
    background-color: #4CAF50;
    color: white;
    font-size: 18px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .register-button:hover {
    background-color: #45a049;
  }
  

</style>