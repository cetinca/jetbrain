import math
import argparse


parser = argparse.ArgumentParser(description="Differentiate Payment")
parser.add_argument("--type", type=str)
parser.add_argument("--principal", type=float)
parser.add_argument("--periods", type=int)
parser.add_argument("--interest", type=float)
parser.add_argument("--payment", type=float)

args = parser.parse_args()

# args = parser.parse_args(["--type", "annuity", "--payment", "8722",
#                           "--periods", "120", "--interest", "5.6"])
# Arguments: --type=annuity --principal=1000000 --periods=8 --interest=9.8

args_dict = dict(vars(args))
_type = args.type
sum_monthly_payment = 0


def month_to_year(mon):
    years = mon // 12
    months = mon % 12
    if years == 0 and months != 0:
        return f"It will take {months} months to repay this loan!"
    elif months == 0 and years != 0:
        return f"It will take {years} years to repay this loan!"
    else:
        return f"It will take {years} years and {months} months to repay " \
               f"this " \
               f"loan!"


if args.payment is not None:
    _payment = int(args.payment)
else:
    _payment = args.payment

if args.periods is not None:
    _periods = int(args.periods)
else:
    _periods = args.periods
if args.principal is not None:
    _principal = int(args.principal)
else:
    _principal = args.principal
if args.interest is not None:
    _interest = float(args.interest) / (12 * 100)
else:
    _interest = args.interest

for k, v in args_dict.items():  # to convert dictionary
    if isinstance(v, (int, float)):
        if int(v) <= 0:
            print("Incorrect parameters")
if not (_type == "annuity" or _type == "diff"):
    print("Incorrect parameters 1")
elif _interest is None:
    print("Incorrect parameters 2")
elif _type == "diff" and _payment is not None:
    print("Incorrect parameters 3")
elif len(args_dict) < 4:
    print("Incorrect parameters 4")
elif _type == "diff":
    for m in range(1, _periods + 1):
        _payment = _principal / _periods + _interest * (_principal - (
                _principal * (m - 1)) / _periods)
        print(f"Month {m}: payment is {math.ceil(_payment)}")
        sum_monthly_payment += math.ceil(_payment)
    overpayment = sum_monthly_payment - _principal
    print(f"Overpayment = {overpayment}")
elif _type == "annuity" and _periods == None:
    n = math.log((_payment / (_payment - _interest * _principal)),
                 1 + _interest)
    n = math.ceil(n)
    overpayment = int(n * _payment - _principal)
    print(month_to_year(math.ceil(n)))
    print(f"Overpayment = {overpayment}")
elif _type == "annuity" and _principal == None:
    principal = _payment / ((_interest * (1 + _interest) ** _periods) / ((1
                                                                          +
                                                                          _interest) **
                                                                         _periods - 1))
    overpayment = int(_periods * _payment - principal)
    print(f"Your loan principal = {int(principal)}!")
    print(f"Overpayment = {overpayment}")
elif _type == "annuity" and _payment == None:
    payment = _principal * (_interest * (1 + _interest) ** _periods) / ((1 +
                                                                         _interest) **
                                                                        _periods - 1)
    overpayment = math.ceil(payment) * _periods - _principal
    print(f"Your monthly payment = {math.ceil(payment)}!")
    print(f"Overpayment = {overpayment}")
