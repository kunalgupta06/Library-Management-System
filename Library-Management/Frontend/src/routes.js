import LandingPage from './components/landingpage.vue'
import loginPage from './components/loginPage.vue'
import registerPage from './components/registerPage.vue'
import homePage from './components/homePage.vue'
import LibBook from './components/LibBook.vue'
import {  createRouter, createWebHistory} from 'vue-router'
import adminPage from './components/adminPage.vue';
import membersPage from './components/members.vue'
import BookRequest from './components/BookRequest.vue'

const routes = [
    {
        name: 'LandingPage',
        component: LandingPage,
        path: '/',
    },
    {
        name: 'Login',
        component: loginPage,
        path: '/loginPage',
    },
    {
        name: 'Register',
        component: registerPage,
        path: '/registerPage',
    },
    {
        name: 'Homepage',
        component: homePage, meta: { requiresAuth: true, requiresuser: true },
        path: '/homePage',
    },
    {
        name: 'LibBook',
        component: LibBook,
        path: '/LibBook',
    },
    {   name:'adminPage',
        component: adminPage, meta: { requiresAuth: true, requiresAdmin: true },
        path: '/adminPage',
         },

    {   name:'members',
        component: membersPage,
        path: '/members',
        },
        {
          name: 'BookRequest',
          component: BookRequest,
          path: '/BookRequest',
      },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
});
router.beforeEach((to, from, next) => {
    const isAuthenticated = localStorage.getItem('user');
    const role = localStorage.getItem('role');
  
    if (to.matched.some(record => record.meta.requiresAuth)) {
      if (!isAuthenticated) {
        next({ path: '/loginPage' });
      } else if (to.matched.some(record => record.meta.requiresAdmin) && role !== 'admin') {
        next({ path: '/homePage' });
      } else {
        next();
      }
    } else {
      next();
    }
  });
  


export default router;
