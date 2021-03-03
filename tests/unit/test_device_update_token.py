import pytest

from tests.utils.device_mock import DeviceMock


@pytest.fixture()
def device():
    dev = DeviceMock({
        0x42: bytes.fromhex('2ede51c3ba895f695ad640f9'),
    })
    return dev


class TestUpdateToken:
    def test_read_update_token(self, device):
        assert device.update_token == 'Lt5Rw7qJX2la1kD5'


    def test_write_update_token(self, device):
        with pytest.raises(AttributeError, match="attribute is read-only"):
            device.update_token = 'x7OtEJw3g5qzkf0j'

