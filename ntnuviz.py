from collections import defaultdict
from pathlib import Path
from re import search
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

    timetable, nonscheduled = timetable_from_df(df, year)
    if nonscheduled:
        print("下列為不定期課程，請自行查詢：")
        for c in nonscheduled:
            print(c)
    timetable_to_df(timetable).to_excel(Path(OUTPUT_PATH))


def defaultdict_list_factory() -> list[list[str]]:
    return [[] for _ in default_periods]


def timetable_from_df(
    df: pd.DataFrame,
    year: str,
    periods: list[str] = default_periods,
) -> tuple[defaultdict[str, list[list[str]]], list[str]]:
    """Return a timetable and nonscheduled courses."""
    timetable = defaultdict[str, list[list[str]]](defaultdict_list_factory)
    nonscheduled_courses: list[str] = []

    for _, row in df.iterrows():
        row_year = row.get(YEAR)
        if pd.notna(row_year) and year not in str(row_year):
            continue

        course_str = f"{row[CLASS_ID]} {row[CLASS_NAME]}"
        raw_time_locations = str(row[TIME_LOCATION]).split(", ")

        # "四 2-3 和平 誠101", "四 2 和平 誠101", "◎面授/同步", "◎密集課程"...
        for r in raw_time_locations:
            weekday_period = search(
                r"([一二三四五])\s([0-9A-Za-z]+(?:-[0-9A-Za-z]+)?)", r
            )
            if not weekday_period:
                nonscheduled_courses.append(course_str)
                continue

            weekday, period_range = weekday_period.groups()
            parts = period_range.split("-")
            start = periods.index(parts[0])
            end = periods.index(parts[-1])

            for period in range(start, end + 1):
                timetable[weekday][period].append(course_str)

    return timetable, nonscheduled_courses


def timetable_to_df(
    timetable: defaultdict[str, list[list[str]]],
    periods: list[str] = default_periods,
    weekdays: list[str] = default_weekdays,
) -> pd.DataFrame:
    data = {
        weekday: ["\n\n".join(courses) for courses in weekday_periods]
        for weekday, weekday_periods in timetable.items()
    }

    df = pd.DataFrame(data, index=periods, columns=weekdays)
    df.index.name = PERIOD

    return df


if __name__ == "__main__":
    main()
