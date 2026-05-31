import axios from 'axios'

const API_URL = 'http://localhost:8000/mentoring'

export const getMentors = (skip = 0, limit = 10) => {
  return axios.get(`${API_URL}/mentors`, { params: { skip, limit } })
}

export const applyAsMentor = (formData) => {
  return axios.post(`${API_URL}/apply`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

export const getMentorById = (id) => {
  return axios.get(`${API_URL}/mentors/${id}`)
}

export const getMentorApplications = async () => {
  const token = localStorage.getItem('token')
  const response = await axios.get(`${API_URL}/my-applications`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })
  return response.data
}

export const updateApplicationStatus = async (applicationId, status) => {
  const token = localStorage.getItem('token')
  const response = await axios.put(
    `${API_URL}/applications/${applicationId}/status`,
    { status },
    {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    }
  )
  return response.data
}