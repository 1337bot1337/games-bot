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
