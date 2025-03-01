<!-- <template>
    <div class="book-request-container">
      <h1>Book Requests</h1>
      <table v-if="bookRequests.length" class="book-request-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>User ID</th>
            <th>Book ID</th>
            <th>Status</th>
            <th>Request Date</th>
            <th>Grant Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in bookRequests" :key="request.id">
            <td>{{ request.id }}</td>
            <td>{{ request.user_id }}</td>
            <td>{{ request.book_id }}</td>
            <td :class="getStatusClass(request.status)">{{ request.status }}</td>
            <td>{{ new Date(request.request_date).toLocaleString() }}</td>
            <td>{{ request.grant_date ? new Date(request.grant_date).toLocaleString() : 'Pending' }}</td>
            <td>
              <button v-if="request.status === 'Pending'" class="approve-button" @click="approveRequest(request.id)">Approve</button>
              <button v-if="request.status === 'Pending'" class="reject-button" @click="rejectRequest(request.id)">Reject</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else class="no-requests">No book requests available.</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'BookRequest',
    data() {
      return {
        bookRequests: [],
        pollInterval: null
      };
    },
    created() {
      this.fetchBookRequests();
      this.startPolling();
    },
    beforeUnmount() {
      this.stopPolling();
    },
    methods: {
      async fetchBookRequests() {
        try {
          const response = await axios.get('http://127.0.0.1:5000/book_requests');
          this.bookRequests = response.data;
        } catch (error) {
          console.error('Error fetching book requests:', error);
        }
      },
      async approveRequest(requestId) {
        try {
          await axios.post(`http://127.0.0.1:5000/approve_request/${requestId}`);
          this.fetchBookRequests();
        } catch (error) {
          console.error('Error approving request:', error);
        }
      },
      async rejectRequest(requestId) {
        try {
          await axios.post(`http://127.0.0.1:5000/reject_request/${requestId}`);
          this.fetchBookRequests();
        } catch (error) {
          console.error('Error rejecting request:', error);
        }
      },
      getStatusClass(status) {
        if (status === 'Approved') return 'status-approved';
        if (status === 'Rejected') return 'status-rejected';
        return 'status-pending';
      },
      startPolling() {
        this.pollInterval = setInterval(() => {
          this.fetchBookRequests();
        }, 5000); // Poll every 5 seconds
      },
      stopPolling() {
        clearInterval(this.pollInterval);
      }
    }
  };
  </script>
  
  <style scoped>
  .book-request-container {
    padding: 20px;
    font-family: 'Arial', sans-serif;
    max-width: 1200px;
    margin: auto;
  }
  
  h1 {
    margin-bottom: 20px;
    font-size: 28px;
    color: #2c3e50;
    text-align: center;
  }
  
  .book-request-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  }
  
  .book-request-table th,
  .book-request-table td {
    border: 1px solid #ddd;
    padding: 12px;
    text-align: left;
  }
  
  .book-request-table th {
    background-color: #3498db;
    color: #fff;
    font-weight: bold;
  }
  
  .book-request-table tr:nth-child(even) {
    background-color: #f4f4f4;
  }
  
  .book-request-table tr:hover {
    background-color: #e1e1e1;
  }
  
  .approve-button,
  .reject-button {
    padding: 8px 12px;
    border: none;
    border-radius: 4px;
    color: #fff;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.3s ease;
  }
  
  .approve-button {
    background-color: #27ae60; /* Green */
  }
  
  .reject-button {
    background-color: #e74c3c; /* Red */
  }
  
  .approve-button:hover {
    background-color: #2ecc71;
  }
  
  .reject-button:hover {
    background-color: #c0392b;
  }
  
  .no-requests {
    font-size: 18px;
    color: #7f8c8d;
    text-align: center;
  }
  
  .status-approved {
    color: #27ae60;
    font-weight: bold;
  }
  
  .status-rejected {
    color: #e74c3c;
    font-weight: bold;
  }
  
  .status-pending {
    color: #f39c12;
    font-weight: bold;
  }
  </style>
   -->


   <template>
    <div class="book-request-container">
      <h1>Book Requests</h1>
      <table v-if="bookRequests.length" class="book-request-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>User ID</th>
            <th>Book ID</th>
            <th>Status</th>
            <th>Request Date</th>
            <th>Grant Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in bookRequests" :key="request.id">
            <td>{{ request.id }}</td>
            <td>{{ request.user_id }}</td>
            <td>{{ request.book_id }}</td>
            <td :class="getStatusClass(request.status)">{{ request.status }}</td>
            <td>{{ new Date(request.request_date).toLocaleString() }}</td>
            <td>{{ request.grant_date ? new Date(request.grant_date).toLocaleString() : 'Pending' }}</td>
            <td>
              <button v-if="request.status === 'Pending'" class="approve-button" @click="approveRequest(request.id)">Approve</button>
              <button v-if="request.status === 'Pending'" class="reject-button" @click="rejectRequest(request.id)">Reject</button>
              <button v-if="request.status === 'Approved'" class="revoke-button" @click="revokeRequest(request.id)">Revoke</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else class="no-requests">No book requests available.</p>
    </div>
  </template>

