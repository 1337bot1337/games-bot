import Stage, { leave } from 'telegraf/stage'
import Scene from 'telegraf/scenes/base'
import { inlineKeyboard, callbackButton } from 'telegraf/markup'
import { markup } from 'telegraf/extra'

import { SCENE, ACTIONS } from '../../constants'
import { withdrawAmountText, withdrawCardText, withdrawReadyText, errorText } from '../../texts'
import apiService from '../../services/api'

const echoScene = new Scene(SCENE.WITHDRAW_AMOUNT)
echoScene.enter((ctx) => {
  console.log(ctx);
  ctx.reply(withdrawAmountText)
})
echoScene.on('text', (ctx) => {
  ctx.session.amount = Number(ctx.message.text)
  ctx.scene.enter(SCENE.WITHDRAW_CARD)
})

const toMain = inlineKeyboard([
  callbackButton('На главную', ACTIONS.MAIN)
])

const withdrawScene = new Scene(SCENE.WITHDRAW_CARD)
withdrawScene.enter((ctx) => ctx.reply(withdrawCardText))
withdrawScene.leave(async({from, session, reply}) => {
  try {
    await apiService.postWithdrawRequest(from.id, session.amount, session.card)
    reply(withdrawReadyText, markup(toMain))
  } catch(e) {
    console.log(e)
    reply(errorText)
  }
})
withdrawScene.on('text', async (ctx) => {
  // [0-9]{16}
  ctx.session.card = ctx.message.text
  await ctx.scene.leave()
})

export const withdrawStage = new Stage([withdrawScene, echoScene], { ttl: 120 })