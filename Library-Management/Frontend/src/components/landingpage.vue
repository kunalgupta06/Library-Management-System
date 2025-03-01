<template>
  
    <div class="promo-photos">
      <img :src="photos[currentPhoto]" alt="Promotional Photo" />
    </div>
  
</template>

<script>
export default {
  name: 'LandingPage',
  data() {
    return {
      isOpen: false,
      photos: [
        'https://i.pinimg.com/564x/25/a7/0e/25a70e4b073836a212d4f1d0a9d2c3b8.jpg',
        'https://i.pinimg.com/564x/73/50/97/735097cc3810372d8437f37f597eddac.jpg',
        'https://i.pinimg.com/564x/1a/92/92/1a92926f299d2e9378dceecac1fd6554.jpg',
      ],
      currentPhoto: 0,
    };
  },
  methods: {
    toggleMenu() {
      this.isOpen = !this.isOpen;
    },
    changePhoto() {
      this.currentPhoto = (this.currentPhoto + 1) % this.photos.length;
    }
  },
  mounted() {
    this.photoInterval = setInterval(this.changePhoto, 10);
  },
  beforeUnmount() {
    clearInterval(this.photoInterval);
  },
};
</script>

<style scoped>

.promo-photos {
  margin-top: 80px; /* Adjust as needed for spacing from navbar */
  text-align: center;
}

.promo-photos img {
  width: 40%;
  height:80%;
  max-height: 800px; /* Adjust height as needed */
  object-fit: flex;
  margin-top:50px;
}

@media screen and (max-width: 768px) {
  .nav-links {
    display: none;
  }

  .hamburger {
    display: flex;
  }

  .buttons {
    display: none;
  }
}
</style>
