import axios from 'axios'

console.log(process.env.VUE_APP_BASE_API_URL)
const api = axios.create({
    baseURL: process.env.VUE_APP_BASE_API_URL,
})

export default api