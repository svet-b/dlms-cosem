import pytest

from dlms_cosem import cosem, dlms_data, enumerations
from dlms_cosem.connection import DlmsConnection
from dlms_cosem.protocol import acse, xdlms


@pytest.fixture()
def system_title() -> bytes:
    return b"HEWATEST"


@pytest.fixture()
def meter_system_title() -> bytes:
    return b"uti123457"


@pytest.fixture()
def lls_password() -> bytes:
    return bytes.fromhex("12345678")


@pytest.fixture()
def global_authentication_key() -> bytes:
    return bytes.fromhex("D0D1D2D3D4D5D6D7D8D9DADBDCDDDEDF")


@pytest.fixture()
def global_broadcast_key() -> bytes:
    return bytes.fromhex("0F0E0D0C0B0A09080706050403020100")


@pytest.fixture()
def global_encryption_key() -> bytes:
    return bytes.fromhex("000102030405060708090A0B0C0D0E0F")


@pytest.fixture()
def global_cip_authentication_key() -> bytes:
    return bytes.fromhex("C0C1C2C3C4C5C6C7C8C9CACBCCCDCECF")


@pytest.fixture()
def global_cip_encryption_key() -> bytes:
    return bytes.fromhex("101112131415161718191A1B1C1D1E1F")


@pytest.fixture()
def master_key() -> bytes:
    return bytes.fromhex("00112233445566778899AABBCCDDEEFF")


@pytest.fixture()
def aarq():

    return acse.ApplicationAssociationRequest(
        ciphered=False,
        system_title=None,
        public_cert=None,
        authentication=None,
        authentication_value=None,
        user_information=acse.UserInformation(
            content=xdlms.InitiateRequest(
                proposed_conformance=xdlms.Conformance(
                    general_protection=False,
                    general_block_transfer=False,
                    delta_value_encoding=False,
                    attribute_0_supported_with_set=False,
                    priority_management_supported=False,
                    attribute_0_supported_with_get=False,
                    block_transfer_with_get_or_read=True,
                    block_transfer_with_set_or_write=True,
                    block_transfer_with_action=True,
                    multiple_references=True,
                    data_notification=False,
                    access=False,
                    get=True,
                    set=True,
                    selective_access=True,
                    event_notification=False,
                    action=True,
                ),
                proposed_quality_of_service=0,
                client_max_receive_pdu_size=65535,
                proposed_dlms_version_number=6,
                response_allowed=True,
                dedicated_key=None,
            )
        ),
    )


@pytest.fixture()
def aare():
    from dlms_cosem import enumerations
    from dlms_cosem.protocol import acse
    from dlms_cosem.protocol.xdlms import Conformance, InitiateResponse

    return acse.ApplicationAssociationResponse(
        result=enumerations.AssociationResult.ACCEPTED,
        result_source_diagnostics=enumerations.AcseServiceUserDiagnostics.NULL,
        ciphered=False,
        authentication=None,
        system_title=None,
        public_cert=None,
        authentication_value=None,
        user_information=acse.UserInformation(
            content=InitiateResponse(
                negotiated_conformance=Conformance(
                    general_protection=False,
                    general_block_transfer=False,
                    delta_value_encoding=False,
                    attribute_0_supported_with_set=False,
                    priority_management_supported=True,
                    attribute_0_supported_with_get=False,
                    block_transfer_with_get_or_read=True,
                    block_transfer_with_set_or_write=False,
                    block_transfer_with_action=False,
                    multiple_references=False,
                    data_notification=False,
                    access=False,
                    get=True,
                    set=True,
                    selective_access=True,
                    event_notification=True,
                    action=True,
                ),
                server_max_receive_pdu_size=500,
                negotiated_dlms_version_number=6,
                negotiated_quality_of_service=0,
            )
        ),
        implementation_information=None,
        responding_ap_invocation_id=None,
        responding_ae_invocation_id=None,
    )


@pytest.fixture()
def ciphered_hls_aare(
    aare: acse.ApplicationAssociationResponse, meter_system_title: bytes
) -> acse.ApplicationAssociationResponse:
    aare.ciphered = True
    aare.system_title = meter_system_title
    aare.authentication = enumerations.AuthenticationMechanism.HLS_GMAC
    return aare


@pytest.fixture()
def rlrq() -> acse.ReleaseRequest:

    data = bytes.fromhex("6203800100")  # Normal no user-information
    rlrq = acse.ReleaseRequest.from_bytes(data)
    return rlrq


@pytest.fixture()
def rlre() -> acse.ReleaseResponse:

    data = b"c\x03\x80\x01\x00"
    rlre = acse.ReleaseResponse.from_bytes(data)
    return rlre


@pytest.fixture()
def get_request() -> xdlms.GetRequestNormal:

    # invocation counter
    return xdlms.GetRequestNormal(
        cosem_attribute=cosem.CosemAttribute(
            interface=enumerations.CosemInterface.DATA,
            instance=cosem.Obis(0, 0, 0x2B, 1, 0),
            attribute=2,
        )
    )


@pytest.fixture()
def set_request() -> xdlms.SetRequestNormal:

    # invocation counter
    return xdlms.SetRequestNormal(
        cosem_attribute=cosem.CosemAttribute(
            interface=enumerations.CosemInterface.CLOCK,
            instance=cosem.Obis(a=0, b=0, c=1, d=0, e=0, f=255),
            attribute=2,
        ),
        data=b"\t\x0c\x07\xe5\x01\x18\xff\x0e09P\xff\xc4\x00",
        access_selection=None,
        invoke_id_and_priority=xdlms.InvokeIdAndPriority(
            invoke_id=1, confirmed=True, high_priority=True
        ),
    )


@pytest.fixture()
def set_response() -> xdlms.SetResponseNormal:
    return xdlms.SetResponseNormal(
        result=enumerations.DataAccessResult.SUCCESS,
        invoke_id_and_priority=xdlms.InvokeIdAndPriority(
            invoke_id=1, confirmed=True, high_priority=True
        ),
    )


@pytest.fixture()
def action_request() -> xdlms.ActionRequestNormal:
    return xdlms.ActionRequestNormal(
        cosem_method=cosem.CosemMethod(
            interface=enumerations.CosemInterface.DISCONNECT_CONTROL,
            instance=cosem.Obis.from_string("0.0.96.3.10.255"),
            method=1,
        ),
        data=dlms_data.UnsignedLongData(0).to_bytes(),
        invoke_id_and_priority=xdlms.InvokeIdAndPriority(
            invoke_id=1, confirmed=True, high_priority=True
        ),
    )


@pytest.fixture()
def exception_response() -> xdlms.ExceptionResponse:

    return xdlms.ExceptionResponse(
        state_error=enumerations.StateException.SERVICE_NOT_ALLOWED,
        service_error=enumerations.ServiceException.OPERATION_NOT_POSSIBLE,
    )


@pytest.fixture()
def connection_with_hls(
    system_title, global_encryption_key, global_authentication_key
) -> DlmsConnection:

    return DlmsConnection(
        client_system_title=system_title,
        authentication_method=enumerations.AuthenticationMechanism.HLS_GMAC,
        global_encryption_key=global_encryption_key,
        global_authentication_key=global_authentication_key,
        security_suite=0,
    )
