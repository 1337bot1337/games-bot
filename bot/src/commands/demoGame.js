import { inlineKeyboard, urlButton, callbackButton } from 'telegraf/markup'
import { markup } from 'telegraf/extra'
import { errorText } from '../texts'
import { ACTIONS } from '../constants'
import { ApiGameErrors } from '../texts'
import apiService from '../services/api'


const demoURLbutton = (url) => inlineKeyboard([
     urlButton(`Перейти в игру`, `${url}`) ])


export default async (ctx) => {
    try {
        const gameId = ctx.match.input.split('_')[1]
        const tgId = ctx.from.id
        const type_game = 'demo'
        const gameInfo = await apiService.getGameInfo(gameId, type_game, tgId)
        const url = gameInfo['url']
        if (url)  {
            const bt = demoURLbutton(encodeURI(url))
            ctx.reply('Жми!', markup(bt));
        } else {
            ctx.reply(ApiGameErrors[gameInfo['err_code']]);
        }
    } catch(e) {
        ctx.reply(errorText)
    }
}
