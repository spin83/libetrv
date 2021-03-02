import time
import fire
import datetime as dt
import locale
from libetrv.device import eTRVDevice


def time_to_str(datetime):
    if datetime is not None:
        return datetime.strftime('%Y-%m-%d %H:%M:%S %Z')
    return None


class CLI:
    def __init__(self, pin=None, secret=None):
        self._pin = pin
        if secret is not None:
            self._secret = bytes.fromhex(secret)
        else:
            self._secret = None

    def scan(self, timeout=10.):
        print("Detected eTRV devices:")
        for device, key in eTRVDevice.scan(timeout):
            key_str = key if key is not None else "-"
            print("{}, RSSI={}dB, key={}".format(device.addr, device.rssi, key_str))
    
    def device(self, device_id):
        return Device(device_id, self._pin, self._secret)


class Device:
    def __init__(self, device, pin, secret):
        self._pin = pin
        self._secret = secret
        self._device = eTRVDevice(device, pin=self._pin, secret=self._secret)

    def get_handler(self, uuid):
        self._device.connect(False)
        ch = self._device.ble_device.getCharacteristics(uuid=uuid)[0]
        print("Handler: 0x{:02X}".format(ch.getHandle()))

    def retrieve_key(self):
        print(
            "In 5 seconds this script will try to retrieve a secure key from eTRV device. "
            "Don't forget to save it for later. Before that be sure that device is in pairing mode. "
            "You can achieve that by pressing button on device"
        )
        time.sleep(5)
        print("Secret Key:", self._device.secret_key)

    def battery(self):
        result = self._device.battery
        print("Battery level: {}%".format(result))

    def pin_settings(self):
        result = self._device.pin_settings
        print('Pin number:  {:04d}'.format(result.pin_number))
        print('Pin enabled: {}'.format(result.pin_enabled))

    def settings(self):
        result = self._device.settings
        print('Frost protection temperature: {:.1f}°C'.format(result.frost_protection_temperature))
        print('Schedule mode:                {}'.format(result.schedule_mode))
        print('Vacation temperature:         {:.1f}°C'.format(result.vacation_temperature))
        print('Vacation From:                {}'.format(time_to_str(result.vacation_from)))
        print('Vacation To:                  {}'.format(time_to_str(result.vacation_to)))

    def temperature(self):
        temp = self._device.temperature
        print("Current room temperature: {:.1f}°C".format(temp.room_temperature))
        print("Set point temperature:    {:.1f}°C".format(temp.set_point_temperature))

    def name(self):
        device_name = self._device.name
        print("Device name: '{}'".format(device_name))

    def current_time(self):
        device_time = self._device.current_time
        print("Current time: {}".format(time_to_str(device_time)))
        
    def set_setpoint(self, setpoint):
        self._device.temperature.set_point_temperature = setpoint
        
    def set_pin(self, pin):
        if pin==0:
            self._device.pin_settings.pin_number = 0
            self._device.pin_settings.pin_enabled = False
            self._device.pin_settings.save()
        elif pin>0 and pin<=9999:
            self._device.pin_settings.pin_number = pin
            self._device.pin_settings.pin_enabled = True
            self._device.pin_settings.save()
        else:
            print('Invalid pin number')

    def set_current_time(self):
        self._device.current_time = dt.datetime.now(dt.timezone.utc).astimezone()

    def set_locale(self):
        self._device.locale = locale.getdefaultlocale()[0].split('_')[0].lower()

    def error(self):
        result = self._device.error
        print("Error:                   0x{:x}".format(result.error))
        print("E9 valve does not close: {}".format(result.e9_valve_does_not_close))
        print("E10 invalid time:        {}".format(result.e10_invalid_time))
        print("E14 low battery:         {}".format(result.e14_low_battery))
        print("E15 very low_battery:    {}".format(result.e15_very_low_battery))
    
    def clear_error(self):
        self._device.error.error = 0

if __name__ == "__main__":
    fire.Fire(CLI)
