import json
import cglogging as cgl
import boto3
import os
import datetime
import time
from secret_manager import secret_manager
import requests
logger_Class = cgl.cglogging()
logger = logger_Class.setup_logging()


def lambda_handler(event, context):
    print(event)
    supplier_id = int(event["queryStringParameters"]["supplierId"])
    logger.debug("Received Avinode Message: ")
    try:
        body = event["body"]
        host_address = body["href"]
        data = get_update_message(supplier_id, host_address)
        msg_id = body["id"]
        if "arfq" in msg_id:
            process_rfq(body, supplier_id)
        else:
            process_trip_msg(body, supplier_id)


    except Exception as details:
        logger.error('Exception, Unexpected error: {} , {}'.format(19002, details))
        return 19002, 'Exception, Unexpected error ', 'FATAL', 'Auto Close Handler'


def get_update_message(supplier_id, host_address):
    secret_name = supplier_id + "-1-Profiles"
    secret_data = secret_manager.get_secrets(secret_name)
    secret_data = secret_data[2]
    secret_data = secret_data["SecretString"]
    secret_json = json.loads(secret_data)
    key_data = secret_json["CGFLFEED0006-CAMP"]
    key_data = json.loads(key_data)
    tokens = key_data["token"]
    # secret_string = secret_json["JWT"]
    headers = {}
    new_iso_timestamp = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()
    headers[
        "Authorization"] = "Bearer eyJraWQiOiI4MTIwMUVGMy01Qjk3LTRCQzktOTUwNC0wRTI4RDZBNzk4NzMiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzUxMiJ9.eyJzdWIiOiIxQTM1Mzg0NS1FNDg5LTRDQjctQjMxMi1GNzU1RDNBQjdFMDAiLCJhdmlkb21haW4iOiIuYXZpbm9kZS5jb20iLCJhdml0ZW5hbnQiOjU1NjksImlzcyI6ImF2aW5vZGUiLCJhdml0eXBlIjoxNiwiYXZpbm9uY2UiOiI3MTU1OTMyNS02NmEyLTRmNTAtYjRlNi1mNGQxNDkwMmQ0MzQifQ.TgC3yuc5Tstqx1ihKUR2XE-hkfEmgaok66vClWWEwqJ0LLYEFZ_U_rlDRde04fMMborC5CDo1FfzLYNN3sCuh11UyBVm4rzGlZQHxbJwB6Pk8viBR6DmxGi-BKoGaAv0Ch20Va73hMcrEGxYq2pm49tpkWV9uxRX58OqPIb2206D0M7Z5CihHet5ghsLJxg8OlAA-satsPFMQzu4daPLEIL9d91v5xLg0Pm6Jt4TKTDQQmr9yX8PQyGRY4sivqkWykdLIEU44UyPGrZH9n01S9juURa8nXFdO_U3LIvR-ByMTQ7Ne_GEBTkDPHID7f2LyGRTpr-zLzyqBN_mHHcJbw"
    headers["X-Avinode-ApiToken"] = "41888c20-319f-4b6b-b063-5b717e8a8857"
    headers["X-Avinode-SentTimestamp"] = new_iso_timestamp
    headers["X-Avinode-Product"] = "CAG-Noble"
    headers["Accept"] = "application/json"
    # items = json.dumps(body)
    response = requests.get(host_address,  headers=headers)
    body = response["body"]
    return body


def process_rfq(body):
    pass


