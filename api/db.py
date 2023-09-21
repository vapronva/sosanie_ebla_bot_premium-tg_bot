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
        self.__cll.insert_one(content.dict())

    def get_request(self, requestID: str) -> Optional[UserRequestContentDatabaseModel]:
        foundRequest = self.__cll.find_one({"requestID": requestID})
        return (
            UserRequestContentDatabaseModel(**foundRequest or {})
            if foundRequest
            else None
        )

    def get_request_by_callback_data(
        self, callback_field: str, callback_id: str,
    ) -> Optional[UserRequestContentDatabaseModel]:
        foundRequest = self.__cll.find_one(
            {f"tts.callbackData.{callback_field}": callback_id},
        )
        return (
            UserRequestContentDatabaseModel(**foundRequest or {})
            if foundRequest
            else None
        )

    def get_user_allowed(self, user_id: int) -> bool:
        return self.__ull.find_one({"user_id": user_id, "allowed": True}) is not None

    def set_user_allowance(self, user_id: int, allowed: bool) -> None:
        self.__ull.update_one(
            {"user_id": user_id}, {"$set": {"allowed": allowed}}, upsert=True,
        )

    def create_token(self, token: DatabaseTokenObjectModel) -> None:
        self.__tll.insert_one(token.dict())

    def get_token(self, token: str) -> Optional[DatabaseTokenObjectModel]:
        foundToken = self.__tll.find_one({"token": token})
        return DatabaseTokenObjectModel(**foundToken or {}) if foundToken else None

    def update_token(
        self, token: str, fieldName: str, newValue: Any,
    ) -> DatabaseTokenObjectModel:
        return self.__tll.find_one_and_update(
            {"token": token},
            {"$set": {fieldName: newValue}},
            return_document=pymongo.ReturnDocument.AFTER,
        )

    def update_token_usage(self, token: str) -> None:
        self.__tll.update_one(
            {"token": token},
            {"$inc": {"used": 1}, "$set": {"lastUsage": datetime.now()}},
        )

    def check_token_usage(self, token: str) -> bool:
        currentToken = self.get_token(token)
        if not currentToken:
            return False
        if currentToken.maxUsage is None:
            return True
        return currentToken.totalUsage < currentToken.maxUsage
