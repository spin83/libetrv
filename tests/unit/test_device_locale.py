import pytest

from tests.utils.device_mock import DeviceMock


@pytest.fixture()
def device():
    dev = DeviceMock({
        0x3c: b''
    })
    return dev


class TestEncryptionTemperature:
    def test_read_locale(self, device):
        with pytest.raises(AttributeError, match="attribute is write-only"):
            device.locale == "en"

    def test_write_name(self, device):
        device.locale = "pl"
        assert device.fields['locale'].raw_data[0x3c].locale == b'pl'
        assert device.ble_device.handlers_history.pop() == 0x3c
        assert device.ble_device.sent_data_history.pop() == bytes.fromhex('5786fd7cb50eb499')

