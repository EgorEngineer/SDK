import datetime

class Feature:
    def __init__(self, last_feature_id: int, app: 'App'):
        self.feature_id = last_feature_id + 1
        self.app_id = app.app_id
        self.created_at = datetime.now()
    @property
    def feature_name(self):
        return self._feature_name

    @feature_name.setter
    def feature_name(self, value):
        if not isinstance(value, list):
            raise TypeError("Expected a list of characters")
        self._feature_name = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise TypeError("Expected a string")
        self._description = value

    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, value):
        if not isinstance(value, datetime):
            raise TypeError("Expected a date/time object")
        self._created_at = value

    @property
    def updated_at(self):
        return self._updated_at

    @updated_at.setter
    def updated_at(self, value):
        if not isinstance(value, datetime):
            raise TypeError("Expected a date/time object")
        self._updated_at = value

    def start_voting(self):
        votes = Votes(self)


class App:
    def __init__(self, app_id: int, app_name: int):
        self.app_id = app_id
        self.app_name = app_name


class Logs:
    def __init__(self, log_id: int, user_id: int, action: list, created_at: datetime):
        self.log_id = log_id
        self.user_id = user_id
        self.action = action
        self.created_at = created_at

class User:
    def __init__(self, email: list):
        try:
            self.user_id = sum([int(c) for c in email])
        except ValueError as e:
            raise ValueError('Email should be a valid integer sequence') from e
        else:
            self.email = email
            self.created_at = datetime.now()
            self.app_id = None

class Votes:
    def __init__(self, feature: 'Feature', user_id: int):
        self.vote_id = 0
        self.user_id = user_id
        self.feature_id = feature.feature_id
        self.created_at = datetime.now()


class Results:
    def __init__(self, result_id: int, feature_id: int, total_votes: int, positive_votes: int, negative_votes: int, last_updated: datetime):
        self.result_id = result_id
        self.feature_id = feature_id
        self.total_votes = total_votes
        self.positive_votes = positive_votes
        self.negative_votes = negative_votes
        self.last_updated = last_updated