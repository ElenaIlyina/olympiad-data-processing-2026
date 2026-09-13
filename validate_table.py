#!/usr/bin/env python3
"""
Script to validate olympiads_2026_27.html against task1 and task6 rules.
"""

import re

def validate(filename='olympiads_2026_27.html'):
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()

    tables = re.findall(r'<table[\s\S]*?</table>', html)
    print(f"Total tables: {len(tables)} (Expected: 3)")

    row_counts = []
    season_2026_count = 0
    venue_errors = []
    bold_errors = []

    for t_idx, t in enumerate(tables):
        rows = re.findall(r'<tr([^>]*)>([\s\S]*?)</tr>', t)
        data_rows = 0
        for r_attr, r_body in rows:
            if 'level-header' in r_attr or 'colspan' in r_body or '<th' in r_body:
                continue
            data_rows += 1
            is_season = 'season-2026' in r_attr
            if is_season:
                season_2026_count += 1

            tds = re.findall(r'<td[^>]*>([\s\S]*?)</td>', r_body)
            if len(tds) >= 8:
                num = tds[0].strip()
                name = re.sub(r'<[^>]+>', '', tds[1]).strip()
                reg_dates = tds[2]
                qual_dates = tds[3]
                fin_dates = tds[4]
                venue = tds[5].strip()

                if not re.match(r'^отбор:\s*[^;]+;\s*финал:\s*.+$', venue):
                    venue_errors.append((t_idx+1, num, name, venue))

                has_b_in_dates = '<b>' in (reg_dates + qual_dates + fin_dates)
                if is_season and not has_b_in_dates:
                    bold_errors.append((t_idx+1, num, name, 'season-2026 but missing <b>'))
                elif not is_season and has_b_in_dates:
                    bold_errors.append((t_idx+1, num, name, 'not season-2026 but contains <b>'))

        row_counts.append(data_rows)

    print(f"Data rows per table: {row_counts} (Expected: [18, 21, 3])")
    print(f"Total data rows: {sum(row_counts)} (Expected: 42)")
    print(f"Season-2026 rows: {season_2026_count}")
    print(f"Venue formatting errors: {len(venue_errors)}")
    for ve in venue_errors:
        print("  Venue error:", ve)
    print(f"Bold date consistency errors: {len(bold_errors)}")
    for be in bold_errors:
        print("  Bold error:", be)

    if len(venue_errors) == 0 and len(bold_errors) == 0 and row_counts == [18, 21, 3]:
        print("\nSUCCESS: All task1 and task6 validation checks passed!")
        return True
    else:
        print("\nFAILURE: Validation errors found!")
        return False

if __name__ == '__main__':
    validate()
