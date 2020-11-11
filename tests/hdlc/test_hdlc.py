import pytest

from dlms_cosem.protocol import hdlc, crc


def test_hdlc_frame_format_field_from_bytes():
    in_bytes = bytes.fromhex("a01d")
    f = hdlc.DlmsHdlcFrameFormatField.from_bytes(in_bytes)
    assert f.length == 29
    assert not f.segmented


def test_hdlc_frame_format_filed_from_bytes_segmented():
    in_bytes = bytes.fromhex("a81d")
    f = hdlc.DlmsHdlcFrameFormatField.from_bytes(in_bytes)
    assert f.length == 29
    assert f.segmented


def test_hdlc_frame_format_raises_value_error_too_long():
    with pytest.raises(ValueError):
        f = hdlc.DlmsHdlcFrameFormatField(length=999999, segmented=False)


def test_hdlc_frame_format_to_bytes_not_segmented():
    f = hdlc.DlmsHdlcFrameFormatField(length=29, segmented=False)
    assert f.to_bytes().hex() == "a01d"


def test_hdlc_frame_format_to_bytes_segmented():
    f = hdlc.DlmsHdlcFrameFormatField(length=29, segmented=True)
    assert f.to_bytes().hex() == "a81d"


class TestHdlcAddress:
    def test_find_address(self):
        frame = "7ea87e210396a4090f01160002020f02160002020f03160002020f04160002020f05160002020f0616000204120017110009060000160000ff0202010902030f0116010002030f0216010002030f0316010002030f0416010002030f0516010002030f0616010002030f0716010002030f0816010002030f09160100016ff37e"
        frame_bytes = bytes.fromhex(frame)
        destination_address, source_address = hdlc.HdlcAddress.find_address(frame_bytes)
        assert destination_address == (16, None, 1)
        assert source_address == (1, None, 1)

    @pytest.mark.parametrize(
        "address,resulting_bytes",
        [
            ((1, None, "client"), b"\x03"),
            ((16, None, "client"), b"\x21"),
            ((0b1001010, None, "server"), b"\x95"),
            ((0b0100101, None, "client"), b"\x4b"),
            ((1, 17, "server"), b"\x02\x23")
        ],
        # TODO: need to find references of multiy byte addresses to test.
    )
    def test_client_address_just_logical(self, address, resulting_bytes):
        add = hdlc.HdlcAddress(
            logical_address=address[0],
            physical_address=address[1],
            address_type=address[2],
        )
        assert add.to_bytes() == resulting_bytes


class TestCrc:
    def test_crc(self):

        data = "033f"
        correct_crc = "5bec"

        _crc = crc.CRCCCITT()
        result = _crc.calculate_for(bytes.fromhex(data))
        assert result == bytes.fromhex(correct_crc)


class TestSnrmFrame:
    def test_parses_correct(self):
        out_data = bytes.fromhex("7ea00802232193bd647e")
        destination_address = hdlc.HdlcAddress(logical_address=1, physical_address=17,
                                               address_type="server")

        # Public client
        source_address = hdlc.HdlcAddress(logical_address=16, physical_address=None,
                                          address_type="client")
        snrm = hdlc.SetNormalResponseModeFrame(destination_address, source_address)

        assert snrm.to_bytes() == out_data


class TestUAFrame:
    def test_parser_correctly(self):
        out_data = bytes.fromhex('7EA01F21022373E6C781801205019A06019A070400000001080400000001CCA27E')
        # from device so public client is destination address.
        source_address = hdlc.HdlcAddress(logical_address=1, physical_address=17,
                                               address_type="server")

        # Public client
        destination_address = hdlc.HdlcAddress(logical_address=16, physical_address=None,
                                          address_type="client")

        information = out_data[9:-3]
        ua = hdlc.UnumberedAcknowlegmentFrame(destination_address, source_address, information)
        print(ua.hcs.hex())
        print(ua.to_bytes().hex())
        print(out_data.hex())
        assert ua.to_bytes() == out_data

    def test_from_bytes(self):

        in_data = b'~\xa0\x1f!\x02#s\xe6\xc7\x81\x80\x12\x05\x01\x9a\x06\x01\x9a\x07\x04\x00\x00\x00\x01\x08\x04\x00\x00\x00\x01\xcc\xa2~'
        frame = hdlc.UnumberedAcknowlegmentFrame.from_bytes(in_data)
        assert in_data == frame.to_bytes()







