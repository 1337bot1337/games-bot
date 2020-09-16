import axios from 'axios'

export default axios.create({
  baseURL: 'http://135.181.35.252/api/v1/'
})