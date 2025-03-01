<template>
  <div>
    <div class="search-category-container">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search by name or author..."
        class="search-bar"
      />
      <select v-model="selectedGenre" class="genre-dropdown">
        <option value="">All Genres</option>
        <option v-for="genre in genres" :key="genre" :value="genre">{{ genre }}</option>
      </select>
    </div>

    <div class="book-list">
      <div v-for="book in filteredBooks" :key="book.id" class="book-item">
        <img :src="book.photo_path" alt="Book Photo" />

        <h3>Name: {{ book.book_name }}</h3>
        <p>Author: {{ book.author }}</p>
        <p>Genre: {{ book.genre }}</p>
        <p>Price: ₹{{ book.price }}</p>
        
        <div class="book-buttons">
          <template v-if="user && user.role === 'admin'">
            <button @click="openUpdateModal(book)" class="btn-update">Update</button>
            <button @click="deleteBook(book.id)" class="btn-delete">Delete</button>
          </template>
          <template v-if="user && user.role === 'user'">
            <template v-if="book.is_rented === 'Pending'">
              <button class="btn-pending" disabled>Pending</button>
            </template>
            <template v-else-if="book.is_rented === 'Approved'">
              <button @click="returnBook(book)" class="btn-return">Return</button>
              <a :href="book.pdf_filename" target="_blank" class="btn-view-pdf">View PDF</a>
            </template>
            <template v-else>
              <button @click="rentBook(book)" class="btn-rent">Rent</button>
            </template>
          </template>
        </div>

        <div v-if="user && user.role === 'user' && book.is_rented === 'Rejected'">
          <p class="pdf-access-message">Access rejected.</p>
        </div>
        <div v-else-if="user && user.role === 'user' && !book.is_rented">
          <p class="pdf-access-message">Buy or rent the book to view the PDF.</p>
        </div>
      </div>
    </div>

    <UpdateBookModal
      v-if="showUpdateModal"
      :showModal="showUpdateModal"
      :book="selectedBook"
      @close-modal="showUpdateModal = false"
      @update-success="fetchBooks"
    />
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import UpdateBookModal from './updatebook.vue';

