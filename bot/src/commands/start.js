import apiService from '../services/api'

import mainBlock from './main'

import { startText } from '../texts'


export default async (ctx) => {
  try {
    await apiService.postUserWithSource(ctx.from.id, ctx.startPayload || 'none')
    ctx.reply(startText)
    mainBlock()(ctx)
  } catch (e) {
    console.log(e)
  }
}