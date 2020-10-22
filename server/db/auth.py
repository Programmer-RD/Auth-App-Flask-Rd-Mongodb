from server import *
import requests
from server.db.send_email import *


class Sign_Up:
    def __init__(self, user_name: str, password: str, email: str) -> None:
        self.user_name = user_name
        self.password = password
        self.email = email
        self.db = cluster["Auth"]
        self.collection = self.db["Auth"]

    def check_email_validitiy(self) -> bool:
        url = "https://isitarealemail.com/api/email/validate"
        # Send a request to the above url and passing the email that is going to be checked if it is valied or not.
        request_result = requests.get(
            url,
            {"email": self.email},
        )
        result = request_result.json()["status"]
        if result == "valid":  # if the email is valied it returns True
            return True
        # else it will return False
        return False

    def check_user_name_and_password(self) -> bool:
        results = []
        for result in self.collection.find(
            {"username": self.user_name, "password": self.password}
        ):  # this for loop takes all the users with the same user name and the password if there is none it will return True else it will return False Because there is someother user with the same user name and password
            results.append(result)
        if results == []:
            return True
        return False

    def check_email_and_password(self) -> bool:
        results = []
        for result in self.collection.find(
            {"email": self.email, "password": self.password}
        ):  # this for loop takes all the users with the same email and the password if there is none it will return True else it will return False Because there is someother user with the same email and password
            results.append(result)
        if results == []:
            return True
        return False

    def get_id(self):
        ids = []
        for id_ in self.collection.find({}):
            ids.append(id_["_id"])
        if ids == []:
            ids = 0
        else:
            ids = sorted(ids)[-1] + 1
        return [ids, True]

    def add_to_db(self) -> [bool, "result message for user"]:
        su = Sign_Up(user_name=self.user_name, password=self.password, email=self.email)
        results = [
            su.get_id(),
            su.check_email_and_password(),
            su.check_email_validitiy(),
            su.check_user_name_and_password(),
        ]  # This is a awesome way to not to write much if else elif statments
        if False not in results:
            self.collection.insert_one(
                {
                    "_id": results[0][0],
                    "username": self.user_name,
                    "password": self.password,
                    "email": self.email,
                }
            )
            return [True, "New Account Created ! "]
        errors = []
        if results[1] is False:
            errors.append("There is another using the same email and password as you.")
        if results[2] is False:
            errors.append("Your email is not valied ! ")
        if results[3] is False:
            errors.append(
                "There is another using the same user name and password as you."
            )
        return [False, errors]


class Sign_In:
    def __init__(self, user_name_or_email: str, password: str) -> None:
        self.user_name_or_email = user_name_or_email
        self.password = password
        self.db = cluster["Auth"]
        self.collection = self.db["Auth"]

    def check_user_name_and_password(self) -> bool:
        results = []
        for result in self.collection.find(
            {"username": self.user_name_or_email, "password": self.password}
        ):  # this for loop takes all the users with the same user name and the password if there is none it will return False else it will return True Because there is someother user with the same user name and password
            results.append(result)
        if results == []:
            return [False, "No User With the Same user name and password ! "]
        return [True, results[0]["email"]]

    def check_email_and_password(self) -> bool:
        results = []
        for result in self.collection.find(
            {"email": self.user_name_or_email, "password": self.password}
        ):  # this for loop takes all the users with the same email and the password if there is none it will return False else it will return True Because there is someother user with the same email and password
            results.append(result)
        if results == []:
            return [False, "No User With the Same email and password ! "]
        return [True, results[0]["email"]]

    def check(self) -> [bool, "result"]:
        si = Sign_In(user_name_or_email=self.user_name_or_email, password=self.password)
        results = [
            si.check_email_and_password(),
            si.check_user_name_and_password(),
        ]  # This is a awesome way to not to write much if else elif statments
        if results[0][0] is True or results[1][0] is True:
            print(results[0][1])
            try:
                send_mail(
                    to_email=results[0][1],
                    subject="Loged In Successfully ! ",
                    body="Loged In Successfully ! ",
                )
            except:
                send_mail(
                    to_email=results[1][1],
                    subject="Loged In Successfully ! ",
                    body="Loged In Successfully ! ",
                )
            return [True, "Loged In Successfully ! "]
        return [False, [results[0][1], results[1][1]]]
