def cleanup(items):
    # Fix: Iterate over a copy or use a list comprehension
    return [item for item in items if not item.startswith('OLD-')]

if __name__ == '__main__':
    data = ['OLD-1', 'OLD-2', 'KEEP-1', 'OLD-3', 'KEEP-2']
    result = cleanup(data)
    import json
    print(json.dumps(result))
