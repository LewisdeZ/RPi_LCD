#!/usr/bin/env python3
# Check out these repos:
# https://github.com/r1cc4rdo/PTV_v3
# https://github.com/pizza1016/ptv-timetable

import requests
import hashlib
import hmac
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import asyncio
from aiohttp.client import ClientSession

# 86 TRAM
# route_type=1
# route_id=1881
# stop_id=2036
# stop_name="Gower ST/Plenty RD #48"
#
# Direction IDs:
# direction_id=34
# direction_name="Bundoora RMIT"
#
# direction_id=27
# direction_name="Waterfront City Docklands"


def next_trams(
            stop_id: int,
            route_id: int | None = None,
            low_floor_tram: bool = False,
            as_of: datetime = datetime.now(tz=ZoneInfo("Australia/Melbourne"))
        ) -> list:
    # https://github.com/pizza1016/ptv-timetable/blob/trunk/tramtracker/asyncapi.py#L76
    """Returns the details and times of the next trams to depart from the specified stop.
    The number of results returned can vary, but is usually three entries per destination.

    :param stop_id:        The TramTracker code of the stop
    :param route_id:       If specified, return next trams for the specified route identifier
    :param low_floor_tram: If set to ``True``, only departures with low-floor trams will be returned
    :param as_of:          The time from which to get departures; defaults to current system time
    :return:               A list of departures from the stop
    """
    TZ_MELBOURNE = ZoneInfo("Australia/Melbourne")
    EPOCH = datetime(1970, 1, 1, tzinfo=timezone.utc)
    if as_of.tzinfo is None:
        as_of = as_of.replace(tzinfo=TZ_MELBOURNE)
    as_of = as_of.astimezone(TZ_MELBOURNE)
    timestamp = round((as_of - EPOCH) / timedelta(milliseconds=1))
    request = f"/GetNextPredictionsForStop.ashx?stopNo={stop_id}\
    &routeNo={route_id if route_id is not None else 0}\
    &isLowFloor={'true' if low_floor_tram else 'false'}&ts={timestamp}"

    # url = f"http://tramtracker.com.au/Controllers{request}"

    session = ClientSession(base_url="http://tramtracker.com.au/Controllers")
    session.request("GET", request)

    # return [TramDeparture(stop_id=stop_id,
    #                         trip_id=element["TripID"],
    #                         route_id=element["InternalRouteNo"],
    #                         route_number=element["HeadBoardRouteNo"],
    #                         primary_route_number=element["RouteNo"],
    #                         vehicle_id=element["VehicleNo"] if element["VehicleNo"] != 0 else None,
    #                         vehicle_class=element["TramClass"] if element["TramClass"] != "" else None,
    #                         destination=element["Destination"],
    #                         tt_available=element["IsTTAvailable"],
    #                         low_floor_tram=element["IsLowFloorTram"],
    #                         air_conditioned=element["AirConditioned"],
    #                         display_ac_icon=element["DisplayAC"],
    #                         has_disruption=element["HasDisruption"],
    #                         disruptions=element["DisruptionMessage"]["Messages"],
    #                         has_special_event=element["HasSpecialEvent"],
    #                         special_event_message=element["SpecialEventMessage"] if element["SpecialEventMessage"] != "" else None,
    #                         has_planned_occupation=element["HasPlannedOccupation"],
    #                         planned_occupation_message=element["PlannedOccupationMessage"] if element["PlannedOccupationMessage"] != "" else None,
    #                         estimated_departure=(EPOCH + timedelta(milliseconds=int(TIMESTAMP_PATTERN.fullmatch(element["PredictedArrivalDateTime"]).group("timestamp")))).astimezone(TZ_MELBOURNE)
    #                         ) for element in response]

class PTVv3:
    """
    Minimal implementation of the Public Transport Victoria (PTV) v3 API.
    For documentation and instructions to obtain an id/key pair please visit:
    https://www.ptv.vic.gov.au/footer/data-and-reporting/datasets/ptv-timetable-api
    This file is part of the https://github.com/r1cc4rdo/PTV_v3 repository.
    """
    base_url = 'https://timetableapi.ptv.vic.gov.au'

    def __init__(self, ptv_id, ptv_key, debug=False):

        self.id = ptv_id
        self.key = ptv_key.encode('utf-8')
        self.debug = debug

    def __call__(self, endpoint, **params):
        """
        Signs and performs a request; throws on failure.
        Returns the JSON encoded response.
        """
        params['devid'] = self.id
        encoded = [f'{k}={v}'
                   for k, vs in params.items()
                   for v in (vs if isinstance(vs, (list, tuple)) else [vs])]

        request = f'{endpoint}?{"&".join(encoded)}'
        hashed = hmac.new(self.key, request.encode('utf-8'), hashlib.sha1)
        url = f'{PTVv3.base_url}{request}&signature={hashed.hexdigest()}'
        if self.debug:
            print(url)

        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_next_service():
        pass


if __name__ == '__main__':
    ptv_id, ptv_key = '3003660', 'ab1a8578-584c-4559-891b-f17a5d97fc32'
    ptv = PTVv3(ptv_id, ptv_key, debug=True)
    # print(ptv('/v3/disruptions', route_types=2))
    response = ptv('/v3/departures/route_type/1/stop/2036/route/1881')
    print(f"Response keys: {response.keys()}")

    # Give some pretty strings (16 characters or less) for the routes+directions
    route_names = {
        '86_from_city': '86 BUNDOORA RMIT',
        '86_to_city': '86 DOCKLANDS CBD',
        'train_to_city': 'TO CITY',
        'train_from_city': 'TO MERNDA'
    }

    tram_departures_bundoora = [ # direction_id=34
        datetime.strptime(
            departure['scheduled_departure_utc'][:-4],
            "%Y-%m-%dT%H:%M"
        )
        for departure in response['departures']
        if departure['direction_id'] == 34
    ]
    
    tram_departures_city = [ # direction_id=27
        datetime.strptime(
            departure['scheduled_departure_utc'][:-4],
            "%Y-%m-%dT%H:%M"
        )
        for departure in response['departures']
        if departure['direction_id'] == 27
    ]

    now = datetime.now() # Current time...



    next_trams(
        stop_id=2036,
        route_id=1881
    )

            # stop_id: int,
            # route_id: int | None = None,
            # low_floor_tram: bool = False,
            # as_of: datetime = datetime.now(tz=ZoneInfo("Australia/Melbourne"))
