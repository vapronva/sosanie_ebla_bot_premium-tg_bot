from datetime import datetime
from typing import Any, Optional

import pymongo

from models import DatabaseTokenObjectModel, UserRequestContentDatabaseModel


class DB:
    def __init__(self, uri: str) -> None:
        self.__client = pymongo.MongoClient(uri)
        self.__db = self.__client["sebp"]
        self.__cll = self.__db["content"]
        self.__ull = self.__db["allowed"]
        self.__tll = self.__db["tokens"]

    def create_user_content(self, content: UserRequestContentDatabaseModel) -> None:
        self.__cll.insert_one(content.model_dump(mode="json"))

    def get_request(self, request_id: str) -> Optional[UserRequestContentDatabaseModel]:
        found_request = self.__cll.find_one({"requestID": request_id})
        return (
            UserRequestContentDatabaseModel(**found_request or {})
            if found_request
            else None
        )

    def get_request_by_callback_data(
        self,
        callback_field: str,
        callback_id: str,
    ) -> Optional[UserRequestContentDatabaseModel]:
        found_request = self.__cll.find_one(
            {f"tts.callbackData.{callback_field}": callback_id},
        )
        return (
            UserRequestContentDatabaseModel(**found_request or {})
            if found_request
            else None
        )

    def get_user_allowed(self, user_id: int) -> bool:
        return self.__ull.find_one({"user_id": user_id, "allowed": True}) is not None

    def set_user_allowance(self, user_id: int, allowed: bool) -> None:
        self.__ull.update_one(
            {"user_id": user_id},
            {"$set": {"allowed": allowed}},
            upsert=True,
        )

    def create_token(self, token: DatabaseTokenObjectModel) -> None:
        self.__tll.insert_one(token.model_dump(mode="json"))

    def get_token(self, token: str) -> Optional[DatabaseTokenObjectModel]:
        found_token = self.__tll.find_one({"token": token})
        return DatabaseTokenObjectModel(**found_token or {}) if found_token else None

    def update_token(
        self,
        token: str,
        field_name: str,
        new_value: Any,
    ) -> DatabaseTokenObjectModel:
        return self.__tll.find_one_and_update(
            {"token": token},
            {"$set": {field_name: new_value}},
            return_document=pymongo.ReturnDocument.AFTER,
        )

    def update_token_usage(self, token: str) -> None:
        self.__tll.update_one(
            {"token": token},
            {"$inc": {"used": 1}, "$set": {"lastUsage": datetime.now()}},
        )

    def check_token_usage(self, token: str) -> bool:
        if current_token := self.get_token(token):
            return (
                True
                if current_token.maxUsage is None
                else current_token.used < current_token.maxUsage
            )
        else:
            return False
