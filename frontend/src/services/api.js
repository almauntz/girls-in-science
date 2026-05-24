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


// Ažuriranje statusa korisnice (aktivna/deaktivirana)
export async function updateUserStatus(token, userId, isActive) {
   const response = await fetch(`${BASE_URL}/profiles/${userId}/status?is_active=${isActive}`, {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })

  if (!response.ok) {
    throw new Error('Greška prilikom izmjene statusa na serveru')
  }

  return response.json()
}