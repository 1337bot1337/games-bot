import startBlock from './commands/start'
import mainBlock from './commands/main'
import helpCommand from './commands/help'

import { withdrawStage } from './commands/Balance/withdraw'
import balance from './commands/Balance/balance'
import gameList from './commands/games'

import { ACTIONS, SCENE } from './constants'

import session from 'telegraf/session'

import bot from './bot'

// Middleware
bot.use(session())
bot.use(withdrawStage.middleware())
// Commands
bot.start(startBlock);
bot.help(helpCommand());
// Actions
bot.action(ACTIONS.MAIN, mainBlock({ demo: 0, rub: 0, usd: 20 }));
bot.action(ACTIONS.WITHDRAW, (ctx) => ctx.scene.enter(SCENE.WITHDRAW_AMOUNT));
bot.action(ACTIONS.GAMES, gameList())
bot.action(ACTIONS.BALANCE, balance())
bot.action(ACTIONS.INVITE, ctx => ctx.forwardMessage('reddsdf'))

bot.launch().then(() => console.log(`Launched ${new Date()}`))
