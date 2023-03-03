def serialize(data, success: bool, message: str, status_code: int):
    return {
        'data': data,
        'success': success,
        'message': message,
        'statusCode': status_code
    }