def process_rfq(input_message, supplier_id):
    json_message = json.loads(input_message)
    meta_json = json_message["meta"]
    links_json = json_message["links"]
    message_data = json_message["data"]
    segments = message_data["segments"]
    seller_lift = message_data["sellerLift"]
    buyer_company = message_data["buyerCompany"]
    buyer_info = message_data["buyerAccount"]
    aircraft_type = seller_lift["aircraftType"]
    aircraft_tail = seller_lift["aircraftTail"]
    canceled = message_data["canceled"]
    if canceled == "true":
        canceled = True
    else:
        canceled = False
    journeys = []
    counter = 1
    pax_count = 0
    for segment in segments:
        journey = {}
        journeys.append(journey)
        pax_count = segment["paxCount"]
        origin = segment["startAirport"]
        destination = segment["endAirport"]
        if journey["faa"] is not None:
            journey["originAirportCode"] = origin["faa"]
        elif journey["icao"] is not None:
            journey["originAirportCode"] = origin["icao"]
        else:
            journey["originAirportCode"] = origin["unofficialICAO"]

        journey["destinationAirportCode"] = segment["endAirport"]

        # if dest_country == "US":
        if journey["faa"] is not None:
            journey["destinationAirportCode"] = origin["faa"]
        elif journey["icao"] is not None:
            journey["destinationAirportCode"] = origin["icao"]
        else:
            journey["destinationAirportCode"] = origin["unofficialICAO"]
        journey["journeyItem"] = counter
        departure_date = origin["departureDateTime"]["dateTimeLocal"]
        journey["departureDate"] = departure_date[0, 10]
        journey["departureTime"] = departure_date[11, 16]
        # journey["originState"] = origin["province"]["code"]
        # journey["destinationState"] = destination["province"]["code"]
        journey["aircraftType"] = aircraft_type
        journey["nnumber"] = aircraft_tail
        counter += 1
    call_shopping(journeys, pax_count, supplier_id)


def process_trip_msg(input_message, supplier_id):
    json_message = json.loads(input_message)
    # meta_json = json_message["meta"]
    # links_json = json_message["links"]
    message_data = json_message["quote"]
    # canceled = message_data["canceled"]
    # rfqs = message_data["rfqs"]
    segments = message_data["segments"]
    # seller_lift = rfqs["sellerLift"]
    # buyer_company = rfqs["buyerCompany"]
    # buyer_info = rfqs["buyerAccount"]
    # aircraft_type = seller_lift["aircraftType"]
    aircraft_tail = message_data["lift"]["aircraftTail"]
    # if canceled == "true":
    #     canceled = True
    # else:
    #     canceled = False
    journeys = []
    counter = 1
    pax_count = 0
    for segment in segments:
        journey = {}
        journeys.append(journey)
        pax_count = segment["paxCount"]
        origin = segment["startAirport"]
        destination = segment["endAirport"]
        # origin_country = origin["country"]["code"]
        # dest_country = destination["country"]["code"]
        if "faa" in origin:
            journey["originAirportCode"] = origin["faa"]
        elif "icao" in origin:
            journey["originAirportCode"] = origin["icao"]
        else:
            journey["originAirportCode"] = origin["unofficialICAO"]

        journey["destinationAirportCode"] = segment["endAirport"]

        if "faa" in destination:
            journey["destinationAirportCode"] = destination["faa"]
        elif "icao" in destination is not None:
            journey["destinationAirportCode"] = destination["icao"]
        else:
            journey["destinationAirportCode"] = destination["unofficialICAO"]
        # journey["originCountryCode"] = origin_country
        journey["journeyItem"] = counter
        journey["departureDate"] = segment["dateTime"]["date"]
        journey["departureTime"] = segment["dateTime"]["time"]
        journey["airportType"] = "A"
        # journey["destinationCountryCode"] = dest_country
        # journey["originCity"] = origin["city"]
        # journey["destinationCity"] = destination["city"]
        # departure_date = origin["departureDateTime"]["dateTimeLocal"]
        # journey["departureDate"] = departure_date[0, 10]
        # journey["departureTime"] = departure_date[11, 16]
        # journey["originState"] = origin["province"]["code"]
        # journey["destinationState"] = destination["province"]["code"]
        # journey["aircraftType"] = aircraft_type
        journey["nnumber"] = aircraft_tail
        counter += 1
    call_shopping(journeys, pax_count, supplier_id)



