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

export async function getActiveWorkshops() {
  const response = await fetch(`${BASE_URL}/workshops/active`)
  return response.json()
}

export async function getWorkshopDetails(workshopId) {
  const response = await fetch(`${BASE_URL}/workshops/${workshopId}`)
  return response.json()
}

// services/api.js

// services/api.js

export const registerForWorkshop = async (formData, token) => {
  // Puni URL: prefiks iz routera + putanja metode
  const url = 'http://localhost:8000/workshops/registration'; 

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}` 
    },
    body: JSON.stringify(formData)
  });

  if (!response.ok) {
    const errorData = await response.json();
    // Ovo će sada ispisati "Workshop not found" ili "Already registered"
    throw new Error(errorData.detail || 'Greška pri registraciji');
  }

  return await response.json();
};