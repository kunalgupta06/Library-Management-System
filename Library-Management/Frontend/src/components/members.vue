<template>
    <div>
      <!-- Show message if user is not authorized -->
      <div v-if="user && user.role === 'user'">
        <h2>Unauthorized</h2>
        <p>You are not authorized to view this data.</p>
      </div>
  
      <!-- Show list of users if the user is an admin -->
      <div v-if="user && user.role === 'admin'" class="members-container">
        <h2>Members</h2>
        <div v-for="member in members" :key="member.id" class="member-box">
          <p>Name: {{ member.name }}</p>
          <p>Username: {{ member.username }}</p>
          <p>ID: {{ member.id }}</p>
          <p>Active: {{ member.active ? 'Yes' : 'No' }}</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { onMounted, ref } from 'vue';
  
  export default {
    name: 'membersPage',
    setup() {
      const user = ref(null);
      const members = ref([]);
  
      const fetchUser = () => {
        const storedUser = localStorage.getItem('user');
        if (storedUser) {
          try {
            user.value = JSON.parse(storedUser);
          } catch (e) {
            console.error('Error parsing user from localStorage:', e);
          }
        }
      };
  
      const fetchMembers = async () => {
        try {
          const response = await fetch('http://127.0.0.1:5000/members');
          if (!response.ok) throw new Error('Network response was not ok');
          const data = await response.json();
          members.value = data;
        } catch (error) {
          console.error('Error fetching members:', error);
        }
      };
  
      onMounted(() => {
        fetchUser();
        if (user.value && user.value.role === 'admin') {
          fetchMembers();
        }
      });
  
      return {
        user,
        members
      };
    },
  };
  </script>
  
  <style scoped>
  .members-container {
    padding: 20px;
  }
  
  .member-box {
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 15px;
    margin-bottom: 15px;
    width: 300px;
    text-align: center;
  }
  
  .members-container h2 {
    text-align: center;
    margin-bottom: 20px;
    color: #007bff;
    font-size: 2em;
    font-family: Arial, sans-serif;
  }
  
  .member-box p {
    margin: 5px 0;
    color: #463a3a;
    font-family: Arial, sans-serif;
  }
  
  h2 {
    color: #dc3545;
    text-align: center;
  }
  </style>
  