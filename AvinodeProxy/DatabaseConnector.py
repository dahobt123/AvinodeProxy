import json
import os
import cglogging as cgl
import psycopg2

from SecretManagertConnection import SecretManagerConnection

logger_Class = cgl.cglogging()
logger = logger_Class.setup_logging()


class DatabaseConnector:
    database_key = os.environ['CAG_DATABASE_CREDENTIALS']
    region = os.environ['CAG_REGION']
    host = ""
    user = ""
    password = ""
    database = "CharterAndGO"
    port = ""
    databaseConnection = None
    databaseCursor = None

    @classmethod
    def connect_to_database(cls):
        secret = SecretManagerConnection.get_secrets(cls.database_key, cls.region)
        logger.debug("inside database connector")
        if 'username' in secret['SecretString']:
            extracted_secret = json.loads(secret['SecretString'])
            cls.user = extracted_secret['username']
            cls.password = extracted_secret['password']
            cls.host = extracted_secret["host"]
            cls.port = extracted_secret['port']
            cls.engine = extracted_secret['engine']

        try:
            cls.databaseConnection = psycopg2.connect(user=cls.user, password=cls.password, database=cls.database,
                                                      host=cls.host, port=cls.port)
            return 0, " "
        except (Exception, psycopg2.Error) as error:
            cls.databaseConnection.rollback()
            print(1, "sql failed".format(error))
            return 1, " "

    # -----------------------------------orders---------------------------------------

    @classmethod
    def readOrders(cls, orders):
        logger.debug("inside Read orders database ")
        sql = """SELECT charter_supplier_id, order_id
        FROM public.reporting_orders WHERE charter_supplier_id = %s AND order_id = %s"""

        try:
            cursor = cls.databaseConnection.cursor()
            cursor.execute(sql, (orders["supplierId"], orders["orderId"]))
            resultList = cursor.fetchall()
            orderResult = []
            for result in resultList:
                orderResult.append({
                    "supplierId": result[0],
                    "orderId": result[1],
                })
            return orderResult

        except (Exception, psycopg2.Error) as error:
            cls.databaseConnection.rollback()
            print(1, "sql failed".format(error))

    @classmethod
    def createOrders(cls, orders):
        logger.debug(" inside create orders database ")
        sql = """INSERT INTO public.reporting_orders( trip_locator, status, charter_supplier_id, business_profile_id, 
        business_profile_name, book_date, departure_date, arrival_date, trip_level_origin_airport, 
        trip_level_destination_airport, passenger_segment_tax, federal_excise_tax, charterid, order_id, total_cost,
         total_base_price, total_charter_fees, base_price_override, order_substatus, international_tax, total_fuel_cost,
          total_cabin_cost, total_aircraft_hull_cost, total_maintenance_cost, total_supporting_services_cost, 
          total_airport_fees, total_government_taxes, charter_trip_type, trip_name, trip_org_first_name, 
          trip_org_last_name, trip_billing_company_name, trip_billing_company_address, trip_billing_company_city,
           trip_billing_company_state, trip_billing_first_name, trip_billing_last_name, trip_org_address, 
           trip_org_city, trip_org_state, payment, trip_billing_phone, order_source_detail, passenger_category, 
           trip_catergory, shopping_id, order_source, offer_id, trip_org_country, trip_org_pcode,
           trip_billing_country, trip_billing_pcode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
           %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

        try:
            cursor = cls.databaseConnection.cursor()
            cls.databaseCursor = cls.databaseConnection.cursor()
            cursor.execute(sql, (orders["tripLocator"],
                                 orders["orderStatus"],
                                 orders["supplierId"],
                                 orders["businessProfileId"],
                                 orders["businessProfileName"],
                                 orders["bookData"],
                                 orders["tripStartDate"],
                                 orders["tripEndDate"],
                                 orders["originAirport"],
                                 orders["destinationAirport"],
                                 orders["passengerSegmentTax"],
                                 orders["federalExciseTax"],
                                 orders["charterId"],
                                 orders["orderId"],
                                 orders["totalCost"],
                                 orders["totalBasePrice"],
                                 orders["totalCharterFees"],
                                 orders["basePriceOverride"],
                                 orders["orderSubStatus"],
                                 orders["internationalTax"],
                                 orders["totalFuelCost"],
                                 orders["totalCabinCost"],
                                 orders["totalAircraftHullCost"],
                                 orders["totalMaintenanceCost"],
                                 orders["totalSupportingServicesCost"],
                                 orders["totalAirportsFees"],
                                 orders["totalGovernmentTaxes"],
                                 orders["charterTripType"],
                                 orders["tripName"],
                                 orders["tripOrgFirstName"],
                                 orders["tripOrgLastName"],
                                 orders["tripBillingCompanyName"],
                                 orders["tripBillingCompanyAddress"],
                                 orders["tripBillingCompanyCity"],
                                 orders["tripBillingCompanyState"],
                                 orders["tripBillingFirstName"],
                                 orders["tripBillingLastName"],
                                 orders["tripOrgAddress"],
                                 orders["tripOrgCity"],
                                 orders["tripOrgState"],
                                 orders["payment"],
                                 orders["tripBillingPhone"],
                                 orders["orderSourceDetail"],
                                 orders["passengerCategory"],
                                 orders["tripCategory"],
                                 orders["shoppingId"],
                                 orders["orderSource"],
                                 orders["offerId"],
                                 orders["tripOrgCounty"],
                                 orders["tripOrgPcode"],
                                 orders["tripBillingCompanyCounty"],
                                 orders["tripBillingCompanyPcode"]
                                 ))
            cls.databaseConnection.commit()

            return 0, " "

        except (Exception, psycopg2.Error) as error:
            cls.databaseConnection.rollback()
            print(cls.databaseCursor.query)
            print(1, "sql failed to load orders".format(error))
            return 1, "failed to load orders ", " "

    @classmethod
    def updateOrders(cls, orders):
        logger.debug("inside update orders database ")
        sql = """UPDATE public.reporting_orders SET trip_locator=%s, status=%s, charter_supplier_id=%s, 
        business_profile_id=%s, business_profile_name=%s, book_date=%s, departure_date=%s, arrival_date=%s,
         trip_level_origin_airport=%s, trip_level_destination_airport=%s, passenger_segment_tax=%s, federal_excise_tax=%s,
          charterid=%s, order_id=%s, total_cost=%s, total_base_price=%s, total_charter_fees=%s, base_price_override=%s,
           order_substatus=%s, international_tax=%s, total_fuel_cost=%s, total_cabin_cost=%s, total_aircraft_hull_cost=%s, 
           total_maintenance_cost=%s, total_supporting_services_cost=%s, total_airport_fees=%s, total_government_taxes=%s,
            charter_trip_type=%s, trip_name=%s, trip_org_first_name=%s, trip_org_last_name=%s, trip_billing_company_name=%s,
             trip_billing_company_address=%s, trip_billing_company_city=%s, trip_billing_company_state=%s, 
             trip_billing_first_name=%s, trip_billing_last_name=%s, trip_org_address=%s, trip_org_city=%s, trip_org_state=%s,
              payment=%s, trip_billing_phone=%s, order_source_detail=%s, passenger_category=%s, trip_catergory=%s, 
              shopping_id=%s, order_source=%s, offer_id=%s, trip_org_country=%s, trip_org_pcode=%s, trip_billing_country=%s,
               trip_billing_pcode=%s WHERE  charter_supplier_id = %s AND order_id = %s ;"""
        try:
            cursor = cls.databaseConnection.cursor()
            cursor.execute(sql, (orders["tripLocator"],
                                 orders["orderStatus"],
                                 orders["supplierId"],
                                 orders["businessProfileId"],
                                 orders["businessProfileName"],
                                 orders["bookData"],
                                 orders["tripStartDate"],
                                 orders["tripEndDate"],
                                 orders["originAirport"],
                                 orders["destinationAirport"],
                                 orders["passengerSegmentTax"],
                                 orders["federalExciseTax"],
                                 orders["charterId"],
                                 orders["orderId"],
                                 orders["totalCost"],
                                 orders["totalBasePrice"],
                                 orders["totalCharterFees"],
                                 orders["basePriceOverride"],
                                 orders["orderSubStatus"],
                                 orders["internationalTax"],
                                 orders["totalFuelCost"],
                                 orders["totalCabinCost"],
                                 orders["totalAircraftHullCost"],
                                 orders["totalMaintenanceCost"],
                                 orders["totalSupportingServicesCost"],
                                 orders["totalAirportsFees"],
                                 orders["totalGovernmentTaxes"],
                                 orders["charterTripType"],
                                 orders["tripName"],
                                 orders["tripOrgFirstName"],
                                 orders["tripOrgLastName"],
                                 orders["tripBillingCompanyName"],
                                 orders["tripBillingCompanyAddress"],
                                 orders["tripBillingCompanyCity"],
                                 orders["tripBillingCompanyState"],
                                 orders["tripBillingFirstName"],
                                 orders["tripBillingLastName"],
                                 orders["tripOrgAddress"],
                                 orders["tripOrgCity"],
                                 orders["tripOrgState"],
                                 orders["payment"],
                                 orders["tripBillingPhone"],
                                 orders["orderSourceDetail"],
                                 orders["passengerCategory"],
                                 orders["tripCategory"],
                                 orders["shoppingId"],
                                 orders["orderSource"],
                                 orders["offerId"],
                                 orders["tripOrgCounty"],
                                 orders["tripOrgPcode"],
                                 orders["tripBillingCompanyCounty"],
                                 orders["tripBillingCompanyPcode"],
                                 orders["supplierId"],
                                 orders["orderId"]))
            cls.databaseConnection.commit()
            return 0, " "
        except (Exception, psycopg2.Error) as error:
            cls.databaseConnection.rollback()
            print(1, "sql failed to update orders".format(error))
            return 1, "failed to update orders"

    @classmethod
    def deleteOrders(cls, orders):
        logger.debug("inside delete orders database ")
        sql = """UPDATE public.reporting_orders
                SET order_id=%s, trip_locator=%s, status=%s, charter_supplier_id=%s, business_profile_id=%s, business_profile_name=%s,
                book_date=%s, departure_date=%s, trip_start_date=%s, trip_end_date=%s, trip_level_origin_airport=%s, 
                trip_level_destination_airport=%s, booking_fee=%s, booking_federal_excise_tax=%s, charterid=%s
                WHERE charter_supplier_id = %s AND order_id = %s ;"""

        try:
            cursor = cls.databaseConnection.cursor()
            cursor.execute(sql, (orders["orderId"], orders["tripName"], orders["status"],
                                 orders["supplierId"], orders["BusinessProfileId"],
                                 orders["businessProfileName"], orders["bookData"],
                                 orders["departureDate"], orders["startDate"],
                                 orders["endDate"], orders["originAirport"],
                                 orders["destinationAirport"], orders["booking_fee"],
                                 orders["federalExciseTax"], orders["charterId"],
                                 orders["supplierId"], orders["orderId"]))
            cls.databaseConnection.commit()
            return 0, " "
        except (Exception, psycopg2.Error) as error:
            cls.databaseConnection.rollback()
            print(1, "sql failed to update orders".format(error))
            return 1, "failed to update orders"

    # -----------------------------------OrderItems---------------------------------------

    @classmethod
    def createOrderItems(cls, orderItems):
        logger.debug(" inside create OrderItems database ")
        sql = """INSERT INTO public.reporting_order_items( order_item_id, order_id, origin_airport, destination_airport, 
        departure_time, arrival_time, aircraft_cag_id, aircraft_tail_number, aircraft_make, aircraft_model, 
        num_passengers, trip_distance_miles, total_segment_cost, passenger_service_tax, airport_fees, 
        charter_supplier_id, segment_type, segment_status, charterid, departure_taxi_time, flight_duration, 
        arrival_taxi_time, override_flight_duration, aircraft_hull_cost, supporting_services_cost, maintenance_cost, 
        fuel_cost, cabin_cost) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
         %s, %s, %s, %s, %s, %s, %s, %s);"""
        try:
            cursor = cls.databaseConnection.cursor()
            cursor.execute(sql, (orderItems["orderItemId"],
                                 orderItems["orderId"],
                                 orderItems["originAirport"],
                                 orderItems["destinationAirport"],
                                 orderItems["startTime"],
                                 orderItems["endTime"],
                                 orderItems["aircraftCagId"],
                                 orderItems["tailNumber"],
                                 orderItems["make"],
                                 orderItems["model"],
                                 orderItems["numPassengers"],
                                 orderItems["mileage"],
                                 orderItems["totalCost"],
                                 orderItems["passengerServiceTax"],
                                 orderItems["airportFees"],
                                 orderItems["charterSupplierId"],
                                 orderItems["segmentType"],
                                 orderItems["segmentStatus"],
                                 orderItems["charterId"],
                                 orderItems["departureTaxiTime"],
                                 orderItems["flightDuration"],
                                 orderItems["arrivalTaxiTime"],
                                 orderItems["overrideFlightDuration"],
                                 orderItems["aircraftHullCost"],
                                 orderItems["supportingServicesCost"],
                                 orderItems["maintenanceCost"],
                                 orderItems["fuelCost"],
                                 orderItems["cabinCost"]))

            cls.databaseConnection.commit()

            return 0, " "

        except (Exception, psycopg2.Error) as error:
            cls.databaseConnection.rollback()
            print(1, "sql failed to load orders".format(error))
            return 1, "failed to load orders ", " "

    @classmethod
    def readOrderItems(cls, order):
        logger.debug("inside Read OrderItems database ")

        sql = """SELECT order_item_id, order_id, origin_airport, destination_airport, departure_time, arrival_time, 
        aircraft_cag_id, aircraft_tail_number, aircraft_make, aircraft_model, num_passengers, trip_distance_miles, 
        total_segment_cost, passenger_service_tax, airport_fees, charter_supplier_id, segment_type, segment_status, 
        charterid, departure_taxi_time, flight_duration, arrival_taxi_time, override_flight_duration, 
        aircraft_hull_cost, supporting_services_cost, maintenance_cost, fuel_cost, cabin_cost
        FROM public.reporting_order_items 
        WHERE charter_supplier_id = %s AND order_id = %s """

        try:
            cursor = cls.databaseConnection.cursor()
            cursor.execute(sql, (order["supplierId"], order["orderId"]))
            resultList = cursor.fetchall()
            resultOrderItems = []
            for result in resultList:
                resultOrderItems.append({"orderItemId": result[0],
                                         "orderId": result[1],
                                         "originAirport": result[2],
                                         "destinationAirport": result[3],
                                         "startTime": result[4],
                                         "endTime": result[5],
                                         "aircraftCagId": result[6],
                                         "tailNumber": result[7],
                                         "make": result[8],
                                         "model": result[9],
                                         "numPassengers": result[10],
                                         "mileage": result[11],
                                         "totalCost": result[12],
                                         "passengerServiceTax": result[13],
                                         "airportFees": result[14],
                                         "charterSupplierId": result[15],
                                         "segmentType": result[16],
                                         "segmentStatus": result[17],
                                         "charterId": result[18],
                                         "departureTaxiTime": result[19],
                                         "flightDuration": result[20],
                                         "arrivalTaxiTime": result[21],
                                         "overrideFlightDuration": result[22],
                                         "aircraftHullCost": result[23],
                                         "supportingServicesCost": result[24],
                                         "maintenanceCost": result[25],
                                         "fuelCost": result[26],
                                         "cabinCost": result[27],
                                         })
            if len(resultOrderItems):
                return 0, " ", resultOrderItems
            else:
                return 0, " ", None
        except (Exception, psycopg2.Error) as error:
            cls.databaseConnection.rollback()
            print(1, "sql failed to load orders".format(error))
            return 1, "failed to load orders ", " "

    @classmethod
    def updateOrderItems(cls, orderItems):
        logger.debug("inside update OrderItems database ")
        sql = """UPDATE public.reporting_order_items SET order_item_id=%s, order_id=%s, origin_airport=%s, 
        destination_airport=%s, departure_time=%s, arrival_time=%s, aircraft_cag_id=%s, aircraft_tail_number=%s, 
        aircraft_make=%s, aircraft_model=%s, num_passengers=%s, trip_distance_miles=%s, total_segment_cost=%s, 
        passenger_service_tax=%s, airport_fees=%s, charter_supplier_id=%s, segment_type=%s, segment_status=%s, charterid=%s, 
        departure_taxi_time=%s, flight_duration=%s, arrival_taxi_time=%s, override_flight_duration=%s, 
        aircraft_hull_cost=%s, supporting_services_cost=%s, maintenance_cost=%s, fuel_cost=%s, cabin_cost=%s 
        WHERE charter_supplier_id = %s AND order_item_id =%s AND order_id = %s;"""

        try:
            cursor = cls.databaseConnection.cursor()
            cursor.execute(sql, (orderItems["orderItemId"],
                                 orderItems["orderId"],
                                 orderItems["originAirport"],
                                 orderItems["destinationAirport"],
                                 orderItems["startTime"],
                                 orderItems["endTime"],
                                 orderItems["aircraftCagId"],
                                 orderItems["tailNumber"],
                                 orderItems["make"],
                                 orderItems["model"],
                                 orderItems["numPassengers"],
                                 orderItems["mileage"],
                                 orderItems["totalCost"],
                                 orderItems["passengerServiceTax"],
                                 orderItems["airportFees"],
                                 orderItems["charterSupplierId"],
                                 orderItems["segmentType"],
                                 orderItems["segmentStatus"],
                                 orderItems["charterId"],
                                 orderItems["departureTaxiTime"],
                                 orderItems["flightDuration"],
                                 orderItems["arrivalTaxiTime"],
                                 orderItems["overrideFlightDuration"],
                                 orderItems["aircraftHullCost"],
                                 orderItems["supportingServicesCost"],
                                 orderItems["maintenanceCost"],
                                 orderItems["fuelCost"],
                                 orderItems["cabinCost"],
                                 orderItems["charterSupplierId"],
                                 orderItems["orderItemId"],
                                 orderItems["orderId"]))
            cls.databaseConnection.commit()

            return 0, " "
        except (Exception, psycopg2.Error) as error:
            cls.databaseConnection.rollback()
            print(1, "sql failed to load orders".format(error))
            return 1, "failed to load orders ", " "

    @classmethod
    def deleteOrderItems(cls, orderItems):
        logger.debug("inside delete OrderItems database ")
        sql = """DELETE FROM public.reporting_order_items
                    WHERE charter_supplier_id = %s AND order_item_id =%s AND order_id;"""
        try:
            cursor = cls.databaseConnection.cursor()
            cursor.execute(sql, (orderItems["supplierId"], orderItems["orderItemId"], orderItems["orderId"]))
            cls.databaseConnection.commit()

            return 0, " "
        except (Exception, psycopg2.Error) as error:
            cls.databaseConnection.rollback()
            print(1, "sql failed to load orders".format(error))
            return 1, "failed to load orders ", " "

    # -----------------------------------OrderItemCrew---------------------------------------

    @classmethod
    def createOrderItemCrew(cls, crew):
        logger.debug(" inside create OrderItemCrew database ")
        sql = """INSERT INTO public.reporting_order_item_crew_assignment( order_item_id, crew_profile_id, first_name, 
        last_name, order_id, charter_supplier_id, crew_type, charterid)	VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
        try:
            cursor = cls.databaseConnection.cursor()
            cursor.execute(sql, (crew["orderItemId"],
                                 crew["crewProfileId"],
                                 crew["firstName"],
                                 crew["lastName"],
                                 crew["orderId"],
                                 crew["charterSupplierId"],
                                 crew["crewType"],
                                 crew["charterId"],
                                 ))
            cls.databaseConnection.commit()
            return 0, " "
        except (Exception, psycopg2.Error) as error:
            cls.databaseConnection.rollback()
            print(1, "sql failed to load crew".format(error))
            return 1, "failed to load crew ", " "

    @classmethod
    def readOrderItemCrew(cls, orderId, charterId):
        logger.debug("inside Read OrderItemCrew database ")
        sql = """SELECT order_item_id, crew_profile_id, first_name, last_name, order_id, charter_supplier_id, 
        crew_type, charterid FROM public.reporting_order_item_crew_assignment 
        WHERE order_id = %s AND charter_supplier_id = %s;"""
        try:
            cursor = cls.databaseConnection.cursor()
            cursor.execute(sql, (orderId, charterId))
            resultList = cursor.fetchall()
            crewResult = []
            for result in resultList:
                crewResult.append({
                    "orderItemId": result[0],
                    "crewProfileId": result[1],
                    "firstName": result[2],
                    "lastName": result[3],
                    "orderId": result[4],
                    "supplierId": result[5],
                    "crewType": result[6],
                    "charterId": result[7]
                })

            if len(crewResult) > 0:
                return 0, " ", crewResult
            else:
                return 0, " ", None
        except (Exception, psycopg2.Error) as error:
            cls.databaseConnection.rollback()
            print(1, "sql failed to load crew".format(error))
            return 1, "failed to load crew ", None

    @classmethod
    def updateOrderItemCrew(cls, crew):
        logger.debug("inside update OrderItemCrew database ")
        sql = """UPDATE public.reporting_order_item_crew_assignment
            SET order_item_id=%s, crew_profile_id=%s, first_name=%s, last_name=%s, order_id=%s, charter_supplier_id=%s,
             crew_type=%s, charterid=%s  WHERE charter_supplier_id =%s AND order_id=%s AND order_item_id =%s  AND 
             crew_profile_id=%s; """
        try:
            cursor = cls.databaseConnection.cursor()
            cursor.execute(sql, (crew["orderItemId"], crew["crewProfileId"], crew["firstName"], crew["lastName"],
                                 crew["orderId"], crew["charterSupplierId"], crew["crewType"], crew["charterId"],
                                 crew["charterSupplierId"], crew["orderId"], crew["orderItemId"],
                                 crew["crewProfileId"]))
            cls.databaseConnection.commit

            return 0, " "
        except (Exception, psycopg2.Error) as error:
            cls.databaseConnection.rollback()
            print(1, "sql failed to load crew".format(error))
            return 1, "failed to load crew ", " "

    @classmethod
    def deleteOrderItemCrew(cls, crew):
        logger.debug("inside delete OrderItemCrew database ")
        sql = """DELETE FROM public.reporting_order_item_crew_assignment
            WHERE charter_supplier_id =%s AND order_id=%s AND order_item_id =%s AND crew_profile_id =%s ;"""
        try:
            cursor = cls.databaseConnection.cursor()
            cursor.execute(sql, (crew["supplierId"], crew["orderId"], crew["orderItemId"], crew["crewProfileId"]))
            cls.databaseConnection.commit()

            return 0, " "
        except (Exception, psycopg2.Error) as error:
            cls.databaseConnection.rollback()
            print(1, "sql failed to load crew".format(error))
            return 1, "failed to load crew ", " "

    # -----------------------------------OrderItemPassenger---------------------------------------

    @classmethod
    def createOrderItemPassenger(cls, passenger):
        logger.debug(" inside create OrderItemPassenger database ")
        sql = """INSERT INTO public.reporting_order_item_pax 
        (order_item_id, first_name, last_name, charter_supplier_id, order_id, charterid)
            VALUES (%s, %s, %s, %s, %s, %s);"""
        try:
            cursor = cls.databaseConnection.cursor()
            cursor.execute(sql, (passenger["orderItemId"], passenger["firstName"], passenger["lastName"],
                                 passenger["charterSupplierId"], passenger["orderId"], passenger["charterId"]))
            cls.databaseConnection.commit()

            return 0, " "
        except (Exception, psycopg2.Error) as error:
            cls.databaseConnection.rollback()
            print(1, "sql failed to load passenger".format(error))
            return 1, "failed to load crew passenger"

    @classmethod
    def readOrderItemPassenger(cls, orderId, charterId):
        logger.debug("inside Read OrderItemPassenger database ")
        sql = """SELECT order_item_id, first_name, last_name, charter_supplier_id, order_id
            FROM public.reporting_order_item_pax WHERE  order_id = %s AND charter_supplier_id = %s; """
        try:
            cursor = cls.databaseConnection.cursor()
            cursor.execute(sql, (orderId, charterId))

            resultList = cursor.fetchall()
            passengerResult = []
            for result in resultList:
                passengerResult.append({
                    "orderItemId": result[0],
                    "firstName": result[1],
                    "lastName": result[2],
                    "supplierId": result[3],
                    "orderId": result[4],
                })
            if len(passengerResult) > 0:
                return 0, " ", passengerResult
            else:
                return 0, " ", None
        except (Exception, psycopg2.Error) as error:
            cls.databaseConnection.rollback()
            print(1, "sql failed to load passenger".format(error))
            return 1, "failed to load crew passenger", None

    @classmethod
    def updateOrderItemPassenger(cls, passenger):
        logger.debug("inside update OrderItemPassenger database ")
        sql = """UPDATE public.reporting_order_item_pax
            SET order_item_id=%s, first_name=%s, last_name=%s, charter_supplier_id=%s, order_id=%s, charterid=%s
            WHERE order_item_id= %s AND charter_supplier_id = %s AND order_id = %s AND first_name=%s 
            AND last_name=%s;"""
        try:
            cursor = cls.databaseConnection.cursor()
            cursor.execute(sql, (passenger["orderItemId"], passenger["firstName"], passenger["lastName"],
                                 passenger["charterSupplierId"], passenger["orderId"], passenger["charterId"],
                                 passenger["orderItemId"], passenger["charterSupplierId"], passenger["orderId"],
                                 passenger["firstName"], passenger["lastName"]))
            cls.databaseConnection.commit()

            return 0, " "
        except (Exception, psycopg2.Error) as error:
            cls.databaseConnection.rollback()
            print(1, "sql failed to load passenger".format(error))
            return 1, "failed to load crew passenger"

    @classmethod
    def deleteOrderItemPassenger(cls, passenger):
        logger.debug("inside delete OrderItemPassenger database ")
        sql = """DELETE FROM public.reporting_order_item_pax
            WHERE order_item_id= %s AND  user_id =%s AND charter_supplier_id = %s AND order_id = %s;"""
        try:
            cursor = cls.databaseConnection.cursor()
            cursor.execute(sql, (passenger["orderItemId"], passenger["userId"],
                                 passenger["supplierId"], passenger["orderId"]))

            result = cursor.fetchall()
            passengerResult = {
                "orderItemId": result["order_item_id"],
                "firstName": result["first_name"],
                "lastName": result["last_name"],
                "supplierId": result["charter_supplier_id"],
                "orderId": result["order_id"],
                "charterId": result["charterid"]
            }
            return 0, " ", passengerResult
        except (Exception, psycopg2.Error) as error:
            cls.databaseConnection.rollback()
            print(1, "sql failed to load passenger".format(error))
            return 1, "failed to load crew passenger", passengerResult

    @classmethod
    def commit(cls):
        cls.databaseConnection.commit

    @classmethod
    def close_connection(cls):
        cls.databaseConnection.close()