require("dotenv").config();
const { BOT_TOKEN } = process.env;
import Telegraf from 'telegraf'

const bot = new Telegraf(BOT_TOKEN)

export default bot

