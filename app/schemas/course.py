from pydantic import BaseModel, ConfigDict


class CourseSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    summary: str
    category: str
    thumbnail_url: str | None
    instructor_name: str
    price_krw: int
    level: str
    duration_minutes: int


class CourseDetail(CourseSummary):
    description: str
