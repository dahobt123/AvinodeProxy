from enum import Enum


class action_enum(Enum):
    GetValidAircraftDetailsWithChild = "GetValidAircraftDetailsWithChild",
    GetValidAircraft = " GetValidAircraft",
    GetLatestAircraftTimes = "GetLatestAircraftTimes",
    ReadAll = "ReadAll",
    updateTotals = "updateTotals",
    GetDueList = "GetDueList"