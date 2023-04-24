# Привет, Влад!(в комментах к ревью было про то что можно писать в личку,
# но я не понял как).
# Хотел сказать спасибо за понятное ревью и то что все- таки заставил понять
# датаклассес, эсдикт и немного про обработку ошибок
# Коммент удалю, проект перепушу)


from dataclasses import dataclass, asdict
from typing import List


@dataclass
class InfoMessage:
    training_type: str
    duration: int
    distance: float
    speed: float
    calories: float

    MESSAGE = ('Тип тренировки: {training_type}; '
               'Длительность: {duration:.3f} ч.; '
               'Дистанция: {distance:.3f} км; '
               'Ср. скорость: {speed:.3f} км/ч; '
               'Потрачено ккал: {calories:.3f}. ')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Basic training class."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    M_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: int,
                 weight: int,
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
        print('Method is not specified for the class')
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Return info message about training."""
        training_type = self.__class__.__name__
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()

        return InfoMessage(training_type, self.duration,
                           distance, speed, calories)


class Running(Training):
    """Type of training: running."""
    CAL_COEF_MULTI: int = 18
    CAL_COEF_SHIFT: float = 1.79

    def get_spent_calories(self):
        return ((self.CAL_COEF_MULTI * super().get_mean_speed()
                 + self.CAL_COEF_SHIFT) * self.weight
                / super().M_IN_KM * (self.duration * self.M_IN_H))


class SportsWalking(Training):
    """Type of training: sports walking."""
    S_WALK_COEF_1: float = 0.035
    S_WALK_COEF_2: float = 0.029
    SM_IN_M: int = 100
    KMH_IN_MS: float = 0.278

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_mean_speed(self) -> float:
        """Get mean speed in kilometers per hour."""
        return self.action * super().LEN_STEP / self.duration / super().M_IN_KM

    def get_spent_calories(self):
        duration_in_m = self.duration * super().M_IN_H
        speed_in_ms = self.get_mean_speed() * self.KMH_IN_MS

        return ((self.S_WALK_COEF_1 * self.weight + ((speed_in_ms ** 2)
                / (self.height / self.SM_IN_M)) * self.S_WALK_COEF_2
            * self.weight) * duration_in_m)


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
    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.SWIM_COEF_SHIFT)
                * self.SWIM_COEF_MULTI * self.weight * self.duration)


def read_package(workout_type: str, data: List[int]) -> Training:
    """Read data received from the sensors."""
    training_type_dict = {'SWM': Swimming,
                          'RUN': Running,
                          'WLK': SportsWalking}
    current_training = training_type_dict.get(workout_type)
    if current_training is None:
        print(TypeError('uncorrect training type'))
    else:
        return current_training(*data)


def main(training: Training) -> None:
    try:
        info = training.show_training_info()
        message = info.get_message()
        print(message)
    except Exception:
        print(Exception('moving on to the next package'))


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
