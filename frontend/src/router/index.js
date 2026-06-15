import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { guestOnly: true }
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
    meta: { guestOnly: true }
  },
  
  //dodana ruta za listu radionnica
  {
    path: '/workshops',
    name: 'workshops',
    component: () => import('../views/workshops/WorkshopsView.vue'),
  },
  // Ruta za admin panel radionica  
  {
  path: '/workshops/admin',
  component: () => import('../views/workshops/WorkshopsAdminView.vue'),
  meta: { requiresAuth: true }
  },
  // Ruta za upravljanje prijedlozima radionica u admin panelu
  {
  path: '/workshops/admin/proposals',
  name: 'proposals-admin',
  component: () => import('../views/workshops/ProposalAdminView.vue'),
  meta: { requiresAuth: true }
  },
  // Ruta za pregled prijava na radionice
  {
  path: '/workshops/admin/registrations',
  name: 'registrations-admin',
  component: () => import('../views/workshops/UsersListOnWorkshop.vue'),
  meta: { requiresAuth: true }
  },
  //Ruta za prikaz prijedloga radionica koje je korisnik poslao
  {
  path: '/workshops/my-proposals',
  name: 'my-proposals',
  component: () => import('../views/workshops/MyProposalsView.vue'),
  meta: { requiresAuth: true }
  },
  //dodana ruta za detalje radionice
  {
   path: '/workshops/:id',
   name: 'workshops-detail',
  component: () => import('../views/workshops/WorkshopsDetailView.vue'),
  },
  {
    path: '/mentoring',
    name: 'mentoring',
    component: () => import('../views/mentoring/MentoringView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/role-models',
    name: 'role-models',
    component: () => import('../views/rolemodels/RoleModelsView.vue'),
    
  },
  {
    path: '/role-models/add',
    name: 'rolemodels-add',
    component: () => import('../views/rolemodels/RoleModelAdd.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/profiles',
    name: 'profiles',
    component: () => import('../views/profiles/ProfilesView.vue'),
    meta: { requiresAuth: true }
  },
  {
  path: '/role-models/:id',
  name: 'rolemodels-detail',
  component: () => import('../views/rolemodels/RoleModelDetail.vue'),
},
  {
  path: '/role-models/:id/edit',
  name: 'rolemodels-edit',
  component: () => import('../views/rolemodels/RoleModelEdit.vue'),
  meta: { requiresAuth: true }
},
{
  path: '/news',
  name: 'news',
  component: () => import('../views/news/NewsView.vue'),
},
{
  path: '/news/create',
  name: 'create-news',
  component: () => import('../views/news/CreateNewsView.vue'),
  meta: { requiresAuth: true }
},
{
  path: '/news/:id',
  name: 'news-detail',
  component: () => import('../views/news/NewsDetail.vue'),
},
{
  path: '/news/:id/edit',
  name: 'news-edit',
  component: () => import('../views/news/NewsEdit.vue'),
  meta: { requiresAuth: true }
},

  {
  path: '/profiles/:user_id',
  name: 'public-profile',
  component: () => import('../views/profiles/PublicProfileView.vue')
  },
  {
    path: '/admin/users',
    name: 'admin-users',
    component: () => import('../views/profiles/AdminView.vue'),
    meta: { requiresAuth: true }
  },
]
const router = createRouter({
  history: createWebHistory(),
  routes
})
router.beforeEach((to, from, next) => {
  const isLoggedIn = !!localStorage.getItem('token')
  if (to.meta.requiresAuth && !isLoggedIn) {
    next('/login')
  } else if (to.meta.guestOnly && isLoggedIn) {
    next('/')
  } else {
    next()
  }
})
export default router