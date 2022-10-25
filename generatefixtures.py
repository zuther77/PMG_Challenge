#!/usr/bin/env python3

import csv
import hashlib
import os
import random

DIR = os.path.abspath(os.path.dirname(__file__))
FILES = {
    'clothing.csv': ('Blouses', 'Shirts', 'Tanks', 'Cardigans', 'Pants', 'Capris', '"Gingham" Shorts',),
    'accessories.csv': ('Watches', 'Wallets', 'Purses', 'Satchels',),
    'household_cleaners.csv': ('Kitchen Cleaner', 'Bathroom Cleaner',),
}


def write_file(writer, length, categories):
    writer.writerow(['email_hash', 'category'])
    for i in range(0, length):
        writer.writerow([
            hashlib.sha256(
                'tech+test{}@pmg.com'.format(i).encode('utf-8')).hexdigest(),
            random.choice(categories),
        ])


def main():
    if not os.path.exists('./fixtures'):
        os.makedirs('fixtures')

    for fn, categories in FILES.items():
        with open(os.path.join(DIR, 'fixtures', fn), 'w+', encoding='utf-8') as fh:
            write_file(
                csv.writer(fh, doublequote=False, escapechar='\\',
                           quoting=csv.QUOTE_ALL),
                random.randint(7, 7),
                categories
            )


if __name__ == '__main__':
    main()
