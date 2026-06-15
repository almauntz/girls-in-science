const BASE_URL = 'http://127.0.0.1:8000'

/* =========================================================
   AUTH HELPERS

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
/* =========================================================
   RATINGS
========================================================= */

export const checkRegistration = async (workshopId) => {
  return apiRequest(`/workshops/registration/check/${workshopId}`, {
    method: 'GET',
    headers: getAuthHeaders()
  })
}

export const submitWorkshopRating = async (workshopId, ratingPayload) => {
  return apiRequest(`/workshops/${workshopId}/ratings`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(ratingPayload)
  })
}

export const getWorkshopRatings = async (workshopId) => {
  return apiRequest(`/workshops/${workshopId}/ratings`, {
    method: 'GET'
  })
}

export const getWorkshopRatingsAverage = async (workshopId) => {
  return apiRequest(`/workshops/${workshopId}/ratings/average`, {
    method: 'GET'
  })
}

export const autoCompleteWorkshops = async () => {
  return apiRequest('/workshops/auto-complete', {
    method: 'POST'
  })
  return response.json()
}

// dohvat profila
export async function getMyProfile(token) {
  const response = await fetch(`${BASE_URL}/profiles/me`, {
    headers: { 
      'Authorization': `Bearer ${token}` 
    }
  })
  return response.json()
}

// ažuriranje profila
export async function updateProfile(token, data) {
  const response = await fetch(`${BASE_URL}/profiles/me`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(data)
  })
  return response.json()
}

export async function getRoleModels() {
  const response= await fetch(`${BASE_URL}/role-models/`)
  return response.json()
}

export async function getRoleModel(id) {
  const response = await fetch(`${BASE_URL}/role-models/${id}`)
  return response.json()
}

export async function updateRoleModel(id, data) {
  const token = localStorage.getItem('token')
  const response = await fetch(`${BASE_URL}/role-models/${id}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(data)
  })
  return response.json()
}

export async function addRoleModel(data, token) {
  const response = await fetch(`${BASE_URL}/role-models/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(data)
  })
  return response.json()
}

export async function deleteRoleModel(id, token) {
  const response = await fetch(`${BASE_URL}/role-models/${id}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })
  return response.json()
}

export async function getNewsPost(id) {
  const response = await fetch(`${BASE_URL}/news/${id}`)
  return response.json()
}

export async function deleteNewsPost(id, token) {
  const response = await fetch(`${BASE_URL}/news/${id}`, {
    method: 'DELETE',

// Dohvatanje svih korisnika za admin panel
export async function getAllUsers(token) {
  const response = await fetch(`${BASE_URL}/admin/users`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })

  if (response.status === 403) {
    throw new Error('DEAKTIVIRAN_NALOG');
  }

  if (!response.ok) {
    throw new Error('Greška prilikom dohvaćanja liste korisnika')
  }

  return response.json()
}


// Ažuriranje statusa korisnice (aktivna/deaktivirana)
export async function updateUserStatus(token, userId, isActive) {
   const response = await fetch(`http://127.0.0.1:8000/admin/${userId}/status?is_active=${isActive}`, {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })
  return response.json()
}

export async function createNewsPost(data, token) {
  const response = await fetch(`${BASE_URL}/news/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify(data)
  })
  return response.json()
}

export async function getNewsPosts() {
  const response = await fetch(`${BASE_URL}/news/`)
  return response.json()
}

export async function updateNewsPost(id, data) {
  const token = localStorage.getItem('token')
  const response = await fetch(`${BASE_URL}/news/${id}`, {
    method: 'PATCH',

  if (!response.ok) {
    throw new Error('Greška prilikom izmjene statusa na serveru')
  }

  return response.json()
}


// GIS4-74/75: Ažuriranje uloge korisnice (Studentica, Mentorica, Admin)
export async function updateUserRole(token, userId, newRole) {
  const response = await fetch(`${BASE_URL}/admin/${userId}/role`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(data)
  })
    // Šaljemo ulogu unutar body-ja kao JSON
    body: JSON.stringify({ role: newRole })
  })

  if (!response.ok) {
    throw new Error('Greška prilikom izmjene uloge na serveru')
  }

  return response.json()
}