def check_system(pressure):
    if pressure > 80:
        print("WARNING: HIGH PRESSURE")
    else:
        print("STATUS: STABLE")

if __name__ == '__main__':
    current_pressure = 85
    check_system(current_pressure)
