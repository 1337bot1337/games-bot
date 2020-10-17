import { inlineKeyboard, urlButton, callbackButton } from 'telegraf/markup'
import { markup } from 'telegraf/extra'
import {ApiGameErrors, errorText} from '../texts'
import { ACTIONS } from '../constants'
import apiService from '../services/api'


const realURLbutton = (url) => inlineKeyboard([
     urlButton(`Перейти в игру`, `${url}`) ])


export default async (ctx) => {
    try {
        const gameId = ctx.match.input.split('_')[1]

        const tgId = ctx.from.id
        const type_game = 'real'
        const gameInfo = await apiService.getGameInfo(gameId, type_game, tgId)
        const url = gameInfo['url']
        if (url)  {
            const bt = realURLbutton(encodeURI(url))
            ctx.reply('Жми!', markup(bt));
        } else {
            ctx.reply(ApiGameErrors[gameInfo['err_code']]);
        }
    } catch(e) {
        ctx.reply(errorText)
    }
}
