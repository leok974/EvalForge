def index_records(records):
    indexed = {}
    for r in records:
        indexed[r['id']] = r
    return indexed

if __name__ == '__main__':
    data = [
        {'id': 'EVT-1', 'type': 'auth', 'val': 1},
        {'id': 'EVT-2', 'type': 'io', 'val': 2}
    ]
    indexed = index_records(data)
    import json
    print(json.dumps(indexed, sort_keys=True))
