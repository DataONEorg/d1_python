import argparse
import importlib

# import cryptography
import cryptography.x509
import mock
import responses

import d1_common.cert.x509

import d1_test.d1_test_case
import d1_test.mock_api.echo_credentials
import freezegun

@freezegun.freeze_time('1999-01-01')
class TestDataONEBaseClient(d1_test.d1_test_case.D1TestCase):
    def _cmd(self, module_name, **cmd_arg_dict):
        cmd = importlib.import_module(module_name)

        with mock.patch(
            "argparse.ArgumentParser.parse_args",
            return_value=argparse.Namespace(**cmd_arg_dict, debug=True),
        ):

            with mock.patch(
                "d1_common.cert.x509.input_key_passphrase",
                return_value=b"valid_passphrase",
            ):

                return cmd.main()

    def test_1000(self):
        """cert-create-ca.py: Creates valid CA file."""
        with d1_test.d1_test_case.temp_file_name(".pem") as pem_path:
            self._cmd("d1_util.cert_create_ca", common_name="localCA", ca_path=pem_path)
            cert_obj = d1_common.cert.x509.deserialize_pem_file(pem_path)
            self.sample.assert_equals(cert_obj, "gen_ca")

    def test_1010(self):
        """cert-create-csr.py: Creates valid CSR file."""
        with d1_test.d1_test_case.temp_file_name(".pem") as pem_path:
            self._cmd(
                "d1_util.cert_create_csr", node_urn="urn:node:XXYY", csr_path=pem_path
            )
            cert_obj = d1_common.cert.x509.load_csr(pem_path)
            assert isinstance(cert_obj, cryptography.x509.CertificateSigningRequest)

    def test_1020(self):
        """cert-create-csr.py: Creates valid CSR file."""
        with d1_test.d1_test_case.temp_file_name(".pem") as pem_path:
            self._cmd(
                "d1_util.cert_create_csr", node_urn="urn:node:XXYY", csr_path=pem_path
            )
            cert_obj = d1_common.cert.x509.load_csr(pem_path)
            assert isinstance(cert_obj, cryptography.x509.CertificateSigningRequest)

    @responses.activate
    def test_1030(self):
        """cert-check-cn.py: Submits valid requst to CN."""
        d1_test.mock_api.echo_credentials.add_callback(
            d1_test.d1_test_case.MOCK_CN_BASE_URL
        )
        self._cmd(
            "d1_util.cert_check_cn",
            d1client__base_url=d1_test.d1_test_case.MOCK_CN_BASE_URL,
            d1client__cert_pem_path=self.test_files.get_abs_test_file_path(
                "cert/cert_with_simple_subject_info.pem"
            ),
        )

    def test_1040(self):
        """cert-check-local.py: Extracts cert with subject info."""
        with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
            self._cmd(
                "d1_util.cert_check_local",
                cert_pem_path=self.test_files.get_abs_test_file_path(
                    "cert/cert_with_simple_subject_info.pem"
                ),
            )
            self.sample.assert_equals(out_stream.getvalue(), "cert_check_local")

    def test_1050(self):
        """check-scimeta-indexing.py: Submits valid request to CN."""
        with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
            self._cmd(
                "d1_util.cert_check_local",
                cert_pem_path=self.test_files.get_abs_test_file_path(
                    "cert/cert_with_simple_subject_info.pem"
                ),
            )
            self.sample.assert_equals(out_stream.getvalue(), "cert_check_local")


"xml/scimeta_eml_valid.xml"
