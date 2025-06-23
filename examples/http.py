import socket
from datetime import datetime
from typing import Annotated, List
import json

from structure import Structure, Endianes
from structure.types import Data, string, vector


class HTTPHeader(Structure):
    key: Annotated[str, string(terminator=": ")]
    value: Annotated[str, string(terminator="\r\n")]


class HTTPRequest(Structure):
    method: Annotated[str, string(terminator=" ")]
    path: Annotated[str, string(terminator=" ")]
    version: Annotated[str, string(terminator="\r\n")]
    headers: Annotated[List[HTTPHeader], vector(HTTPHeader, terminator="\r\n")]
    data: Data


class HTTPResponse(Structure):
    version: Annotated[str, string(terminator=" ")]
    status_code: Annotated[str, string(terminator=" ")]
    status: Annotated[str, string(terminator="\r\n")]
    headers: Annotated[List[HTTPHeader], vector(HTTPHeader, terminator="\r\n")]
    data: Data


def build_request() -> HTTPRequest:
    return HTTPRequest(
        method="GET",
        path="/json",
        version="HTTP/1.1",
        headers=[
            HTTPHeader(key="Host", value="wtfismyip.com"),
            HTTPHeader(key="User-Agent", value="Structure"),
            HTTPHeader(key="Accept", value="*/*"),
            HTTPHeader(key="Date", value=str(datetime.now())),
        ],
        data=b"",
    )


def main():
    request = build_request()
    raw_request = request.dump(endianes=Endianes.BIG)

    with socket.create_connection(("wtfismyip.com", 80)) as sock:
        sock.sendall(raw_request)
        raw_response = sock.recv(4096)

    response = HTTPResponse.parse(raw_response, endianes=Endianes.BIG)

    print(f"status: {response.status_code} {response.status}")
    print(f"headers:")
    for header in response.headers:
        print(f"\t{header.key} = {header.value}")

    print("data:")
    print(json.dumps(json.loads(response.data), indent=4))


if __name__ == "__main__":
    main()
