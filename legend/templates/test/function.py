import azure.functions as func
import function_app as app

def test_{{ function_name }}_success():
    # Construct a mock HTTP request
    req = func.HttpRequest(
        method='GET',
        body=None,
        url='/api/{{ function_name }}',
        params={'name': 'Test'}
    )

    # Call the function
    resp = app.{{ function_name }}(req)

    # Check the response
    assert resp.status_code == 200
    assert "success" in resp.get_body().decode().lower()
