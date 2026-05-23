def filter_parts(parts):
    for part in parts:
        if not part.startswith('DEF-'):
            print(part)

if __name__ == '__main__':
    batch = ['UNIT-101', 'DEF-001', 'UNIT-102', 'DEF-002', 'UNIT-103']
    filter_parts(batch)
