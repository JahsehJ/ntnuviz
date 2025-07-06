from collections import defaultdict
from pathlib import Path
from sys import argv

import pandas as pd

SHEET_NAME = "cofopdl"
CLASS_ID = "開課代碼"
CLASS_NAME = "中文課程名稱"
TIME_LOCATION = "地點時間"
YEAR = "年"
PERIOD = "節次"
XLS_PATH = "export.xls"
OUTPUT_PATH = "課表.xlsx"
default_periods = list("0123456789") + ["10"] + list("ABCD")
default_weekdays = list("一二三四五")


def main() -> None:
    year = argv[1]

    with open(Path(XLS_PATH), "rb") as f:
        df = pd.read_excel(f, sheet_name=SHEET_NAME)

    timetable = timetable_from_df(df, year)
    timetable_to_df(timetable).to_excel(Path(OUTPUT_PATH))


def timetable_from_df(
    df: pd.DataFrame,
    year: str,
    periods: list[str] = default_periods,
) -> defaultdict[str, defaultdict[str, list[str]]]:
    timetable = defaultdict[str, defaultdict[str, list[str]]](
        lambda: defaultdict[str, list[str]](list)
    )

    for _, row in df.iterrows():
        row_year = row.get(YEAR)
        if pd.notna(row_year) and year not in str(row_year):
            continue

        course_str = f"{row[CLASS_ID]} {row[CLASS_NAME]}"
        raw_time_locations = str(row[TIME_LOCATION]).split(", ")

        for r in raw_time_locations:
            weekday, period_range, _location = r.split(sep=" ", maxsplit=2)
            parts = period_range.split("-")
            start = periods.index(parts[0])
            end = periods.index(parts[-1])

            for period in range(start, end + 1):
                timetable[weekday][str(period)].append(course_str)

    return timetable


def timetable_to_df(
    timetable: defaultdict[str, defaultdict[str, list[str]]],
    periods: list[str] = default_periods,
    weekdays: list[str] = default_weekdays,
) -> pd.DataFrame:
    data = {
        weekday: {
            period: "\n\n".join(courses)
            for period, courses in weekday_periods.items()
        }
        for weekday, weekday_periods in timetable.items()
    }

    df = pd.DataFrame(data, index=periods, columns=weekdays)
    df.index.name = PERIOD

    return df


if __name__ == "__main__":
    main()
