from typing import List
import pymongo
from models import VoiceMessageTTSInlineModel


class DB:
    def __init__(self, uri: str) -> None:
        self.__client = pymongo.MongoClient(uri)
        self.__db = self.__client["sebp"]
        self.__cll = self.__db["content"]
        self.__ull = self.__db["allowed"]

    def create_user_content(
        self,
        user_id: int,
        requestID: str,
        content: str,
        tts: List[VoiceMessageTTSInlineModel],
    ) -> None:
        self.__cll.insert_one(
            {"user_id": user_id, "requestID": requestID, "content": content, "tts": tts}
        )

    def get_request(self, requestID: str) -> dict:
        return self.__cll.find_one({"requestID": requestID})

    def get_user_allowed(self, user_id: int) -> bool:
        return self.__ull.find_one({"user_id": user_id, "allowed": True}) is not None

    def set_user_allowance(self, user_id: int, allowed: bool) -> None:
        self.__ull.update_one(
            {"user_id": user_id}, {"$set": {"allowed": allowed}}, upsert=True
        )
