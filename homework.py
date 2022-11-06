class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,  # имя класса тренировки
                 duration: float,  # длительность тренировки в часах
                 distance: float,  # дистанция в километрах, за тренировку
                 speed: float,  # средняя скорость, пользователя
                 calories: float  # количество израсходованных килокалорий
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        duration_formatted = '%.3f' % round(self.duration, 3)
        distance_formatted = '%.3f' % round(self.distance, 3)
        speed_formatted = '%.3f' % round(self.speed, 3)
        calories_formatted = '%.3f' % round(self.calories, 3)

        return (f'Тип тренировки: {self.training_type}; Длительность: '
                + f'{duration_formatted} ч.; '
                + f'Дистанция: {distance_formatted} км; Ср. '
                + f'скорость: {speed_formatted} км/ч; Потрачено ккал: '
                + f'{calories_formatted}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65  # default расстояние за шаг
    M_IN_KM = 1000  # константа для перевода значений из метров в километры
    CM_IN_M = 100  # константа для перевода длины в метры
    MIN_IN_H = 60  # константа для перевода времени в минуты

    def __init__(self,
                 action: int,  # количество совершённых действий
                 duration: float,  # длительность тренировки
                 weight: float,  # вес спортсмена
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    LEN_STEP = 0.65  # расстояние, которое спортсмен преодолевает за один шаг
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    LEN_STEP = 0.65  # расстояние, которое спортсмен преодолевает за один шаг
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    KMH_IN_MSEC = 0.278

    def __init__(self,
                 action: int,  # количество совершённых действий
                 duration: float,  # длительность тренировки
                 weight: float,  # вес спортсмена
                 height: float  # рост спортсмена
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + ((self.get_mean_speed() * self.KMH_IN_MSEC)**2
                 / (self.height / self.CM_IN_M))
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight)
                * self.duration * self.MIN_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38  # расстояние, которое преодолеваемое за один гребок
    CALORIES_WEIGHT_MULTIPLIER = 2
    CALORIES_MEAN_SPEED_SHIFT = 1.1

    def __init__(self,
                 action: int,  # количество совершённых действий
                 duration: float,  # длительность тренировки
                 weight: float,  # вес спортсмена
                 length_pool: float,  # рост спортсмена
                 count_pool: float  # рост спортсмена
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_classes = {'SWM': (lambda: Swimming(*data)),
                        'RUN': (lambda: Running(*data)),
                        'WLK': (lambda: SportsWalking(*data))}
    return training_classes[workout_type]()


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
