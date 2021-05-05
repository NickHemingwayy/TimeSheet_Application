# Calculates totals from column lists passed in
def calc(col):
    coltotal = 0.00
    for i in col:
        if i != '' and i.replace('.', '', 1).isdigit():
            coltotal += float(i)
            print(coltotal)
    return str("%.2f" % coltotal)  # returned to be displayed as total Hour string at bottom of page
