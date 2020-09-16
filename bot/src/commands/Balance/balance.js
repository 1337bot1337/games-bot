import { urlButton, callbackButton } from 'telegraf/markup'
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

export default () => async (ctx) => {
    ctx.reply(balanceText({coins: 50, bonus: 100}), BalanceButtons);
}