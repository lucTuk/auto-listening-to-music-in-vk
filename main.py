import random
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class AuLi:
    def __init__(self, email, password):
        options = webdriver.FirefoxOptions()

        # Определяем user agent, чтобы вк думал, что мы заходим с мобильного устройства
        options.set_preference('general.useragent.override', 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F '
                                                             'Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) '
                                                             'Chrome/62.0.3202.84 Mobile Safari/537.36')
        self.driver = webdriver.Firefox('.', options=options)
        self.domain = 'https://vk.com/'
        self.email = email
        self.password = password

    @staticmethod
    def random_sleep():
        """Метод для рандомного засыпания, чтобы страница успевела прогрузиться"""
        time_sleep = int(random.randint(6, 10))
        sleep(time_sleep)

    @staticmethod
    def minutes_to_seconds(durations: list):
        """Метод переводящая формат времени MM:SS в секунды"""
        total = 0
        for duration in durations:
            total += int(duration.split(':')[0]) * 60 + int(duration.split(':')[1])
        return total

    def close_browser(self):
        """Метод объеденяющая методы драйвера close() и quit() для закрытия браузера после непредвиденной ошибки"""
        driver = self.driver
        driver.close()
        driver.quit()

    def auth(self):
        """Метод для авторизация в вк"""
        driver = self.driver

        try:
            driver.get(self.domain)
            self.random_sleep()

            # Получаем input'ы поля email, для ввода email/номера телефона и поля pass, для ввода пароля
            email_input = driver.find_element_by_name('email')
            password_input = driver.find_element_by_name('pass')

            email_input.clear()
            password_input.clear()
            self.random_sleep()

            email_input.send_keys(self.email)
            password_input.send_keys(self.password)
            self.random_sleep()

            password_input.send_keys(Keys.ENTER)
            self.random_sleep()

            # Если на аккаунти есть двухфакторка
            if driver.find_elements_by_id('authcheck_code'):
                authcheck_code = input('Пожалуйста, введите код из личного сообщения от Администрации или из '
                                       'приложения для генерации кодов, чтобы подтвердить, что Вы владелец '
                                       'страницы: ')

                send = driver.find_element_by_id('authcheck_code')
                send.send_keys(authcheck_code)
                send.send_keys(Keys.ENTER)
                sleep(20000)

        except Exception as e:
            print(e)
            self.close_browser()

    def album_listening(self, album_link: str, count=1):
        """Метод для прослушивания альбома. А то б###ь не понятно)"""

        # Оптимизируем ссылку для мобильной версии вк
        if 'z=' in album_link:
            act = album_link.split('z=')[1].split('%')[0]
            album_link = f'https://m.vk.com/audio?act={act}'

        elif 'act=' in album_link:
            pass

        # Авторизируемся вк
        self.auth()

        driver = self.driver

        try:
            driver.get(album_link)
            self.random_sleep()

            # Определяем сколько секунд потребуется, чтобы прослушать весь альбом
            durations = [duration.text for duration in driver.find_elements_by_class_name('ai_dur')]
            self.random_sleep()

            # Общую продолжительность альбома умножаем на кол-во раз прослушиваний и прибамляем погрешность в 300
            # секунд на рекламы. Если у вас платная подписка на музыку вк, можете уменьшеть погрешность.
            time_sleep = (self.minutes_to_seconds(durations) * count) + 300

            driver.find_element_by_class_name('audioPlaylist__play').click()
            sleep(time_sleep)

            print('Готово!')

        except Exception as e:
            print(e)
            self.close_browser()
        finally:
            self.close_browser()
