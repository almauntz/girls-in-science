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

  // Workshops
  {
    path: '/workshops',
    name: 'workshops',
    component: () => import('../views/workshops/WorkshopsView.vue'),
  },
  {
    path: '/workshops/admin',
    name: 'workshops-admin',
    component: () => import('../views/workshops/WorkshopsAdminView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/workshops/admin/proposals',
    name: 'proposals-admin',
    component: () => import('../views/workshops/ProposalAdminView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/workshops/admin/registrations',
    name: 'registrations-admin',
    component: () => import('../views/workshops/UsersListOnWorkshop.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/workshops/my-proposals',
    name: 'my-proposals',
    component: () => import('../views/workshops/MyProposalsView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/workshops/:id',
    name: 'workshops-detail',
    component: () => import('../views/workshops/WorkshopsDetailView.vue'),
  },

  // Mentoring — static routes MUST come before dynamic :id
  {
    path: '/mentoring',
    name: 'mentoring',
    component: () => import('../views/mentoring/MentoringView.vue'),
  },
  {
    path: '/mentoring/apply',
    name: 'mentor-registration',
    component: () => import('../views/mentoring/MentorRegistration.vue'),
  },
  {
    path: '/mentoring/my-applications',
    name: 'mentor-applications',
    component: () => import('../views/mentoring/MentorApplicationsView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/mentoring/:id/zahtjev',
    name: 'mentorship-request',
    component: () => import('../views/mentoring/MentorshipRequestView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/mentoring/:id',
    name: 'mentor-profil',
    component: () => import('../views/mentoring/MentorProfileView.vue')
  },

  // Student
  {
    path: '/student/apply',
    name: 'student-registration',
    component: () => import('../views/StudentRegistration.vue'),
  },

  // Role Models — static routes before dynamic :id
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
    path: '/role-models/:id/edit',
    name: 'rolemodels-edit',
    component: () => import('../views/rolemodels/RoleModelEdit.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/role-models/:id',
    name: 'rolemodels-detail',
    component: () => import('../views/rolemodels/RoleModelDetail.vue'),
  },

  // News — static routes before dynamic :id
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
    path: '/news/:id/edit',
    name: 'news-edit',
    component: () => import('../views/news/NewsEdit.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/news/:id',
    name: 'news-detail',
    component: () => import('../views/news/NewsDetail.vue'),
  },

  // Profiles
  {
    path: '/profiles',
    name: 'profiles',
    component: () => import('../views/profiles/ProfilesView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/profiles/:user_id',
    name: 'public-profile',
    component: () => import('../views/profiles/PublicProfileView.vue'),
  },

  // Admin
  {
    path: '/admin/users',
    name: 'admin-users',
    component: () => import('../views/profiles/AdminView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin/mentor-applications',
    name: 'admin-mentor-applications',
    component: () => import('../views/admin/MentorApplicationsView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin/mentor-applications/:id',
    name: 'admin-mentor-applications-detail',
    component: () => import('../views/admin/MentorApplicationDetailView.vue'),
    meta: { requiresAuth: true }
  },

  {
    path: '/unauthorized',
    name: 'unauthorized',
    component: () => import('../views/UnauthorizedView.vue')
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const isLoggedIn = !!localStorage.getItem('token')
  const userRole = localStorage.getItem('user_role')

  if (to.meta.requiresAuth && !isLoggedIn) {
    next('/login')
  } else if (to.meta.requiresAdmin && userRole !== 'admin') {
    next('/unauthorized')
  } else if (to.meta.guestOnly && isLoggedIn) {
    next('/')
  } else {
    next()
  }
})

export default router
