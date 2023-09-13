import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AddQuestion from '../views/AddQuestion.vue'
import Eve from '../views/Eve.vue'
import Human from '../views/HuMan.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/add',
      name: 'addquestion',
      component: AddQuestion
    },
    {
      path: '/eve',
      name: 'eve',
      component: Eve
    },
    {
      path: '/human',
      name: 'human',
      component: Human 
    },
  ]
})

export default router
