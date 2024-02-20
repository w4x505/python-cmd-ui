from cmd_ui.interface import Interface

def test():
    interface = Interface([
        'Сатана', 
        'Могила', 
        'Кладбище', 
        'Кожаная куртка', 
        'Кожаные штаны', 
        'Хеви метал'
    ], 'Меню на взлом денег')

    print('hello satana')

    interface.control.start_tracking_keys()
