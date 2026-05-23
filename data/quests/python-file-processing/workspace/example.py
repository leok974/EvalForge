def sum_manifest(filename):
    total = 0
    with open(filename, 'r') as f:
        for line in f:
            if line.strip():
                total += int(line.strip())
    return total

if __name__ == '__main__':
    result = sum_manifest('manifest.txt')
    print(f"TOTAL_PARTS={result}")
