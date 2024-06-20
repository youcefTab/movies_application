import axios from 'axios'

const BASE_API_URL = process.env.BASE_API_URL

const api = axios.create({
    baseURL: BASE_API_URL,
})

export default api