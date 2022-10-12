from typing import List
import pymongo
from models import VoiceMessageTTSInlineModel


class DB:
    def __init__(self, uri: str) -> None:
        self.__client = pymongo.MongoClient(uri)
        self.__db = self.__client["sebp"]
        self.__cll = self.__db["content"]

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
