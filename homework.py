class InfoMessage:
    """Info message about training"""
    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration}; '
                f'Дистанция: {self.distance}; '
                f'Ср. скорость: {self.speed}; '
                f'Потрачено ккал: {self.calories}'
                )


class Training:
    """Basic training class."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    M_IN_H: int = 60
    SM_IN_M: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Get distance in km."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Get mean speed of movement."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Get count of calories spent on training ."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Return info message about training."""
        training_type = self.__class__.__name__
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = round(self.get_spent_calories(), 3)

        return InfoMessage(training_type, self.duration,
                           distance, speed, calories)


class Running(Training):
    """Type of training: running."""
    CAL_COEF_MULTI: int = 18
    CAL_COEF_SHIFT: float = 1.79

    def __init__(self, action, duration, weight):
        super().__init__(action, duration, weight)

    def get_spent_calories(self):
        return ((self.CAL_COEF_MULTI * super().get_mean_speed()
                 + self.CAL_COEF_SHIFT) * self.weight
                / super().M_IN_KM * (self.duration * self.M_IN_H))


class SportsWalking(Training):
    """Type of training: sports walking."""
    S_WALK_COEF_1: float = 0.035
    S_WALK_COEF_2: float = 0.029
    KMH_IN_MS = 0.278

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_mean_speed(self) -> float:
        """Get mean speed in meters per second."""
        return self.action * super().LEN_STEP * self.KMH_IN_MS

    def get_spent_calories(self):
        height_in_m = self.height / super().SM_IN_M
        duration_in_m = self.duration / super().M_IN_H
        return ((self.S_WALK_COEF_1 * self.weight + (self.get_mean_speed ** 2
                / height_in_m) * self.S_WALK_COEF_2 * self.weight)
                * duration_in_m)


class Swimming(Training):
    """Type of training: swimming."""
    LEN_STEP: float = 1.38
    SWIM_COEF_SHIFT: float = 1.1
    SWIM_COEF_MULTI: int = 2

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.lenght_pool: int = length_pool
        self.count_pool: int = count_pool

    """Redefining method of obtaining distance for swimming."""
    def get_distance(self) -> float:
        """Get distance in km."""
        return self.action * self.LEN_STEP / super().M_IN_KM

    """Redefining method of obtaining mean speed for swimming."""
    def get_mean_speed(self) -> float:
        """Get distance in km."""
        return (self.lenght_pool * self.count_pool
                / super().M_IN_KM / self.duration)

    """Redefining method of obtaining spent calories for swimming"""
    def get_spent_calories(self):
        return ((self.get_mean_speed() + self.SWIM_COEF_SHIFT)
                * self.SWIM_COEF_MULTI * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Read data received from the sensors."""
    training_type_dict = {'SWM': Swimming,
                          'RUN': Running,
                          'WLK': SportsWalking}
    return training_type_dict[workout_type](*data)


def main(training: Training) -> None:
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
