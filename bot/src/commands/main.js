import { urlButton, callbackButton, switchToChatButton } from 'telegraf/markup'

import apiService from '../services/api'

import { mainText, errorText, inviteText } from '../texts'
import { ACTIONS } from '../constants'

const ButtonsGroup = {
  reply_markup: {
    inline_keyboard: [
      [ callbackButton(`Игры`, ACTIONS.GAMES) ],
      [ callbackButton(`Баланс`, ACTIONS.BALANCE) ],
      [ switchToChatButton(`Пригласить друга`, inviteText) ],
      [ callbackButton(`Английский 🇺🇸`, 'ENG') ,  callbackButton(`Русский 🇷🇺`, `RUS`) ],
      [ urlButton(`Помощь`, 'https://t.me/ee') ]
    ]
  }
}

export default (balance) => async (ctx) => {
  console.log(ctx.from);
  try {
    ctx.reply(mainText, ButtonsGroup)
  } catch(e) {
    ctx.reply(errorText)
  }
}
