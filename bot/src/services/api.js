import axios from 'axios'

const ax = axios.create({
  baseURL: 'http://push.money/api/v1/'
})

class ApiService {
  getGameList = async () => await ax('games')

  addUserWithSource = async (tg_id, source = 'none') => await ax.post('games', {
    tg_id,
    source
  })

  getUserBalance = async (id) => await ax(`wallet/check/${id}`)
}

export default new ApiService() 