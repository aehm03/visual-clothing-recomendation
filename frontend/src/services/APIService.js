import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://localhost:5000/',
  withCredentials: false
}
)

export default {
  detect (file) {
    return apiClient.post('api/detect',
      file,
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
    )
  },
  match (product) {
    return apiClient.post('api/match', product)
  },
  getProduct (id) {
    return apiClient.get('api/product/' + id)
  }
}
