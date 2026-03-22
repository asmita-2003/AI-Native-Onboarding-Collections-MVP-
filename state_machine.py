from enum import Enum
from datetime import datetime


class State(Enum):
    D15 = "D-15"
    D7 = "D-7"
    D1 = "D-1"
    D0 = "DUE"
    D1_PLUS = "D+1"
    D3 = "D+3"
    CLOSED = "CLOSED"
    ESCALATED = "ESCALATED"


class Loan:
    def __init__(self, borrower):
        self.borrower = borrower
        self.state = State.D15
        self.paid = False
        self.dispute = False


def log(event, state):
    print(f"{datetime.now()} | {state.value} | {event}")


def transition(loan):
    if loan.paid:
        loan.state = State.CLOSED
        log("payment_received", loan.state)
        return

    if loan.dispute:
        loan.state = State.ESCALATED
        log("dispute_escalated", loan.state)
        return

    if loan.state == State.D15:
        log("send_reminder", loan.state)
        loan.state = State.D7

    elif loan.state == State.D7:
        log("whatsapp_reminder", loan.state)
        loan.state = State.D1

    elif loan.state == State.D1:
        log("urgent_sms_email", loan.state)
        loan.state = State.D0

    elif loan.state == State.D0:
        log("due_today_notice", loan.state)
        loan.state = State.D1_PLUS

    elif loan.state == State.D1_PLUS:
        log("grace_call", loan.state)
        loan.state = State.D3

    elif loan.state == State.D3:
        log("trigger_voice_agent", loan.state)


def simulate(scenario):
    loan = Loan("Ramesh")

    if scenario == "pays_on_time":
        loan.paid = True

    elif scenario == "disputes":
        loan.dispute = True

    while loan.state not in [State.CLOSED, State.ESCALATED]:
        transition(loan)


if __name__ == "__main__":
    simulate("delinquent")