<script>
import axios from 'axios';

export default {
  name: 'BookRequest',
  data() {
    return {
      bookRequests: [],
      pollInterval: null
    };
  },
  created() {
    this.fetchBookRequests();
    this.startPolling();
  },
  beforeUnmount() {
    this.stopPolling();
  },
  methods: {
    async fetchBookRequests() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/book_requests');
        this.bookRequests = response.data;
      } catch (error) {
        console.error('Error fetching book requests:', error);
      }
    },
    async approveRequest(requestId) {
      try {
        await axios.post(`http://127.0.0.1:5000/approve_request/${requestId}`);
        this.fetchBookRequests();
      }
       
      catch (error) {
        console.error('Error approving request:', error);
      }
    },
    async rejectRequest(requestId) {
      try {
        await axios.post(`http://127.0.0.1:5000/reject_request/${requestId}`);
        this.fetchBookRequests();
      } catch (error) {
        console.error('Error rejecting request:', error);
      }
    },
    async revokeRequest(requestId) {
      try {
        await axios.post(`http://127.0.0.1:5000/revoke_request/${requestId}`);
        this.fetchBookRequests();
      } catch (error) {
        console.error('Error revoking request:', error);
      }
    },
    getStatusClass(status) {
      if (status === 'Approved') return 'status-approved';
      if (status === 'Rejected') return 'status-rejected';
      if (status === 'Revoked') return 'status-revoked';
      return 'status-pending';
    },
    startPolling() {
      this.pollInterval = setInterval(() => {
        this.fetchBookRequests();
      }, 5000); // Poll every 5 seconds
    },
    stopPolling() {
      clearInterval(this.pollInterval);
    }
  }
};
</script>

<style scoped>
  .book-request-container {
    padding: 20px;
    font-family: 'Arial', sans-serif;
    max-width: 1200px;
    margin: auto;
  }
  
  h1 {
    margin-bottom: 20px;
    font-size: 28px;
    color: #2c3e50;
    text-align: center;
  }
  
  .book-request-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  }
  
  .book-request-table th,
  .book-request-table td {
    border: 1px solid #ddd;
    padding: 12px;
    text-align: left;
  }
  
  .book-request-table th {
    background-color: #3498db;
    color: #fff;
    font-weight: bold;
  }
  
  .book-request-table tr:nth-child(even) {
    background-color: #f4f4f4;
  }
  
  .book-request-table tr:hover {
    background-color: #e1e1e1;
  }
  
  .approve-button,
  .reject-button {
    padding: 8px 12px;
    border: none;
    border-radius: 4px;
    color: #fff;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.3s ease;
  }
  
  .approve-button {
    background-color: #27ae60; /* Green */
  }
  
  .reject-button {
    background-color: #e74c3c; /* Red */
  }
  
  .approve-button:hover {
    background-color: #2ecc71;
  }
  
  .reject-button:hover {
    background-color: #c0392b;
  }
  
  .no-requests {
    font-size: 18px;
    color: #7f8c8d;
    text-align: center;
  }
  
  .status-approved {
    color: #27ae60;
    font-weight: bold;
  }
  
  .status-rejected {
    color: #e74c3c;
    font-weight: bold;
  }
  
  .status-pending {
    color: #f39c12;
    font-weight: bold;
  }
  .revoke-button {
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  color: #fff;
  cursor: pointer;
  font-size: 14px;
  background-color: #f39c12; /* Orange */
  transition: background-color 0.3s ease;
}

.revoke-button:hover {
  background-color: #e67e22;
}

.status-revoked {
  color: #f39c12;
  font-weight: bold;
}
  </style>