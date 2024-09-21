class RICE:
    """
    Класс для приоритизации RICE (Reach, Impact, Confidence, Effort).
    """

    def __init__(self, reach: float, impact: float, confidence: float, effort: float):
        """
        Инициализация параметров RICE.

        :param reach: Сколько людей или сегментов затронет проект.
        :param impact: Насколько сильно повлияет проект (оценка от 1 до 5).
        :param confidence: Уверенность в оценках reach и impact (процент от 0 до 100).
        :param effort: Количество усилий (в человеко-месяцах или других единицах), необходимых для реализации проекта.
        """
        self.reach = reach
        self.impact = impact
        self.confidence = confidence / 100  # Преобразуем процент в десятичную дробь
        self.effort = effort

    def calculate_rice_score(self) -> float:
        """
        Рассчитывает RICE score.

        :return: RICE score
        """
        rice_score = (self.reach * self.impact * self.confidence) / self.effort
        return rice_score


class ICE:
    """
    Класс для приоритизации ICE (Impact, Confidence, Effort).
    """

    def __init__(self, impact: float, confidence: float, effort: float):
        """
        Инициализация параметров ICE.

        :param impact: Насколько сильно повлияет проект (оценка от 1 до 10).
        :param confidence: Уверенность в оценках impact (процент от 0 до 100).
        :param effort: Количество усилий (в человеко-месяцах или других единицах), необходимых для реализации проекта.
        """
        self.impact = impact
        self.confidence = confidence / 100  # Преобразуем процент в десятичную дробь
        self.effort = effort

    def calculate_ice_score(self) -> float:
        """
        Рассчитывает ICE score.

        :return: ICE score
        """
        ice_score = (self.impact * self.confidence) / self.effort
        return ice_score


class Kano:
    """
    Класс для анализа приоритизации на основе модели Kano.
    """

    def __init__(self):
        """
        Инициализация модели Kano.
        """
        self.kano_categories = {
            'Must-have': [],
            'One-dimensional': [],
            'Attractive': [],
            'Indifferent': [],
            'Reverse': []
        }

    def add_feature(self, feature_name: str, customer_satisfaction: int, functionality: int):
        """
        Добавление функциональности на основе анализа Kano.

        :param feature_name: Название функциональности.
        :param customer_satisfaction: Оценка удовлетворения пользователей (от -1 до 1, где -1 — недовольны, 0 — индифферентно, 1 — довольны).
        :param functionality: Оценка функциональности (от -1 до 1, где -1 — отрицательно, 0 — нейтрально, 1 — положительно).
        """
        if customer_satisfaction == 1 and functionality == 1:
            self.kano_categories['One-dimensional'].append(feature_name)
        elif customer_satisfaction == 1 and functionality == 0:
            self.kano_categories['Attractive'].append(feature_name)
        elif customer_satisfaction == 0 and functionality == 0:
            self.kano_categories['Indifferent'].append(feature_name)
        elif customer_satisfaction == 1 and functionality == -1:
            self.kano_categories['Must-have'].append(feature_name)
        elif customer_satisfaction == -1 and functionality == 1:
            self.kano_categories['Reverse'].append(feature_name)

    def get_features_by_category(self, category: str) -> list:
        """
        Возвращает список функциональностей по категории Kano.

        :param category: Категория (Must-have, One-dimensional, Attractive, Indifferent, Reverse).
        :return: Список функциональностей в данной категории.
        """
        return self.kano_categories.get(category, [])
