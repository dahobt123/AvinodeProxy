import json
import datetime


class Message:
    message = {"standardResponse": {}, "responseMessage": {}}
    dictionary = {0: " ",
                  401: "bad token",
                  8089: " bad token",
                  8090: " bad token",
                  8093: " bad token",
                  1: "error",
                  }

    @classmethod
    def get_response(cls, err_num, response):
        cls.message["responseMessage"] = response

        if err_num == 0:
            cls.message["standardResponse"] = cls.get_good_standard_message()
            cls.message["responseMessage"] = response
            print(json.dumps(cls.message))
            return cls.message

        else:
            cls.message["standardResponse"] = cls.get_fatal_standard_message(err_num)
            cls.message["responseMessage"] = response
            print(json.dumps(cls.message))
            return cls.message

    @classmethod
    def get_good_standard_message(cls):
        return {
            "count": 0,
            "domain": "CAMP",
            "errorMessage": "",
            "language": "EN",
            "responseType": "GOOD",
            "returnCode": 0,
            "timeStampOfMessage": format(datetime.datetime.utcnow())
        }

    @classmethod
    def get_fatal_standard_message(cls, err_num):
        return {
            "count": 0,
            "domain": "CAMP",
            "errorMessage": cls.dictionary[err_num],
            "language": "EN",
            "responseType": "FATAL",
            "returnCode": err_num,
            "timeStampOfMessage": format(datetime.datetime.utcnow())
        }