from Models.Account import Account, Privacy
from Database import session_scope
from Models.DailyAccountData import DailyAccountData


class AccountRepository:
    @classmethod
    def register_account(cls, acc_username, infl_id, full_name, biography,
                         followers_count, media_count, like_average, comment_average,
                         activity_per_follower, influencer_privacy):
        with session_scope() as session:
            new_acc = Account(acc_username, infl_id, full_name, biography,
                              followers_count, media_count, like_average, comment_average,
                              activity_per_follower, influencer_privacy)
            session.flush()
            session.add(new_acc)
            session.flush()
            new_acc_id = new_acc.id
            session.commit()
            return new_acc_id

    @classmethod
    def check_account_exists(cls, username):
        with session_scope() as session:
            account_item = session.query(Account).filter(
                Account.username == username
            ).first()
            return account_item.id if account_item else None

    @classmethod
    def get_user_id(cls, acc_id):
        with session_scope() as session:
            acc = session.query(Account).filter(Account.id == acc_id).first()
            return acc.user_id if acc else None

    @classmethod
    def get_username(cls, acc_id):
        with session_scope() as session:
            acc = session.query(Account).filter(Account.id == acc_id).first()
            return acc.username if acc else None

    @classmethod
    def register_daily_account_log(cls, acc_id, follower, AVG_Like, AVG_Comment, AVG_share, AVG_save,
                                   engagement_rate, stories, posts, monitoring_status, privacy, price=None):
        with session_scope() as session:
            new_report = DailyAccountData(acc_id, follower, AVG_Like, AVG_Comment, AVG_share, AVG_save,
                                          engagement_rate, stories, posts, monitoring_status, privacy, price)
            session.add(new_report)
            session.commit()
