# Кредитный калькулятор. Работает из коммандной строки или с помощью python-интерпритатора.
# По умолчанию работает на командную строку, но можно изменить на python-интерпритатор. Для этого
# в конце кода измените calculator_cli() на calculator_py()

# Может считать дифферинцированный и аннуитентный тип платежей. Если указан аннуитентный, то помимо
# размера платежа умеет считать период и тело кредита.

# Если выбран режим командной строки, вам нужно указать следующие параметры: --type=annuity или
# diff. --periods=, --principal=, --interest=, --payment=. Если тип дифференцированный, указывайте
# все, кроме --payment. Если annuity - указывайте все, кроме параметра, который хотите посчитать

# Если выбран режим интерпритатора, просто следуйте инструкциям

import math
import argparse
import sys


# Функция калькулятора на интерепритаторе


def calculator_py():
    print('''Do you want to calculate a differentiated payment or an annuity?
type a - for annuity
type d - for differentiated''')
    payment_type = input()
    if payment_type == 'd':
        credit_principal = int(input('Enter credit principal:\n'))
        count_periods = int(input('Enter count of period:\n'))
        credit_interest = float(input('Enter credit interest:\n'))
        credit_payments = diff_payment(credit_principal, credit_interest, count_periods)
        for num, pay in enumerate(credit_payments, 1):
            print(f'Month {num}: paid out {pay}')
    else:
        print('''What do you want to calculate? 
type "n" - for count of months, 
type "a" - for annuity monthly payment,
type "p" - for credit principal: ''')
        option = input()
        if option == 'n':
            credit_principal = int(input('Enter credit principal:\n'))
            credit_payment = int(input('Enter monthly payment:\n'))
            credit_interest = float(input('Enter credit interest:\n'))
            count_years, count_month = month_calculate(credit_principal,
                                                       credit_payment,
                                                       credit_interest)
            if int(count_month) == 0:
                print(f'You need {count_years} years to repay this credit!')
            else:
                print(f'You need {count_years} years and {count_month} months'
                      f' to repay this credit!')
        elif option == 'a':
            credit_principal = int(input('Enter credit principal:\n'))
            count_periods = int(input('Enter count of period:\n'))
            credit_interest = float(input('Enter credit interest:\n'))
            credit_payment = annuity_payment(credit_principal,
                                             count_periods,
                                             credit_interest)
            if isinstance(credit_payment, list):
                print(f'Your annuity payment = {credit_payment[0]} with '
                      f'last annuity payment = {credit_payment[1]}.')
            else:
                print(f'Your annuity payment = {credit_payment}')
        elif option == 'p':
            monthly_payment = float(input('Enter monthly payment:\n'))
            count_periods = int(input('Enter count of period:\n'))
            credit_interest = float(input('Enter credit interest:\n'))
            credit_principal = principal_calculate(monthly_payment,
                                                   count_periods,
                                                   credit_interest)
            print(f'Your credit principal = {credit_principal}!')


# Функция кулькулятора из коммандной строки


def calculator_cli(p_args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='Кредитный калькулятор')
    parser.add_argument('--type',
                        help='Введите тип платежа: annuity или diff')
    parser.add_argument('--payment',
                        type=float,
                        help='Если аннуентные платежи, то укажите сумму платежа. '
                             'Если дифференцированный, не указывайте ничего')
    parser.add_argument('--principal',
                        type=float,
                        help='Введине тело кредита')
    parser.add_argument('--interest',
                        type=float,
                        help='Введите процентную ставку')
    parser.add_argument('--periods',
                        type=int,
                        help='Введите количество периодов, за которые кредит должен'
                             'погаситься')
    args = parser.parse_args(p_args)
    # Создали список из числовых значений аргументов, чтоб ниже проверить на отрицательные значения
    num_args = [args.payment, args.interest, args.periods, args.principal]
    num_args = [i for i in num_args if i]

    # Здесь прописаны ограничения для поступивших аргументов (их должно быть 4; при дифференцированном типе не должно
    # быть указан платеж; должен быть указан процент; не должно быть отицательных значений
    if len(p_args) != 4 or (args.type == 'diff' and args.payment) or not args.interest \
            or any(i <= 0 for i in num_args):
        print('Incorrect parameters')

    # Исключили отрицательные значения, теперь переходим к вычислениям
    else:
        if args.type == 'diff':
            payments = diff_payment(args.principal, args.interest,
                                    args.periods)
            for num, pay in enumerate(payments, 1):
                print(f'Month {num}: paid out {pay}')
            print(f'Overpayment = {sum(payments) - args.principal}')
        else:
            if not args.payment:
                credit_payment = annuity_payment(args.principal,
                                                 args.periods,
                                                 args.interest)
                print(f'Your annuity payment = {credit_payment}')
                print(f'Overpayment = {credit_payment * args.periods - args.principal}')
            elif not args.principal:
                credit_principal = principal_calculate(args.payment,
                                                       args.periods,
                                                       args.interest)
                print(f'Your credit principal = {credit_principal}!')
                print(f'Overpayment = {args.payment * args.periods - credit_principal}')
            elif not args.periods:
                count_years, count_month = month_calculate(args.principal,
                                                           args.payment,
                                                           args.interest)
                if int(count_month) == 0:
                    print(f'You need {count_years} years to repay this credit!')
                else:
                    print(f'You need {count_years} years and {count_month} months'
                          f' to repay this credit!')
                print(f'Overpayment = '
                      f'{args.payment * (count_years * 12 + count_month) - args.principal}')


def diff_payment(principal, interest, periods):
    payments = []
    interest = interest / (12 * 100)
    for i in range(1, periods + 1):
        d = principal / periods + interest * (principal - (principal * (i - 1)) / periods)
        payments.append(math.ceil(d))
    return payments


def annuity_payment(principal, periods, interest):
    i = interest / (12 * 100)
    A = principal * ((i * (1 + i) ** periods) / ((1 + i) ** periods - 1))
    A = math.ceil(A)
    last_payment = principal - (periods - 1) * A
    return A


def month_calculate(principal, payment, interest):
    i = interest / (12 * 100)
    n = math.log(payment / (payment - i * principal), 1 + i)
    n = math.ceil(n)
    years = n // 12
    months = n % 12
    return years, months


def principal_calculate(payment, period, interest):
    i = interest / (12 * 100)
    credit_principal = payment / ((i * (1 + i) ** period) / ((1 + i) ** period - 1))
    return math.ceil(credit_principal)


if __name__ == '__main__':
    calculator_cli()
