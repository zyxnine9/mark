import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Train',
    component: ()=>import('../views/Train')
  },
  {
    path: '/home',
    name: 'Home',
    component: ()=>import('../views/Home')
  },
  {
    path: '/mark',
    name: 'Mark',
    component: ()=>import('../views/Mark')
<<<<<<< HEAD
=======
  },
  {
    path: '/train',
    name: 'train',
    component: ()=>import('../views/Train')
>>>>>>> 93601844cc75e63326eea7bb55903a8a9e654468
  }
]

const router = new VueRouter({
  mode: 'history',
<<<<<<< HEAD
  base: process.env.BASE_URL,
=======
  base: '/mark/ui',
>>>>>>> 93601844cc75e63326eea7bb55903a8a9e654468
  routes
})

export default router
