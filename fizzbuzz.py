for number in range(1,16):
    if number%3==0 and number%5==0:
        print("fizzbuzz")

    if number%3==0:
        print("fizz")

    if number%5==0:
        print("buzz")

    else:
        print(number)