export default {
  name: 'LibBook',
  components: { UpdateBookModal },
  setup() {
    const books = ref([]);
    const user = ref(null);
    const searchQuery = ref('');
    const selectedGenre = ref('');
    const showUpdateModal = ref(false);
    const selectedBook = ref(null);
    const genres = ref([]);

    const fetchBooks = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/libBook');
        if (response.status === 200) {
          books.value = response.data;

          // Populate genres from books data
          genres.value = [...new Set(books.value.map(book => book.genre))];

          const grantRequestsResponse = await axios.get('http://127.0.0.1:5000/book_requests');
          const grantRequests = grantRequestsResponse.data;

          books.value.forEach(book => {
            const request = grantRequests.find(req => req.book_id === book.id && req.user_id === user.value.id);
            if (request) {
              book.is_rented = request.status;
            }
          });
        } else {
          console.error('Failed to fetch books:', response.status);
        }
      } catch (error) {
        console.error('Error fetching books:', error.response ? error.response.data : error.message);
      }
    };

    const fetchUser = () => {
      const storedUser = localStorage.getItem('user');
      if (storedUser) {
        try {
          user.value = JSON.parse(storedUser);
          console.log("Fetched user:", user.value);
        } catch (e) {
          console.error('Error parsing user from localStorage:', e);
        }
      }
    };

    const deleteBook = async (bookId) => {
      try {
        const response = await axios.delete(`http://127.0.0.1:5000/deletebook/${bookId}`);
        if (response.status === 200) {
          books.value = books.value.filter(book => book.id !== bookId);
        }
      } catch (error) {
        console.error('Error deleting book:', error);
      }
    };

    const rentBook = async (book) => {
      console.log("Rent button clicked for book:", book);
      if (user.value && user.value.role === 'user' && user.value.id) {
        try {
          const response = await axios.post('http://127.0.0.1:5000/rentbook', {
            book_id: book.id,
            user_id: user.value.id,
          });

          if (response.status === 200) {
            console.log("Book rental successful, setting status to 'Pending'");
            book.is_rented = 'Pending';
            console.log("Updated book status:", book.is_rented);
            alert(response.data.message);

            const rentedBooks = JSON.parse(localStorage.getItem('rentedBooks')) || [];
            if (!rentedBooks.includes(book.id)) {
              rentedBooks.push(book.id);
            }
            localStorage.setItem('rentedBooks', JSON.stringify(rentedBooks));

            await fetchBooks();
          } else {
            console.error('Unexpected response status:', response.status);
          }
        } catch (error) {
          console.error('Error renting book:', error.response ? error.response.data : error.message);
        }
      } else {
        console.error('User ID is not available or user is not logged in');
      }
    };

    const returnBook = async (book) => {
      console.log("Return button clicked for book:", book);
      if (user.value && user.value.role === 'user' && user.value.id) {
        try {
          const response = await axios.post('http://127.0.0.1:5000/returnbook', {
            book_id: book.id,
            user_id: user.value.id,
          });

          if (response.status === 200) {
            console.log("Book return successful, resetting state");
            book.is_rented = '';
            console.log("Updated book status:", book.is_rented);
            alert(response.data.message);

            let rentedBooks = JSON.parse(localStorage.getItem('rentedBooks')) || [];
            rentedBooks = rentedBooks.filter(id => id !== book.id);
            localStorage.setItem('rentedBooks', JSON.stringify(rentedBooks));

            await fetchBooks();
          } else {
            console.error('Unexpected response status:', response.status);
          }
        } catch (error) {
          console.error('Error returning book:', error.response ? error.response.data : error.message);
        }
      } else {
        console.error('User ID is not available or user is not logged in');
      }
    };

    const openUpdateModal = (book) => {
      selectedBook.value = book;
      showUpdateModal.value = true;
    };

    onMounted(() => {
      fetchBooks();
      fetchUser();
    });

    const filteredBooks = computed(() => {
      const query = searchQuery.value.toLowerCase();
      return books.value.filter(book => {
        return (
          (query ? (book.book_name.toLowerCase().includes(query) || book.author.toLowerCase().includes(query)) : true) &&
          (selectedGenre.value ? book.genre === selectedGenre.value : true)
        );
      });
    });

    return {
      books,
      user,
      searchQuery,
      selectedGenre,
      showUpdateModal,
      selectedBook,
      genres,
      fetchBooks,
      deleteBook,
      rentBook,
      returnBook,
      openUpdateModal,
      filteredBooks,
    };
  }
};
</script>



<style scoped>
/* Container for the search and category filters */
.search-category-container {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

/* Style for the search bar */
.search-bar {
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 70%;
  margin-top: 40px;
}

/* Style for the genre dropdown */
.genre-dropdown {
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 25%;
  margin-top: 40px;
}

/* Container for the book list */
.book-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

/* Style for individual book items */
.book-item {
  background: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  width: calc(33% - 20px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
}

.book-item h3 {
  margin-top: 0;
}

.book-item p {
  margin: 5px 0;
}

/* Style for buttons */
.book-buttons {
  margin-top: 10px;
}

.btn-update,
.btn-delete,
.btn-rent,
.btn-pending,
.btn-return,
.btn-view-pdf {
  padding: 10px;
  font-size: 14px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 5px;
}

.btn-update {
  background-color: #4CAF50;
  color: white;
}

.btn-delete {
  background-color: #f44336;
  color: white;
}

.btn-rent {
  background-color: #2196F3;
  color: white;
}

.btn-pending {
  background-color: #FFC107;
  color: black;
  cursor: not-allowed;
}

.btn-return {
  background-color: #FF5722;
  color: white;
}

.btn-view-pdf {
  background-color: #9C27B0;
  color: white;
}

.pdf-access-message {
  margin-top: 10px;
  color: #666;
  font-size: 14px;
}

/* Modal styles */
.update-book-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.update-book-modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.update-book-modal-content h2 {
  margin-top: 0;
}

.update-book-modal-content .btn-close {
  background: #f44336;
  color: white;
  border: none;
  padding: 8px;
  border-radius: 4px;
  cursor: pointer;
  float: right;
}

.update-book-modal-content .btn-submit {
  background: #4CAF50;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 4px;
  cursor: pointer;
}

.update-book-modal-content input,
.update-book-modal-content select {
  margin-bottom: 10px;
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: calc(100% - 20px);
}
</style>
