"""Fast export contract and command tests; no fonts or film render required."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from verify_export import ExportVerificationError, main, validate_probe, verify_export


GOOD_PROBE = {
    "format": {"format_name": "mov,mp4,m4a,3gp,3g2,mj2", "duration": "31.000000"},
    "streams": [
        {"codec_type": "video", "codec_name": "h264", "width": 1920, "height": 1080,
         "avg_frame_rate": "30/1", "r_frame_rate": "30/1", "duration": "31.000000"},
        {"codec_type": "audio", "codec_name": "aac", "channels": 2,
         "channel_layout": "stereo", "duration": "31.000000"},
    ],
}


class ProbeContractTests(unittest.TestCase):
    def test_default_contract(self):
        validate_probe(deepcopy(GOOD_PROBE))

    def test_custom_contract_and_rational_fps(self):
        probe = deepcopy(GOOD_PROBE)
        video, audio = probe["streams"]
        video.update(width=1280, height=720, avg_frame_rate="30000/1001", r_frame_rate="30000/1001")
        for section in (probe["format"], video, audio):
            section["duration"] = "10.02"
        validate_probe(probe, width=1280, height=720, fps="30000/1001", duration=10)

    def test_contract_failures(self):
        cases = [
            (0, "codec_name", "hevc", "video codec"),
            (0, "width", 1280, "video width"),
            (0, "height", 720, "video height"),
            (0, "avg_frame_rate", "30000/1001", "avg_frame_rate"),
            (0, "r_frame_rate", "24/1", "r_frame_rate"),
            (0, "avg_frame_rate", "0/0", "avg_frame_rate"),
            (0, "avg_frame_rate", float("inf"), "avg_frame_rate"),
            (0, "duration", "30.0", "video duration"),
            (1, "codec_name", "mp3", "audio codec"),
            (1, "channels", 1, "audio channels"),
            (1, "channel_layout", "mono", "audio channel layout"),
            (1, "duration", "5", "audio duration"),
        ]
        for index, field, value, message in cases:
            with self.subTest(field=field, value=value):
                probe = deepcopy(GOOD_PROBE)
                probe["streams"][index][field] = value
                with self.assertRaisesRegex(ExportVerificationError, message):
                    validate_probe(probe)

    def test_missing_and_duplicate_streams(self):
        for index, label in ((0, "video"), (1, "audio")):
            for duplicate in (False, True):
                with self.subTest(stream=label, duplicate=duplicate):
                    probe = deepcopy(GOOD_PROBE)
                    if duplicate:
                        probe["streams"].append(deepcopy(probe["streams"][index]))
                    else:
                        probe["streams"].pop(index)
                    with self.assertRaisesRegex(ExportVerificationError, f"{label} stream count"):
                        validate_probe(probe)

    def test_container_duration_and_invalid_values(self):
        for value in (None, "N/A", "nan", "inf", "-inf", "30.9", "31.1"):
            with self.subTest(value=value):
                probe = deepcopy(GOOD_PROBE)
                probe["format"]["duration"] = value
                with self.assertRaisesRegex(ExportVerificationError, "container duration"):
                    validate_probe(probe)

    def test_wrong_container(self):
        probe = deepcopy(GOOD_PROBE)
        probe["format"]["format_name"] = "matroska,webm"
        with self.assertRaisesRegex(ExportVerificationError, "expected MP4"):
            validate_probe(probe)

    def test_malformed_probe(self):
        for probe in ([], {}, {"streams": None}, {"streams": [1]}, {"format": []}):
            with self.subTest(probe=probe), self.assertRaises(ExportVerificationError):
                validate_probe(probe)

    def test_invalid_expected_contract(self):
        for contract in ({"fps": "0/0"}, {"fps": -1}, {"width": 0}, {"height": -1},
                         {"duration": 0}, {"duration": float("nan")},
                         {"duration_tolerance": -1}, {"duration_tolerance": float("inf")}):
            with self.subTest(contract=contract), self.assertRaises(ExportVerificationError):
                validate_probe(GOOD_PROBE, **contract)

    def test_starter_matches_root(self):
        root = Path(__file__).resolve().parents[1]
        self.assertEqual((root / "verify_export.py").read_bytes(),
                         (root / "skill/assets/starter/verify_export.py").read_bytes())


class ExportToolTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "film with spaces.mp4"
        self.path.write_bytes(b"mocked export")

    @staticmethod
    def result(stdout="", stderr="", returncode=0):
        return subprocess.CompletedProcess([], returncode, stdout, stderr)

    @patch("verify_export.subprocess.run")
    def test_full_decode_and_return_metadata(self, run):
        run.side_effect = [self.result(json.dumps(GOOD_PROBE)), self.result()]
        self.assertEqual(verify_export(self.path), GOOD_PROBE)
        self.assertEqual(run.call_count, 2)
        command = run.call_args_list[1].args[0]
        self.assertEqual(command[0], "ffmpeg")
        self.assertIn("-xerror", command)
        self.assertIn("explode", command)
        self.assertIn(str(self.path), command)
        self.assertEqual(command[-7:], ["-map", "0:v:0", "-map", "0:a:0", "-f", "null", "-"])
        for cap in ("-t", "-to", "-ss", "-frames:v", "copy"):
            self.assertNotIn(cap, command)

    @patch("verify_export.subprocess.run")
    def test_contract_failure_does_not_claim_decode(self, run):
        probe = deepcopy(GOOD_PROBE)
        probe["streams"][1]["duration"] = "3"
        run.return_value = self.result(json.dumps(probe))
        with self.assertRaisesRegex(ExportVerificationError, "audio duration"):
            verify_export(self.path)
        self.assertEqual(run.call_count, 1)

    @patch("verify_export.subprocess.run")
    def test_decode_failures_include_diagnostic(self, run):
        for code in (0, 1):
            with self.subTest(returncode=code):
                run.side_effect = [self.result(json.dumps(GOOD_PROBE)),
                                   self.result(stderr="corrupt decoded frame", returncode=code)]
                with self.assertRaisesRegex(ExportVerificationError, "Full video/audio decode.*corrupt"):
                    verify_export(self.path)

    @patch("verify_export.subprocess.run")
    def test_bad_json_and_probe_failure(self, run):
        for result, message in ((self.result("garbage"), "invalid JSON"),
                                (self.result(stderr="invalid data", returncode=1), "ffprobe failed")):
            with self.subTest(message=message):
                run.return_value = result
                with self.assertRaisesRegex(ExportVerificationError, message):
                    verify_export(self.path)

    @patch("verify_export.subprocess.run", side_effect=FileNotFoundError)
    def test_missing_tool(self, run):
        with self.assertRaisesRegex(ExportVerificationError, "ffprobe is not installed"):
            verify_export(self.path)

    @patch("verify_export.subprocess.run")
    def test_missing_export(self, run):
        with self.assertRaisesRegex(ExportVerificationError, "does not exist"):
            verify_export(self.path.with_name("missing.mp4"))
        run.assert_not_called()

    @patch("verify_export.verify_export", side_effect=ExportVerificationError("bad export"))
    @patch("sys.stderr")
    def test_cli_failure_returns_nonzero(self, stderr, verify):
        self.assertEqual(main([str(self.path)]), 1)
        self.assertIn("bad export", "".join(call.args[0] for call in stderr.write.call_args_list))


if __name__ == "__main__":
    unittest.main()
