from enum import Enum, auto


class UnixTimestampTypes(Enum):
    SECONDS = auto()
    MILLIS = auto()
    NONE = auto()


class UnixTimestamp:
    def get_unix_timestamp_type(self, timestamp: int):
        if self.is_unix_timestamp_of_seconds_unit(timestamp):
            return UnixTimestampTypes.SECONDS

        if self.is_unix_timestamp_of_millis_unit(timestamp):
            return UnixTimestampTypes.MILLIS

        return UnixTimestampTypes.NONE

    def is_unix_timestamp(self, timestamp: int):
        is_seconds_timestamp = self.is_unix_timestamp_of_seconds_unit(timestamp)
        is_millis_timestamp = self.is_unix_timestamp_of_millis_unit(timestamp)
        return is_seconds_timestamp or is_millis_timestamp

    @staticmethod
    def is_unix_timestamp_of_seconds_unit(timestamp: int):
        lower_bound_seconds = 0
        upper_bound_seconds = 13569465600  # 2400-01-01 00:00:00 UTC
        is_timestamp = lower_bound_seconds <= timestamp <= upper_bound_seconds
        return is_timestamp

    @staticmethod
    def is_unix_timestamp_of_millis_unit(timestamp: int):
        lower_bound_millis = 0
        upper_bound_millis = 13569465600000  # 2400-01-01 00:00:00.000 UTC
        is_timestamp = lower_bound_millis <= timestamp <= upper_bound_millis
        return is_timestamp
