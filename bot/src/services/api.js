import axios from 'axios'

const ax = axios.create({
  baseURL: 'https://push.money/api/v1/',
  headers: { 'content-type': 'application/json' }
})

const makeRequest = async (url, method = 'GET', data) => {
  const { data: responseData } = await ax({ url, method, data })
  return responseData
}

class ApiService {

  getGameList = async () => await makeRequest('games')

  postUserWithSource = async (tg_id, source) => 
    await makeRequest('accounts/user/', 'POST', {
      tg_id: 10101010,
      source: 'Space'
    })

  getUserBalance = async (id) => await makeRequest(`wallets/${id}/check/`)

  postWithdrawRequest = async (id, amount, card_number) =>
    await makeRequest(`wallets/${id}/withdraw/`, 'POST', {
      amount: 0,
      card_number: "1111 1111 1111 1111"
    })
}

export default new ApiService() 