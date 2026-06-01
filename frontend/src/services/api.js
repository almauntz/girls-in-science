const BASE_URL = 'http://127.0.0.1:8000'

/* =========================================================
   AUTH HELPERS
========================================================= */

const getToken = () => {
  const token = localStorage.getItem('token')

  if (!token || token === 'null' || token === 'undefined') {
    return null
  }

  return token
}

export const getAuthHeaders = () => {
  const token = getToken()

  if (!token) {
    return {
      'Content-Type': 'application/json'
    }
  }

  return {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`
  }
}

/* =========================================================
   SAFE FETCH WRAPPER
========================================================= */

const apiRequest = async (url, options = {}) => {
  const res = await fetch(`${BASE_URL}${url}`, {
    ...options,
    headers: {
      ...(options.headers || {})
    }
  })

  let data
  try {
    data = await res.json()
  } catch {
    data = null
  }

  if (!res.ok) {
    const error = new Error(data?.detail || 'Server error')
    error.status = res.status
    error.data = data
    throw error
  }

  return data
}

/* =========================================================
   AUTH
========================================================= */

export async function registerUser(email, fullName, password) {
  return apiRequest('/auth/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      email,
      full_name: fullName,
      password
    })
  })
}

export async function loginUser(email, password) {
  const formData = new FormData()
  formData.append('username', email)
  formData.append('password', password)

  return apiRequest('/auth/login', {
    method: 'POST',
    body: formData,
    headers: {} // form-data NE treba content-type
  })
}

/* =========================================================
   USER
========================================================= */

export async function getMe() {
  return apiRequest('/me', {
    method: 'GET',
    headers: getAuthHeaders()
  })
}

/* =========================================================
   WORKSHOPS
========================================================= */

export async function getActiveWorkshops() {
  return apiRequest('/workshops/active', {
    method: 'GET'
  })
}

export async function getWorkshopDetails(workshopId) {
  return apiRequest(`/workshops/${workshopId}`, {
    method: 'GET'
  })
}

/* =========================================================
   REGISTRATION
========================================================= */

export const registerForWorkshop = async (registrationData) => {
  return apiRequest('/workshops/registration', {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(registrationData)
  })
}

export const cancelWorkshopRegistration = async (workshopId) => {
  return apiRequest(`/workshops/cancellation/${workshopId}`, {
    method: 'DELETE',
    headers: getAuthHeaders()
  })
}

/* =========================================================
   WAITING LIST
========================================================= */

export const joinWaitingList = async (workshopId) => {
  return apiRequest(`/workshops/waiting-list/join/${workshopId}`, {
    method: 'POST',
    headers: getAuthHeaders()
  })
}

/* =========================================================
   PROMOTION CHECK
========================================================= */

export const checkMyPromotion = async () => {
  return apiRequest('/workshops/my-promotion', {
    method: 'GET',
    headers: getAuthHeaders()
  })
}