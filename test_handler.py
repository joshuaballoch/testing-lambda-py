from handler import call

def test_hello_world():
    expected_response = {
        "statusCode": 200,
        "body": "{\"message\": \"Hello World!\"}"
    }
    assert call(None,None) == expected_response

