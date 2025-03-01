import { createApp } from 'vue'
import App from './App.vue'
import router from './routes'
import { eventBus } from './eventbus';

// createApp(App).use(router).mount('#app')


const app = createApp(App);

app.config.globalProperties.$eventBus = eventBus;

app.use(router).mount('#app');
