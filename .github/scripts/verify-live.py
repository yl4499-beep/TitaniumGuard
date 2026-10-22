"""Check the public deployment without browser cookies or publisher credentials."""
import argparse
import json
from pathlib import Path
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="The public application URL, including its content GUID")
    args = parser.parse_args()
    base = args.url.rstrip("/") + "/"
    if not base.startswith("https://"):
        parser.error("Use the verified HTTPS application URL")

    def request(path, payload=None):
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        headers = {} if data is None else {"Content-Type": "application/json"}
        req = urllib.request.Request(base + path, data=data, headers=headers)
        with urllib.request.urlopen(req, timeout=45) as response:
            assert response.status == 200, (path, response.status)
            return response.read()

    assert b"TitaniumGuard" in request("")
    assert json.loads(request("health")) == {"status": "ok", "version": "1.0.0"}
    assert b"SwaggerUIBundle" in request("docs")
    assert json.loads(request("openapi.json"))["info"]["title"] == "TitaniumGuard"
    print("PASS anonymous home, health 1.0.0, API docs and OpenAPI", flush=True)

    for name in ("stable_capable", "mean_shift", "stable_incapable"):
        csv = (ROOT / "data" / (name + ".csv")).read_bytes()
        assert request("api/datasets/" + name) == csv, name + ": CSV mismatch"
        actual = json.loads(request("api/analyze", {
            "csv_text": csv.decode("utf-8"), "lsl": 900,
            "baseline_builds": 25, "target": 1.33,
        }))
        expected = json.loads((ROOT / "demo" / (name + ".json")).read_text())
        assert actual == expected, name + ": live result differs from the reviewed full fixture"
        print(f"PASS {name}: full JSON and CSV match; status={actual['status']}; "
              f"signals={actual['signals']['total']}", flush=True)

    try:
        request("api/analyze", {"records": []})
    except urllib.error.HTTPError as error:
        assert error.code == 422, error.code
    else:
        raise AssertionError("Empty input must be rejected")
    print("PASS invalid input: HTTP 422", flush=True)
    print("VERIFIED public TitaniumGuard deployment", flush=True)


if __name__ == "__main__":
    main()