def call_shopping(journeys, pax_count, supplier_id):
    secret_name  = os.environ.get("CAG_Lambda_Secret")
    secret_data = secret_manager.get_secrets(secret_name)
    secret_string = secret_data[2]
    secret_string = secret_string["SecretString"]
    secret_json = json.loads(secret_string)
    secret_string = secret_json["JWT"]
    avinode_request = {}
    todays_date = datetime.date.fromtimestamp(time.time())
    date_in_ISOFormat = todays_date.isoformat()
    context = {"domainName": "Shopping", "language": "EN", "transactionId": date_in_ISOFormat,
               "securityToken": secret_string}
    avinode_request["context"] = context
    common_parms = {"action": "READ", "view": "SHOP", "version": "1.0.0", "client": "CAGPOS"}
    avinode_request["commonParms"] = common_parms
    request_body = {"charterTripType": 135, "primaryLanguage": "EN", "tripCategory": "L", "industry": "",
                    "totalExpectedPassengers": pax_count}
    suppliers = [supplier_id]
    request_body["supplierIds"] = suppliers
    request_body["discountCode"] = "Avinode"
    request = {}
    request["journey"] = journeys
    request["charterTripType"] = 135
    avinode_request["request"] = request
    cag_environment = os.environ.get("CAG_Environment")
    cag_region = os.environ.get("CAG_Region")
    function_name = os.environ.get("CAG_Shopping_Lambda") #+ ":" + cag_environment
    client = boto3.client('lambda', region_name=cag_region)
    try:
        lambda_response = client.invoke(
            FunctionName=function_name,
            Payload=json.dumps(avinode_request),
            InvocationType="RequestResponse",
        )
    except Exception as ex:
        cgl.error("An unexpected error occured: {}".format(ex))

    response = lambda_response['Payload'].read()
    i = 0


# get_update_message("7000", "")
#Tests
# get_update_message(7000, "https://sandbox.avinode.com/api/rfqs/arfq-1000000136")
trip_msg =  {
  "message": "We are pleased to give you the following offer. /Maria",
  "suppressNotification": "false",
  "quote": {
    "segments": [
      {
        "startAirport": {
          "icao": "ESGG"
        },
        "endAirport": {
          "icao": "EGGW"
        },
        "dateTime": {
          "date": "2019-08-17",
          "time": "05:30",
          "departure": "true",
          "local": "false"
        },
        "paxCount": "0",
        "paxSegment": "false",
        "showToBuyer": "false",
        "distanceNM": 602,
        "blockTimeMinutes": 100,
        "flightMinutes": 90
      },
      {
        "startAirport": {
          "icao": "EGGW"
        },
        "endAirport": {
          "icao": "LFPB"
        },
        "dateTime": {
          "date": "2019-08-17",
          "time": "08:00",
          "departure": "true",
          "local": "false"
        },
        "paxCount": "2",
        "paxSegment": "true",
        "showToBuyer": "true",
        "distanceNM": 207,
        "blockTimeMinutes": 53,
        "flightMinutes": 43
      },
      {
        "startAirport": {
          "icao": "LFPB"
        },
        "endAirport": {
          "icao": "ESGG"
        },
        "dateTime": {
          "date": "2019-08-17",
          "time": "11:00",
          "departure": "true",
          "local": "false"
        },
        "paxCount": "0",
        "paxSegment": "false",
        "showToBuyer": "false",
        "distanceNM": 679,
        "blockTimeMinutes": 118,
        "flightMinutes": 108
      }
    ],
    "lift": {
      "aircraftTail": "N12345"
    },
    "messageForBuyer" : "Price does not include de-icing.",
    "currencyCode": "EUR",
    "sellerUniqueQuoteIdentifier": "Q#18272",
    "totalPrice": 15100,
    "lineItems": [{
      "visibleToBuyer": "false",
      "displayName": "My own line item",
      "description": "",
      "type": "My type",
      "price": 5000,
      "formattedUnitPrice": "5,000.00",
      "formattedQuantity": "1"
    }, {
      "visibleToBuyer": "false",
      "displayName": "Another line item",
      "description": "",
      "type": "My type",
      "price": 4700,
      "formattedUnitPrice": "4,700.00",
      "formattedQuantity": "1"
    }],
    "attachments": [{
        "mimeType": "application/pdf",
        "name": "Quote123.pdf",
        "type": "Quote",
        "uri": "https://sandbox.avinode.com/marketplace/mvc/resource/quote/attachment/Quote123.pdf",
        "data": "abc123!?$*&()'-=@~.......",
        "temporaryAttachmentId": "string"
    }]
  }
}

json_message = json.dumps(trip_msg)
process_trip_msg(json_message, "7000")




