from typing import List, Optional
import pymongo
from models import UserRequestContentDatabaseModel


class DB:
    def __init__(self, uri: str) -> None:
        self.__client = pymongo.MongoClient(uri)
        self.__db = self.__client["sebp"]
        self.__cll = self.__db["content"]
        self.__ull = self.__db["allowed"]

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
        self, callback_field: str, callback_id: str
    ) -> Optional[UserRequestContentDatabaseModel]:
        foundRequest = self.__cll.find_one(
            {f"tts.callbackData.{callback_field}": callback_id}
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
            {"user_id": user_id}, {"$set": {"allowed": allowed}}, upsert=True
        )
