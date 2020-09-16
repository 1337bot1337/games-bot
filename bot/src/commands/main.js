import { urlButton, callbackButton } from 'telegraf/markup'

import { startText } from '../texts'
import { ACTIONS } from '../constants'

const ButtonsGroup = {
    reply_markup: {
        inline_keyboard: [
            [ callbackButton(`Игры`, ACTIONS.GAMES) ],
            [ callbackButton(`Баланс`, ACTIONS.BALANCE) ],
            [ callbackButton(`Пригласить друга`, ACTIONS.INVITE) ],
            [ callbackButton(`Английский 🇺🇸`, 'ENG') ,  callbackButton(`Русский 🇷🇺`, `RUS`) ],
            [ urlButton(`Помощь`, 'https://t.me/ee') ]
        ]
    }
}

export default (balance) => async (ctx) => {
    ctx.reply(startText(balance), ButtonsGroup)
}
