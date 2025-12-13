from enum import Enum


class OrderBy(Enum):
    # 생성 날짜 기준 오름차순, 내림차순
    ASC = "asc"
    DESC = "desc"
    # 최근 대화한 순서대로
    CURR = "curr"
