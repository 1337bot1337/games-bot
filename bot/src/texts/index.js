export const startText = 'Добро пожаловать в LuckySevenBot.\nУ нас можно играть в настоящие деньги и выигрывать кучу игр'

export const mainText = (`Выбирай игру. Играй. Выводи деньги себе на счет.\nИли может стоит проверить свой баланс?\n\nТы в главном меню - делай выбор!`)

export const balanceText = (balance) => (`
💼Твой баланс:
Монет: {balance.real_balance}
Бонусных монет: {balance.virtual_balance}
Ожидание на вывод: {balance.withdraw_in_progress_amount}`)

export const gameListText = 'Список доступных игр. Нажми на выбранную, чтобы перейти'

export const withdrawAmountText = 'Введите сумму, которую хотите вывести'

export const withdrawCardText = 'Введите номер карты (16 цифр на лицевой стороне вашей карты)'

export const withdrawReadyText = 'Спасибо, запрос будет обработан в ближайшее время'

export const inviteText = 'и я приглашаем тебя присоединиться к нам, будем косить бабло вместе'

export const errorText = 'Что-то пошло не так. Попробуйте позже'

