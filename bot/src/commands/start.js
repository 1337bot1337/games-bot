import apiService from '../services/api'

import mainBlock from './main'

import { startText } from '../texts'


export default async (ctx) => {
  try {
    await apiService.postUserWithSource(ctx.chat.id, ctx.startPayload || 'none').catch(() => console.log('e'))
    ctx.reply(startText)
    mainBlock()(ctx)
  } catch (e) {
    console.log(e)
  }
}