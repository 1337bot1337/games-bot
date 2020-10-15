import axios from 'axios'

const ax = axios.create({
  baseURL: 'https://smarted.store/api/v1/',
  headers: { 'content-type': 'application/json' }
})

const makeRequest = async (url, method = 'GET', data) => {
  const { data: responseData } = await ax({ url, method, data })
  return responseData
}

class ApiService {

  // getGameList = async () => [{id: 4343434, name: 'Игра номер как-то'},{id: 434554, name: 'Игра номер как-то 2'}]
  getGameList = async () => await makeRequest('games')

  // getGameInfo = async (id) => ({
  //   message: 'some text',
  //   buttons: [
  //     {
  //       title: 'Real Game',
  //       url: 'https://game.com'
  //     },
  //     {
  //       title: 'Demo Game',
  //       url: 'https://game.com'
  //     }
  //   ],
  //   imageUrl: 'https://avatars.mds.yandex.net/get-zen_doc/198334/pub_5b51c25567efea00a91dfd06_5b51c2969b6e4000a9e46cb3/scale_1200'
  // })
  getGameInfo = async (id) => await makeRequest(`games/${id}`)

  postUserWithSource = async (tg_id, source) => 
    await makeRequest('accounts/user/', 'POST', {
      tg_id,
      source
    })

  getUserBalance = async (id) => await makeRequest(`wallets/${id}/check/`)

  postWithdrawRequest = async (id, amount, card_number) =>
    await makeRequest(`wallets/${id}/withdraw/`, 'POST', {
      amount,
      card_number
    })
}

export default new ApiService() 