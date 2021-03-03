import pytest

from tests.utils.device_mock import DeviceMock


@pytest.fixture()
def device():
    dev = DeviceMock({
        0x15: b'Danfoss A/S',
        0x17: b'Eco2',
        0x19: b'',
        0x1b: b'B2',
        0x1d: b'2.00',
        0x1f: b'4.1',
        0x21: b''
    })
    return dev


class TestInformation:
    def test_read_information(self, device):
        assert device.information.model_number == 'Eco2'
        assert device.information.firmware_revision == '2.00'
        assert device.information.system_id == ''

    def test_write_information(self, device):
        with pytest.raises(AttributeError, match="attribute is read-only"):
            device.information.manufacturer_name == "HomeMatic"
            device.information.save()

