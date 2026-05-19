import axios from 'axios'

const API_URL = 'http://localhost:8000/mentoring'

export const getMentors = (skip = 0, limit = 10) => {
  return axios.get(`${API_URL}/mentors`, { params: { skip, limit } })
}
export const getMentorById = (id) => {
  return axios.get(`${API_URL}/mentors/${id}`)
}