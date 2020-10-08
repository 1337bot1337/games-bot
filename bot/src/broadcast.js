import kue from 'kue'

import bot from './bot'
import app from './express'

app.post('/api/v1/send', (req, res) => {
  // TODO: Implement kue
  const messages = req.body
  const interval = setInterval(async () => {
    try {
      const { chatId, message } = messages.shift()
      bot.telegram.sendMessage(chatId, message)
      if(!messages.lenght) clearInterval(interval)
    } catch(e) {
      console.log(e)
    }
  }, 50)
  res.status(201).send({status: 'Messages was added to queue'})
})
