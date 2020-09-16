import { inlineKeyboard, urlButton, callbackButton } from 'telegraf/markup'
import { markup } from 'telegraf/extra'
import { ACTIONS } from '../constants'
import { gameListText } from '../texts'

const games = inlineKeyboard([
    urlButton('Monik', 'http://slonik.ua'),
    urlButton('Bonik', 'http://slonik.ua'),
    urlButton('Finik', 'http://slonik.ua'),
    urlButton('Konik', 'http://konik.ua'),
    callbackButton('Назад', ACTIONS.MAIN)
], { columns: 1 })

export default () => async (ctx) => {
    ctx.reply(gameListText, markup(games));
}
