// import axios from 'axios'
import fetch from 'node-fetch'

// const ax = axios.create({
//   baseURL: 'https://push.money/api/v1/',
//   headers: { 'content-type': 'application/json' }
// })

const baseURL = 'https://push.money/api/v1/'
const headers = { 'Content-Type': 'application/json' }

const makeRequest = async (route, method = 'GET', data) => {
  const initObj = {
    method,
    headers
  }
  if(data) initObj.body = JSON.stringify(data)
  console.log(initObj)
  return fetch(`${baseURL}${route}`, initObj)
    // .then(res => res.json())
    .then(res => console.log(res))
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