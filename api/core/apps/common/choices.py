from django.utils.translation import gettext_lazy as _


class TransactionKind:
    REPLENISHMENT = "replenishment"
    WITHDRAW = "withdraw"
    GAME_STARTED = "game_started"
    GAME_FINISHED = "game_finished"


TRANSACTION_KIND_CHOICES = (
    (TransactionKind.REPLENISHMENT, _("Replenishment")),
    (TransactionKind.WITHDRAW, _("Withdraw")),
    (TransactionKind.GAME_STARTED, _("Game started")),
    (TransactionKind.GAME_FINISHED, _("Game finished")),
)


class TransactionStatus:
    IN_PROGRESS = 'in_progress'
    DONE = 'done'


TRANSACTION_STATUS_CHOICES = (
    (TransactionStatus.IN_PROGRESS, _("Transaction in progress")),
    (TransactionStatus.DONE, _("Transaction done")),
)


class WithdrawRequestStatus:
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    IN_PROGRESS = "in_progress"


WITHDRAW_REQUEST_STATUS_CHOICES = (
    (WithdrawRequestStatus.ACCEPTED, _("Запрос на снятие средств выполнен")),
    (WithdrawRequestStatus.REJECTED, _("Запрос на снятие средств отклонен")),
    (WithdrawRequestStatus.IN_PROGRESS, _("Запрос на снятие средств выполняется")),
)


class RefillStatus:
    IN_PROGRESS = 'in_progress'
    SUCCEED = 'succeed'
    FAILED = 'failed'


REFILL_STATUS_CHOICES = (
    (RefillStatus.IN_PROGRESS, _("Refill in progress")),
    (RefillStatus.SUCCEED, _("Refill succeed")),
    (RefillStatus.FAILED, _("Refill failed")),
)

