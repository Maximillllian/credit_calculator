Кредитный калькулятор. 

Работает из коммандной строки или с помощью python-интерпритатора.
По умолчанию работает на командную строку, но можно изменить на python-интерпритатор. Для этого
в конце кода измените calculator_cli() на calculator_py()

Может считать дифферинцированный и аннуитентный тип платежей. Если указан аннуитентный, то помимо
размера платежа умеет считать период и тело кредита.

Если выбран режим командной строки, вам нужно указать следующие параметры: 

    --type=annuity или diff --periods=
    --principal=...(int)
    --interest=...(float)
    --payment=...(int) 
  
Если тип дифференцированный, указывайте все, кроме --payment. Если annuity - указывайте все, кроме параметра, который хотите посчитать

Если выбран режим интерпритатора, просто следуйте инструкциям
