import { inlineKeyboard, urlButton, callbackButton } from 'telegraf/markup'
import { markup } from 'telegraf/extra'
import { ACTIONS } from '../constants'
import { gameListText, errorText } from '../texts'

import apiService from '../services/api'

const gamesBtnGenerator = (games) => inlineKeyboard([
    ...games.map(game => {
        const keys = Object.keys(game)
        return urlButton(game[keys[0]], `http://${keys[0]}.com`)
    }),
    callbackButton('Назад', ACTIONS.MAIN)
], { columns: 1 })

export default () => async (ctx) => {
    try {
        const games = await apiService.getGameList()
        if(games.length === 0) throw Error
        const buttons = gamesBtnGenerator(games)
        ctx.reply(gameListText, markup(buttons));
    } catch(e) {
        ctx.reply(errorText)
    }
}
