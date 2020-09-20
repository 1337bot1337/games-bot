export const startText = 'Добро пожаловать в LuckySevenBot.\nУ нас можно играть в настоящие деньги и выигрывать кучу игр'

export const mainText = (balance) => (`
Выбирай игру. Играй. Выводи деньги себе на счет.\n
${balanceText(balance)}`)

export const balanceText = (balance) => (`
💼Твой баланс:
Монет: ${'balance.coins'}
Бонусных монет: ${'balance.bonus'}`)

export const gameListText = 'Список доступных игр. Нажми на выбранную, чтобы перейти'

export const withdrawAmountText = 'Введите сумму, которую хотите вывести'

export const withdrawCardText = 'Введите номер карты (16 цифр на лицевой стороне вашей карты)'

export const withdrawReadyText = 'Спасибо, запрос будет обработан в ближайшее время'

export const inviteText = 'и я приглашаем тебя присоединиться к нам, будем косить бабло вместе'

export const errorText = 'Что-то пошло не так. Попробуйте позже'

