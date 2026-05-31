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
  {
    path: '/workshops',
    name: 'workshops',
    component: () => import('../views/workshops/WorkshopsView.vue'),
    meta: { requiresAuth: true }
  },
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
    path: '/student/apply',
    name: 'student-registration',
    component: () => import('../views/StudentRegistration.vue'),
  },
  {
    path: '/mentoring/my-applications',
    name: 'mentor-applications',
    component: () => import('../views/mentoring/MentorApplicationsView.vue'),
    meta: { requiresAuth: true }
  },
  {
  path: '/mentoring/:id',
  name: 'mentor-profil',
  component: () => import('../views/mentoring/MentorProfileView.vue')
  },
  {
    path: '/forum',
    name: 'forum',
    component: () => import('../views/forum/ForumView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/profiles',
    name: 'profiles',
    component: () => import('../views/profiles/ProfilesView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin/mentor-applications',
    name: 'admin-mentor-applications',
    component: () => import('../views/admin/MentorApplicationsView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/mentor-applications/:id',
    name: 'admin-mentor-applications-detail',
    component: () => import('../views/admin/MentorApplicationDetailView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/unauthorized',
    name: 'unauthorized',
    component: () => import('../views/UnauthorizedView.vue')
  },
  {
    path: '/mentoring/apply',
    name: 'student-apply',
    component: () => import('../views/mentoring/StudentRegistration.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/mentoring/:id/zahtjev',
    name: 'mentorship-request',
    component: () => import('../views/mentoring/MentorshipRequestView.vue'),
    meta: { requiresAuth: true }
  }

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const isLoggedIn = !!localStorage.getItem('token')
  const userRole = localStorage.getItem('role')

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
