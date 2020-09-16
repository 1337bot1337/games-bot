import Stage, { leave } from 'telegraf/stage'
import Scene from 'telegraf/scenes/base'
import { inlineKeyboard, callbackButton } from 'telegraf/markup'
import { markup } from 'telegraf/extra'

import { SCENE, ACTIONS } from '../../constants'
import { withdrawAmountText, withdrawCardText, withdrawReadyText } from '../../texts'

const echoScene = new Scene(SCENE.WITHDRAW_AMOUNT)
echoScene.enter((ctx) => ctx.reply(withdrawAmountText))
echoScene.on('text', (ctx) => {
  ctx.session.amount = ctx.message.text
  ctx.scene.enter(SCENE.WITHDRAW_CARD)
  // ctx.reply('Сумма введена не корректно, сообщение должно содержать только цифры. Попробуйте еще раз.')
})

const toMain = inlineKeyboard([
  callbackButton('В начало', ACTIONS.MAIN)
])

const withdrawScene = new Scene(SCENE.WITHDRAW_CARD)
withdrawScene.enter((ctx) => ctx.reply(withdrawCardText))
withdrawScene.leave((ctx) => {
  console.log(ctx.session)
  ctx.reply(withdrawReadyText, markup(toMain))
})
withdrawScene.on('text', async (ctx) => {
  // [0-9]{16}
  ctx.session.card = ctx.message.text
  await ctx.scene.leave()
})

export const withdrawStage = new Stage([withdrawScene, echoScene], { ttl: 120 })