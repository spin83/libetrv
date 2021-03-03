import enum

from .properties import eTRVData, eTRVSingleData
from .fields import eTRVField, TemperatureField, UTCDateTimeField, LocalDateTimeField, EnumField, \
    HexField, TextField, BitField


class BatteryData(eTRVSingleData):
    battery = eTRVField(read_only=True)
    class Meta:
        structure = {
            0x10: """
                unsigned char battery;
            """,
        }
        use_encoding = False
        read_only = True
        direct_field = 'battery'


class DeviceInformationData(eTRVData):
    manufacturer_name = eTRVField(0x15, read_only=True)
    model_number = eTRVField(0x17, read_only=True)
    serial_number = eTRVField(0x19, read_only=True)
    hardware_revision = eTRVField(0x1b, read_only=True)
    firmware_revision = eTRVField(0x1d, read_only=True)
    software_revision = eTRVField(0x1f, read_only=True)
    system_id = eTRVField(0x21, read_only=True)
    class Meta:
        structure = {
            0x15: "str manufacturer_name",
            0x17: "str model_number",
            0x19: "str serial_number",
            0x1b: "str hardware_revision",
            0x1d: "str firmware_revision",
            0x1f: "str software_revision",
            0x21: "str system_id"
        }
        use_encoding = False
        read_only = True


class PinSettingsData(eTRVData):
    pin_number = eTRVField()
    pin_enabled = BitField(name='pin_enabled', bit_position=0)

    class Meta:
        structure = {
            0x27: """
                unsigned int pin_number;
                unsigned char pin_enabled;
                unsigned char padding[3];
            """
        }

class ScheduleMode(enum.Enum):
    MANUAL = 0
    SCHEDULED = 1
    VACATION = 3
    HOLD = 5

class ConfigBits(enum.IntEnum):
    ADAPTABLE_REGULATION = 0
    VERTICAL_INSTALATION = 2
    DISPLAY_FLIP = 3
    SLOW_REGULATION = 4
    VALVE_INSTALLED = 6
    LOCK_CONTROL = 7


class SettingsData(eTRVData):
    adaptable_regulation = BitField(name='config_bits', bit_position=ConfigBits.ADAPTABLE_REGULATION)
    vertical_instalation = BitField(name='config_bits', bit_position=ConfigBits.VERTICAL_INSTALATION)
    display_flip = BitField(name='config_bits', bit_position=ConfigBits.DISPLAY_FLIP)
    slow_regulation = BitField(name='config_bits', bit_position=ConfigBits.SLOW_REGULATION)
    valve_installed = BitField(name='config_bits', bit_position=ConfigBits.VALVE_INSTALLED)
    lock_control = BitField(name='config_bits', bit_position=ConfigBits.LOCK_CONTROL)
    temperature_min = TemperatureField()
    temperature_max = TemperatureField()
    frost_protection_temperature = TemperatureField()
    schedule_mode = EnumField(enum_class=ScheduleMode)
    vacation_temperature = TemperatureField()
    vacation_from = UTCDateTimeField()
    vacation_to = UTCDateTimeField()

    class Meta:
        structure = {
            0x2a: """
                unsigned char config_bits;
                unsigned char temperature_min;
                unsigned char temperature_max;
                unsigned char frost_protection_temperature;
                unsigned char schedule_mode;
                unsigned char vacation_temperature; 
                int vacation_from;
                int vacation_to;
                unsigned char padding[2];
            """
        }


class TemperatureData(eTRVData):
    room_temperature = TemperatureField(read_only=True)
    set_point_temperature = TemperatureField(auto_save=True)

    class Meta:
        structure = {
            0x2d: """
                unsigned char set_point_temperature;
                unsigned char room_temperature;
                unsigned char padding[6];
            """
        }


class NameData(eTRVSingleData):
    name = TextField(max_length=16, auto_save=True)

    class Meta:
        structure = {
            0x30: """
                char name[16];
            """
        }
        direct_field = 'name'


class CurrentTimeData(eTRVSingleData):
    current_time = LocalDateTimeField(name='time_local', tz_field='time_offset', auto_save=True)

    class Meta:
        structure = {
            0x36: """
                int time_local;
                int time_offset;
            """
        }
        direct_field = 'current_time'

class ErrorBits(enum.IntEnum):
    E9_VALVE_DOES_NOT_CLOSE = 8
    E10_INVALID_TIME = 9
    E14_LOW_BATTERY = 13
    E15_VERY_LOW_BATTERY = 14

class ErrorData(eTRVData):
    error = eTRVField(auto_save=True)
    e9_valve_does_not_close = BitField(name='error', bit_position=ErrorBits.E9_VALVE_DOES_NOT_CLOSE)
    e10_invalid_time = BitField(name='error', bit_position=ErrorBits.E10_INVALID_TIME)
    e14_low_battery = BitField(name='error', bit_position=ErrorBits.E14_LOW_BATTERY)
    e15_very_low_battery = BitField(name='error', bit_position=ErrorBits.E15_VERY_LOW_BATTERY)
    class Meta:
        structure = {
            0x39: """
                unsigned short error;
                unsigned char padding[6];
            """
        }

class LocaleData(eTRVSingleData):
    locale = TextField(max_length=2, auto_save=True)

    class Meta:
        structure = {
            0x3c: """
                char locale[2];
                unsigned char padding[6];
            """
        }
        direct_field = 'locale'
        write_only = True

class SecretKeyData(eTRVSingleData):
    key = HexField(read_only=True)

    class Meta:
        structure = {
            0x3f: """
                char key[16];
            """
        }
        use_encoding = False
        direct_field = 'key'


# class DaySchedule(eTRVData):
#     __struct__ = """
#         unsigned char _data[6];
#     """


# class ScheduleStruct(eTRVData):
#     __struct__ = """
#         unsigned char _home_temperature;
#         unsigned char _away_temperature;
#         struct DaySchedule _schedule[7];
#     """
