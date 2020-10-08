import { urlButton, callbackButton } from 'telegraf/markup'
import apiService from '../../services/api'

import { ACTIONS } from '../../constants'
import { balanceText } from '../../texts'

const BalanceButtons = {
  reply_markup: {
    inline_keyboard: [
      [urlButton('Купить монеты', 'http://vuvedimenya.schas'), callbackButton('Вывести деньги', ACTIONS.WITHDRAW)],
      [callbackButton(`👈 Назад`, ACTIONS.MAIN)]
    ]
  }
}

export default async (ctx) => {
  const balance = await apiService.getUserBalance(ctx.from.id)
  ctx.reply(balanceText(balance), BalanceButtons);
}