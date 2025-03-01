<template>
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeModal">&times;</span>
        <h3>Update Book</h3>
        <form @submit.prevent="updateBook">
          <div class="form-group">
            <label for="bookName">Book Name</label>
            <input v-model="bookData.book_name" type="text" id="bookName" required />
          </div>
          <div class="form-group">
            <label for="author">Author</label>
            <input v-model="bookData.author" type="text" id="author" required />
          </div>
          <div class="form-group">
            <label for="dateOfPublish">Date of Publish</label>
            <input v-model="bookData.date_of_publish" type="date" id="dateOfPublish" required />
          </div>
          <div class="form-group">
            <label for="price">Price</label>
            <input v-model="bookData.price" type="number" id="price" required />
          </div>
          <div class="form-group">
            <label for="genre">Genre</label>
            <input v-model="bookData.genre" type="text" id="genre" required />
          </div>
          <div class="form-group">
            <label for="bookPhoto">Book Photo</label>
            <input type="file" @change="handleFileUpload" id="bookPhoto" />
          </div>
          <button type="submit" class="btn-save">Save</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'UpdateBookModal',
    props: {
      showModal: {
        type: Boolean,
        required: true,
      },
      book: {
        type: Object,
        required: true,
      },
    },
    data() {
      return {
        bookData: { ...this.book },
        selectedFile: null,
      };
    },
    methods: {
      handleFileUpload(event) {
        this.selectedFile = event.target.files[0];
      },
      async updateBook() {
        // Create a form data object to send data to backend
        const formData = new FormData();
        formData.append('bookName', this.bookData.book_name);
        formData.append('author', this.bookData.author);
        formData.append('dateOfPublish', this.bookData.date_of_publish);
        formData.append('price', this.bookData.price);
        formData.append('genre', this.bookData.genre);
        if (this.selectedFile) {
          formData.append('bookPhoto', this.selectedFile);
        }
  
        try {
          const response = await fetch(`http://127.0.0.1:5000/updatebook/${this.book.id}`, {
            method: 'PUT',
            body: formData,
          });
          if (response.ok) {
            // Close modal and refresh books
            this.$emit('update-success');
            this.closeModal();
          } else {
            console.error('Failed to update book');
          }
        } catch (error) {
          console.error('Error:', error);
        }
      },
      closeModal() {
        this.$emit('close-modal');
      },
    },
  };
  </script>
  
  <style scoped>
  .modal {
    display: flex;
    justify-content: center;
    align-items: center;
    position: fixed;
    z-index: 1;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgb(0, 0, 0);
    background-color: rgba(0, 0, 0, 0.4);
  }
  
  .modal-content {
    background-color: #fefefe;
    margin: 15% auto;
    padding: 20px;
    border: 1px solid #888;
    width: 80%;
    max-width: 600px;
    border-radius: 10px;
  }
  
  .close {
    color: #aaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
  }
  
  .close:hover,
  .close:focus {
    color: black;
    text-decoration: none;
    cursor: pointer;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  .form-group label {
    display: block;
    margin-bottom: 5px;
  }
  
  .form-group input[type="text"],
  .form-group input[type="date"],
  .form-group input[type="number"],
  .form-group input[type="file"] {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
  }
  
  .btn-save {
    background-color: #4caf50;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .btn-save:hover {
    background-color: #45a049;
  }
  </style>
  