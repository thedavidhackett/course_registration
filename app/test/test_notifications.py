from db import notifications

def test_get_notification():
    test_notification = notifications.find_one({"student_id": 5, "type": "info"})
    assert test_notification['student_id'] == 5
