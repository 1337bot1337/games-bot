import apiService from '../services/api'

import mainBlock from './main'

import { startText } from '../texts'


export default async (ctx) => {
    console.log(ctx.from)
    await apiService.addUserWithSource(ctx.from, ctx.startPayload)
    ctx.reply(startText)
    mainBlock()(ctx)
}
