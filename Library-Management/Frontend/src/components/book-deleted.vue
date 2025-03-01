<template>
  <div>
    <book-item
      v-for="book in books"
      :key="book.id"
      :book="book"
      @delete="deleteBook(book.id)"
    />
  </div>
</template>

<script>
export default {
  data() {
    return {
      books: [], // Assume this is populated with your book data
    };
  },
  methods: {
    deleteBook(bookId) {
      fetch(`http://127.0.0.1:5000/deletebook/${bookId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include', // include credentials if necessary
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to delete the book');
          }
          return response.json();
        })
        .then(data => {
          console.log('Book deleted:', data);
          this.removeBookFromList(bookId); // Update the UI by removing the deleted book
        })
        .catch(error => {
          console.error('Error deleting book:', error);
        });
    },
    removeBookFromList(bookId) {
      this.books = this.books.filter(book => book.id !== bookId);
    }
  }
};
</script>
