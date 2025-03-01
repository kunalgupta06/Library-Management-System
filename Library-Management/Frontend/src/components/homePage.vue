<template>
    <div class="home-container">
      <header class="header">
        <h1>Welcome to the E-Library</h1>
        <p>Your gateway to a world of digital knowledge</p>
      </header>
      <main class="main-content">
        <section class="info">
          <h2>About Us</h2>
          <p>Our e-library offers a vast collection of digital books and resources across various genres. Enjoy easy access to knowledge from anywhere, anytime.</p>
        </section>
        <section class="rules">
          <h2>Rules & Regulations</h2>
          <ul>
            <li>Ensure that your account information is accurate and up-to-date.</li>
            <li>Respect copyright and intellectual property rights when accessing and using digital content.</li>
            <li>Do not share your login credentials with others. Each user should have their own account.</li>
            <li>Only use the digital content for personal, non-commercial purposes.</li>
            <li>Report any technical issues or content errors to our support team promptly.</li>
            <li>Abide by any specific licensing agreements or terms of use associated with individual e-books.</li>
            <li>Maintain the security of your personal data and do not use the e-library for malicious activities.</li>
          </ul>
        </section>
      </main>
      <footer class="footer">
        <p>&copy; 2024 E-Library Management System. All rights reserved.</p>
      </footer>
    </div>
  </template>
  
  <script>
  export default {
    name: 'homePage',
  }
  </script>
  
  <style scoped>
  .home-container {
    font-family: 'Arial', sans-serif;
    color: #333;
    padding: 0 20px;
    margin-top: 60px; /* Space for the fixed navbar */
  }
  
  .header {
    background: #67c8c2;
    color: white;
    padding: 2rem 1rem;
    border-radius: 10px;
    text-align: center;
    margin-bottom: 1rem;
  }
  
  .header h1 {
    font-size: 2rem;
    margin: 0;
  }
  
  .header p {
    font-size: 1.2rem;
    margin: 0.5rem 0;
  }
  
  .main-content {
    max-width: 800px;
    margin: 0 auto;
  }
  
  .info, .rules {
    background: #ffffff;
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
  }
  
  .info h2, .rules h2 {
    color: #0a5550;
    font-size: 1.5rem;
    margin-bottom: 1rem;
  }
  
  .info p, .rules ul {
    color: #333;
    font-size: 1rem;
    line-height: 1.6;
  }
  
  .rules ul {
    list-style: none;
    padding: 0;
  }
  
  .rules li {
    background: #f2f2f2;
    border-radius: 5px;
    padding: 0.5rem;
    margin-bottom: 0.5rem;
  }
  
  .footer {
    text-align: center;
    padding: 1rem;
    background: #0a5550;
    color: white;
    border-radius: 10px;
  }
  </style>
  