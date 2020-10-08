import startBlock from './commands/start'
import mainBlock from './commands/main'
import helpCommand from './commands/help'

import { withdrawStage } from './commands/Balance/withdraw'
import balance from './commands/Balance/balance'
import gamesList from './commands/games'
import gameInfo from './commands/gameInfo'

import { ACTIONS, SCENE } from './constants'

import session from 'telegraf/session'

import bot from './bot'
import './broadcast'

// Middleware
bot.use(session())
bot.use(withdrawStage.middleware())
// Commands
bot.start(startBlock);
bot.help(helpCommand());
// Actions
bot.action(ACTIONS.MAIN, mainBlock({ demo: 0, rub: 0, usd: 20 }));
bot.action(ACTIONS.WITHDRAW, (ctx) => ctx.scene.enter(SCENE.WITHDRAW_AMOUNT));
bot.action(ACTIONS.GAMES, gamesList)
bot.action(new RegExp(`${ACTIONS.GAME}`), gameInfo)
bot.action(ACTIONS.BALANCE, balance)
bot.action(ACTIONS.INVITE, ctx => ctx.forwardMessage('reddsdf'))

bot.launch().then(() => console.log(`BOT started`))
