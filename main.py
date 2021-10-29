from random import randint
from ship import Ship


comp = Ship()
comp.ship_location()
user = Ship('user')
user.ship_location()
while comp.get_err() or user.get_err():
    # print('Error')
    comp = Ship()
    comp.ship_location()
    user = Ship('user')
    user.ship_location()

# comp.print_table()
# user.print_table()
game_over = False
while not game_over:
    while not game_over:  # user step
        comp.print_table()
        user.print_table()
        coordinate = input('Ваш ход. Выберите номер строки и колонки без пробела:')
        answer = comp.set_attack(coordinate)
        # print(answer)
        if answer == 'Промах':
            print(answer)
            break
        elif answer == 'Вы попали':
            print(answer)
            game_over = comp.check_end_game()
            if game_over:
                print('Вы выиграли')
                break
            # comp.print_table()
            # user.print_table()
        elif answer == 'Вы уже сюда стреляли':
            print(answer)
        elif answer == 'error':
            print('Введите корректные данные')

    while not game_over:  # comp step
        row, column = randint(1, 6), randint(1, 6)
        # print(f'while comp row={row}, column={column}')
        answer = user.set_attack(f'{row}{column}')
        if answer == 'Промах':
            print(f'Координаты {row, column}. {answer}')
            break
        elif answer == 'Вы попали':
            print(f'Координаты {row, column}. Компьютер попал.')
            game_over = user.check_end_game()
            if game_over:
                print('Компьютер выиграл')
                break
            comp.print_table()
            user.print_table()


# тест не работает

if __name__ == '__main__':
    pass
