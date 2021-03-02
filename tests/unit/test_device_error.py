import pytest

from tests.utils.device_mock import DeviceMock


@pytest.fixture()
def device():
    dev = DeviceMock({
        0x39: bytes.fromhex('ac1ed84128033e8e')
    })
    return dev


class TestEncryptionError:
    def test_read_error(self, device):
        assert device.error.error == 0x2200
        assert device.error.e10_invalid_time == True
        assert device.error.e14_low_battery == True
        assert device.error.e15_very_low_battery == False

    def test_write_error(self, device):
        device.error.error = 0    
        assert device.fields['error'].raw_data[0x39].error == 0
        assert device.ble_device.handlers_history.pop() == 0x39
        assert device.ble_device.sent_data_history.pop() == bytes.fromhex('19854b04365f7f62')

