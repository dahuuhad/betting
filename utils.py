def convert_american_to_decimal(american_odd):
    if american_odd > 0:
        return (american_odd/100) + 1
    else:
        return (100.0 / american_odd*-1.0) + 1

def convert_decimal_to_american(decimal_odd):
    if decimal_odd >= 2.00:
        return int((decimal_odd - 1.0) * 100)
    else:
        return int((-100)/(decimal_odd - 1.0))
