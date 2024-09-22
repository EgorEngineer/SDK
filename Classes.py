import datetime
class Feature:
    def init(self, last_feature_id, app):
        self.feature_id = last_feature_id + 1
        self.app_id = app.app_id
        self.created_at = datetime.datetime.now()

    def start_voting(self):
        pass

class App:
    def init(self):
        self.app_id = None
        self.app_name = None


class Logs:
    def init(self, log_id, user_id, action, created_at):
        self.log_id = log_id
        self.user_id = user_id
        self.action = action
        self.created_at = created_at


class User:
    def init(self, email):
        self.user_id = sum(ord(c) for c in email)


class Votes:
    def init(self, feature):
        self.vote_id = None
        self.user_id = None
        self.feature_id = feature.feature_id
        self.created_at = datetime.datetime.now()


class Results:
    def init(self, result_id, feature_id, total_votes, positive_votes, negative_votes, last_updated):
        self.result_id = result_id
        self.feature_id = feature_id
        self.total_votes = total_votes
        self.positive_votes = positive_votes
        self.negative_votes = negative_votes
        self.last_updated = last_updated