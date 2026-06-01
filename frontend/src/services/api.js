const BASE_URL = 'http://127.0.0.1:8000'

export async function registerUser(email, fullName, password) {
  const response = await fetch(`${BASE_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, full_name: fullName, password })
  })
  return response.json()
}

export async function loginUser(email, password) {
  const formData = new FormData()
  formData.append('username', email)
  formData.append('password', password)

  const response = await fetch(`${BASE_URL}/auth/login`, {
    method: 'POST',
    body: formData
  })
  return response.json()
}

export async function getMe(token) {
  const response = await fetch(`${BASE_URL}/me`, {
    headers: { 'Authorization': `Bearer ${token}` }
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
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })
  return response.json()
}

export async function createNewsPost(data, token) {
  const response = await fetch(`${BASE_URL}/news`, {
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
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(data)
  })
  return response.json()
}