import { inlineKeyboard, urlButton, callbackButton } from 'telegraf/markup'
import { markup } from 'telegraf/extra'
import { errorText } from '../texts'
import { ACTIONS } from '../constants'
import { gameInfoText } from '../texts'
import apiService from '../services/api'

//const gamesBtnGenerator = (buttons) => inlineKeyboard([
//    ...buttons.map(({ title, url }) => urlButton(title, url)),
//    callbackButton('Назад', ACTIONS.GAMES)
//], { columns: 1 })
//
//export default async (ctx) => {
//    try {
//        const gameId = ctx.match.input.split('_')[1]
//        const { message, buttons, imageUrl } = await apiService.getGameInfo(gameId)
//        ctx.reply(`${message}\n\n${imageUrl}`, markup(gamesBtnGenerator(buttons)));
//    } catch(e) {
//        ctx.reply(errorText)
//    }
//}

const gameBtnGenerator = (id) => inlineKeyboard([
    callbackButton(`Играть на демо фантики`, `${ACTIONS.DEMO_GAME}_${id}`),
    callbackButton(`Играть на реальные фантики`, `${ACTIONS.REAL_GAME}_${id}`),
    callbackButton('Назад', ACTIONS.MAIN)
],  { columns: 1 })


export default async (ctx) => {
    try {
        const gameId = ctx.match.input.split('_')[1]
        const tgId = ctx.from.id
        const buttons = gameBtnGenerator(gameId)
        ctx.reply(gameInfoText, markup(buttons));
    } catch(e) {
        ctx.reply(errorText)
    }
}
