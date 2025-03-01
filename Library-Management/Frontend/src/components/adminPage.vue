
   <template>
    <div class="librarian-dashboard">
      <h1>Librarian Dashboard</h1>
      <div class="stats">
        <div class="stat-item">
          <h3>Active Users</h3>
          <p>{{ stats.active_users }}</p>
        </div>
        <div class="stat-item">
          <h3>Grant Requests</h3>
          <p>{{ stats.grant_requests }}</p>
        </div>
        <div class="stat-item">
          <h3>E-Books Issued</h3>
          <p>{{ stats.ebooks_issued }}</p>
        </div>
      
      </div>
  
      <!-- Add Books Button -->
      <button @click="showAddBookModal = true" class="add-book-button">
        Add Books
      </button>
  
      <!-- Add Book Popup Modal -->
      <div v-if="showAddBookModal" class="modal-overlay" @click="closeModal">
        <div class="modal-content" @click.stop>
          <h2>Add New Book</h2>
          <form @submit.prevent="addBook">
            <div class="form-group">
              <label for="bookPhoto">Book Photo</label>
              <input type="file" id="bookPhoto" @change="handleFileChange" />
            </div>
            <div class="form-group">
              <label for="bookPDF">Upload Book PDF</label>
              <input type="file" id="bookPDF" @change="handlePDFChange" />
            </div>
            <div class="form-group">
              <label for="bookName">Book Name</label>
              <input type="text" id="bookName" v-model="newBook.bookName" />
            </div>
            <div class="form-group">
              <label for="author">Author</label>
              <input type="text" id="author" v-model="newBook.author" />
            </div>
            <div class="form-group">
              <label for="publishDate">Date of Publish</label>
              <input type="date" id="publishDate" :max="todayDate" v-model="newBook.publishDate" />
            </div>
            <div class="form-group">
              <label for="price">Price</label>
              <input type="number" id="price" v-model="newBook.price" />
            </div>
            <div class="form-group">
              <label for="genre">Genre</label>
              <input type="text" id="genre" v-model="newBook.genre" />
            </div>
            <button type="submit">Submit</button>
            <button type="button" @click="closeModal">Cancel</button>
          </form>
        </div>
      </div>
  

      <button @click="triggerExportCSV" class="btn">Export Book Requests to CSV</button>
  
      <!-- Task Status Display -->
      <div v-if="taskStatus">
        <h3>Task Status:</h3>
        <p>Task ID: {{ taskStatus.task_id }}</p>
        <p>Status: {{ taskStatus.status }}</p>
        <p v-if="taskStatus.result">Result: {{ taskStatus.result }}</p>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  
  export default {
    name: 'adminPage',
    setup() {
      const stats = ref({
        active_users: 0,
        grant_requests: 0,
        ebooks_issued: 0,
        ebooks_revoked: 0,
      });
  
      const showAddBookModal = ref(false);
      const newBook = ref({
        bookName: '',
        author: '',
        publishDate: '',
        price: '',
        bookPhoto: null,
        bookPDF: null,
        genre: '',
      });
  
      const handleFileChange = (event) => {
        newBook.value.bookPhoto = event.target.files[0];
      };
  
      const handlePDFChange = (event) => {
        newBook.value.bookPDF = event.target.files[0];
      };
  
      const addBook = async () => {
        const formData = new FormData();
        formData.append('bookName', newBook.value.bookName);
        formData.append('author', newBook.value.author);
        formData.append('dateOfPublish', newBook.value.publishDate);
        formData.append('price', newBook.value.price);
        formData.append('bookPhoto', newBook.value.bookPhoto);
        formData.append('bookPDF', newBook.value.bookPDF);
        formData.append('genre', newBook.value.genre);
  
        try {
          const response = await fetch('http://127.0.0.1:5000/addbook', {
            method: 'POST',
            body: formData,
          });
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          const data = await response.json();
          console.log('Book added:', data);
        } catch (error) {
          console.error('Error adding book:', error);
        }
  
        showAddBookModal.value = false;
      };
  
      const closeModal = () => {
        showAddBookModal.value = false;
      };
  
      const fetchData = async () => {
        try {
          const response = await fetch('http://127.0.0.1:5000/stats');
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          const data = await response.json();
          stats.value = data;
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      };
  
      onMounted(() => {
        fetchData();
      });
  
      const triggerTask = async (taskType) => {
        try {
          const response = await fetch(`http://127.0.0.1:5000/trigger-task/${taskType}`, {
            method: 'POST',
          });
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          const data = await response.json();
          console.log('Task triggered:', data);
        } catch (error) {
          console.error('Error triggering task:', error);
        }
      };
  
//       const triggerExportCSV = async () => {
//   try {
//     const response = await fetch('http://127.0.0.1:5000/export-csv', {
//       method: 'POST',
//     });
//     if (!response.ok) {
//       throw new Error('Network response was not ok');
//     }
//     const data = await response.json();
//     taskStatus.value = data;
//     console.log('CSV export triggered:', data);
    
    
//   } catch (error) {
//     console.error('Error exporting CSV:', error);
//   }
// };
  
      return {
        stats,
        showAddBookModal,
        newBook,
        addBook,
        closeModal,
        handleFileChange,
        handlePDFChange,
        fetchData,
        triggerTask,
        // triggerExportCSV,
      };
    },
  };
  </script>
  
  <style scoped>
  .librarian-dashboard {
    padding: 20px;
  }
  
  .stats {
    display: flex;
    flex-wrap: wrap;
  }
  
  .stat-item {
    flex: 1;
    margin: 10px;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    background-color: white;
  }
  
  .add-book-button {
    margin-top: 20px;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    background-color: #4CAF50;
    color: white;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .add-book-button:hover {
    background-color: #45a049;
  }
  
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 80%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 100px;
  }
  
  .modal-content {
    background: white;
    padding: 20px;
    border-radius: 5px;
    width: 80%;
    max-width: 600px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  .form-group label {
    display: block;
    margin-bottom: 5px;
  }
  
  .form-group input {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
  }
  
  .btn {
    margin: 10px;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    background-color: #007bff;
    color: white;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .btn:hover {
    background-color: #0056b3;
  }
  </style>
  