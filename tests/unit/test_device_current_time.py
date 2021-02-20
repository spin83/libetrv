import pytest
import datetime as dt

from tests.utils.device_mock import DeviceMock

@pytest.fixture()
def device():
    dev = DeviceMock({
        0x36: bytes.fromhex('a6acf6136e7c47aa')
    })
    return dev

class TestEncryptionCurrentTime:
    def test_current_time(self, device):
        assert device.current_time == dt.datetime(2021, 2, 13, 11, 56, 12, tzinfo=dt.timezone(dt.timedelta(seconds=3600)))

    def test_set_time(self, device):
        device.current_time = dt.datetime(2021, 2, 13, 21, 56, 12, tzinfo=dt.timezone(dt.timedelta(seconds=-3600)))

        assert device.ble_device.handlers_history.pop() == 0x36
        assert device.fields['current_time'].raw_data[0x36].time_local == 1613256972
        assert device.fields['current_time'].raw_data[0x36].time_offset == -3600
        assert device.ble_device.sent_data_history.pop() == bytes.fromhex('d86fd79c33107d15')

