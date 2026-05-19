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
export const getMentorById = (id) => {
  return axios.get(`${API_URL}/mentors/${id}`)
}