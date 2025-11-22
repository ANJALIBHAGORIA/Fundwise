def fingerprint(device_info: dict) -> str:
    return 'fp_' + device_info.get('device_id','unknown')
