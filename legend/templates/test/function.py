import azure.functions as func
import json
from {{ function_name }} import main

def test_function_success():
    # Construct a mock HTTP request
    req = func.HttpRequest(
        method='GET',
        body=None,
        url='/api/{{ function_name }}',
        params={}
    )

    # Call the function
    resp = main(req)

    # Check the response
    assert resp.status_code == 200
    assert "success" in resp.get_body().decode().lower()
