require("dotenv").config();
const { BOT_TOKEN } = process.env;

import Telegraf from 'telegraf'
// import apiService from './services/api'

import mainView from './commands/main'
import helpCommand from './commands/help'

import { withdrawStage } from './commands/Balance/withdraw'
import balance from './commands/Balance/balance'
import gameList from './commands/games'

import { ACTIONS, SCENE } from './constants'

import session from 'telegraf/session'

import Stage from 'telegraf/stage'
const { enter, leave } = Stage

const init = async (bot) => {
    // Middleware
    bot.use(session())
    bot.use(withdrawStage.middleware())
    // Commands
    bot.start(mainView({ demo: 0, rub: 0, usd: 20 }));
    bot.help(helpCommand());
    // Actions
    bot.action(ACTIONS.MAIN, mainView({ demo: 0, rub: 0, usd: 20 }));
    bot.action(ACTIONS.WITHDRAW, (ctx) => ctx.scene.enter(SCENE.WITHDRAW_AMOUNT));
    bot.action(ACTIONS.GAMES, gameList())
    bot.action(ACTIONS.BALANCE, balance())

    return bot;
}

init(new Telegraf(BOT_TOKEN)).then(async (bot) => {
    await bot.launch();
    console.log(`Launched ${new Date()}`);
});
