"""Tests for search schemas."""

import pytest
from pydantic import ValidationError

from src.job_search_ai_assistant.api.schemas.search import (
    JobListing,
    SalaryRange,
    SearchFilters,
    SearchRequest,
    SearchResponse,
)


class TestSalaryRange:
    """Test SalaryRange schema."""

    def test_salary_range_all_fields(self):
        """Test SalaryRange with all fields populated."""
        salary = SalaryRange(min_amount=50000.0, max_amount=80000.0, currency="USD")

        assert salary.min_amount == 50000.0
        assert salary.max_amount == 80000.0
        assert salary.currency == "USD"

    def test_salary_range_optional_fields(self):
        """Test SalaryRange with all optional fields as None."""
        salary = SalaryRange()

        assert salary.min_amount is None
        assert salary.max_amount is None
        assert salary.currency is None

    def test_salary_range_partial_fields(self):
        """Test SalaryRange with some fields populated."""
        salary = SalaryRange(min_amount=60000.0, currency="EUR")

        assert salary.min_amount == 60000.0
        assert salary.max_amount is None
        assert salary.currency == "EUR"

    def test_salary_range_only_max(self):
        """Test SalaryRange with only max amount."""
        salary = SalaryRange(max_amount=100000.0)

        assert salary.min_amount is None
        assert salary.max_amount == 100000.0
        assert salary.currency is None

    def test_salary_range_only_currency(self):
        """Test SalaryRange with only currency."""
        salary = SalaryRange(currency="GBP")

        assert salary.min_amount is None
        assert salary.max_amount is None
        assert salary.currency == "GBP"

    def test_salary_range_different_currencies(self):
        """Test SalaryRange with various currency codes."""
        currencies = ["USD", "EUR", "GBP", "UAH", "PLN", "CAD", "AUD"]
        for currency in currencies:
            salary = SalaryRange(currency=currency)
            assert salary.currency == currency

    def test_salary_range_float_precision(self):
        """Test SalaryRange with float precision."""
        salary = SalaryRange(min_amount=75000.50, max_amount=125000.75)

        assert salary.min_amount == 75000.50
        assert salary.max_amount == 125000.75

    def test_salary_range_zero_values(self):
        """Test SalaryRange with zero values."""
        salary = SalaryRange(min_amount=0.0, max_amount=0.0)

        assert salary.min_amount == 0.0
        assert salary.max_amount == 0.0


class TestSearchFilters:
    """Test unified SearchFilters schema."""

    def test_search_filters_all_fields(self):
        """Test SearchFilters with all fields populated."""
        filters = SearchFilters(
            keywords=["python", "django", "postgresql"],
            location="Kyiv, Ukraine",
            salary_range=SalaryRange(min_amount=80000.0, max_amount=120000.0, currency="USD"),
            remote=True,
            experience_level="senior",
            job_type="full-time",
            salary_min=3000.0,
            salary_max=5000.0,
        )

        assert filters.keywords == ["python", "django", "postgresql"]
        assert filters.location == "Kyiv, Ukraine"
        assert filters.salary_range.min_amount == 80000.0
        assert filters.salary_range.max_amount == 120000.0
        assert filters.salary_range.currency == "USD"
        assert filters.remote is True
        assert filters.experience_level == "senior"
        assert filters.job_type == "full-time"
        assert filters.salary_min == 3000.0
        assert filters.salary_max == 5000.0

    def test_search_filters_all_optional(self):
        """Test SearchFilters with all fields as None."""
        filters = SearchFilters()

        assert filters.keywords is None
        assert filters.location is None
        assert filters.salary_range is None
        assert filters.remote is None
        assert filters.experience_level is None
        assert filters.job_type is None
        assert filters.salary_min is None
        assert filters.salary_max is None

    def test_search_filters_keywords_only(self):
        """Test SearchFilters with only keywords."""
        filters = SearchFilters(keywords=["javascript", "react", "nodejs"])

        assert filters.keywords == ["javascript", "react", "nodejs"]
        assert filters.location is None
        assert filters.remote is None

    def test_search_filters_location_and_remote(self):
        """Test SearchFilters with location and remote."""
        filters = SearchFilters(location="San Francisco, CA", remote=False)

        assert filters.location == "San Francisco, CA"
        assert filters.remote is False
        assert filters.keywords is None

    def test_search_filters_salary_range_vs_min_max(self):
        """Test SearchFilters with both salary_range and salary_min/max."""
        filters = SearchFilters(
            salary_range=SalaryRange(min_amount=100000, max_amount=150000, currency="USD"),
            salary_min=2000,
            salary_max=3000,
        )

        # Both can coexist
        assert filters.salary_range.min_amount == 100000
        assert filters.salary_range.max_amount == 150000
        assert filters.salary_min == 2000
        assert filters.salary_max == 3000

    def test_search_filters_experience_levels(self):
        """Test SearchFilters with different experience levels."""
        for level in ["entry", "mid", "senior", "lead"]:
            filters = SearchFilters(experience_level=level)
            assert filters.experience_level == level

    def test_search_filters_job_types(self):
        """Test SearchFilters with different job types."""
        for job_type in ["full-time", "part-time", "contract", "internship"]:
            filters = SearchFilters(job_type=job_type)
            assert filters.job_type == job_type

    def test_search_filters_empty_keywords_list(self):
        """Test SearchFilters with empty keywords list."""
        filters = SearchFilters(keywords=[])
        assert filters.keywords == []
        assert len(filters.keywords) == 0

    def test_search_filters_config_example(self):
        """Test SearchFilters matching the example in Config."""
        filters = SearchFilters(
            keywords=["python", "fastapi", "postgresql"],
            location="Kyiv, Ukraine",
            salary_range=SalaryRange(min_amount=100000, max_amount=150000, currency="USD"),
            remote=True,
            experience_level="senior",
            job_type="full-time",
            salary_min=3000,
            salary_max=5000,
        )

        assert filters.keywords == ["python", "fastapi", "postgresql"]
        assert filters.location == "Kyiv, Ukraine"
        assert filters.remote is True
        assert filters.experience_level == "senior"
        assert filters.job_type == "full-time"


class TestJobListing:
    """Test JobListing schema."""

    def test_job_listing_all_fields(self):
        """Test JobListing with all fields populated."""
        job = JobListing(
            id="job-123",
            title="Senior Python Developer",
            company="Tech Corp",
            location="San Francisco, CA",
            description="We are looking for an experienced Python developer...",
            url="https://example.com/jobs/123",
            posted_date="2024-01-15",
            salary="$120,000 - $180,000",
            source="linkedin",
        )

        assert job.id == "job-123"
        assert job.title == "Senior Python Developer"
        assert job.company == "Tech Corp"
        assert job.location == "San Francisco, CA"
        assert job.description == "We are looking for an experienced Python developer..."
        assert str(job.url) == "https://example.com/jobs/123"
        assert job.posted_date == "2024-01-15"
        assert job.salary == "$120,000 - $180,000"
        assert job.source == "linkedin"

    def test_job_listing_required_fields_only(self):
        """Test JobListing with only required fields."""
        job = JobListing(
            id="job-456",
            title="Software Engineer",
            company="StartupXYZ",
            url="https://example.com/jobs/456",
            source="dou",
        )

        assert job.id == "job-456"
        assert job.title == "Software Engineer"
        assert job.company == "StartupXYZ"
        assert str(job.url) == "https://example.com/jobs/456"
        assert job.source == "dou"
        assert job.location is None
        assert job.description is None
        assert job.posted_date is None
        assert job.salary is None

    def test_job_listing_missing_required_fields(self):
        """Test JobListing validation with missing required fields."""
        with pytest.raises(ValidationError) as exc_info:
            JobListing(
                title="Developer",
                company="Company",
                # Missing: id, url, source
            )

        errors = exc_info.value.errors()
        missing_fields = {error["loc"][0] for error in errors}
        assert "id" in missing_fields
        assert "url" in missing_fields
        assert "source" in missing_fields

    def test_job_listing_invalid_url(self):
        """Test JobListing with invalid URL."""
        with pytest.raises(ValidationError) as exc_info:
            JobListing(id="123", title="Dev", company="Co", url="not-a-url", source="linkedin")

        errors = exc_info.value.errors()
        assert any(error["loc"][0] == "url" for error in errors)

    def test_job_listing_different_sources(self):
        """Test JobListing with different source platforms."""
        sources = ["linkedin", "dou", "djinni", "workua", "indeed", "glassdoor"]
        for source in sources:
            job = JobListing(
                id=f"job-{source}",
                title="Developer",
                company="Company",
                url=f"https://example.com/{source}",
                source=source,
            )
            assert job.source == source

    def test_job_listing_config_example(self):
        """Test JobListing matching the example in Config."""
        job = JobListing(
            id="job-123",
            title="Senior Python Developer",
            company="Tech Corp",
            url="https://example.com/jobs/123",
            source="linkedin",
            location="Kyiv, Ukraine",
            description="We are looking for an experienced Python developer...",
            posted_date="2024-01-15",
            salary="$100,000 - $150,000",
        )

        assert job.id == "job-123"
        assert job.title == "Senior Python Developer"
        assert job.company == "Tech Corp"
        assert job.location == "Kyiv, Ukraine"


class TestSearchRequest:
    """Test SearchRequest schema."""

    def test_search_request_with_all_fields(self):
        """Test SearchRequest with all fields populated."""
        filters = SearchFilters(keywords=["python", "django"], location="Kyiv", remote=True, experience_level="senior")
        request = SearchRequest(
            query="python developer",
            platforms=["linkedin", "dou", "djinni"],
            filters=filters,
        )

        assert request.query == "python developer"
        assert request.platforms == ["linkedin", "dou", "djinni"]
        assert request.filters.keywords == ["python", "django"]
        assert request.filters.location == "Kyiv"
        assert request.filters.remote is True

    def test_search_request_default_platforms(self):
        """Test SearchRequest with default platforms value."""
        request = SearchRequest(query="java developer")

        assert request.query == "java developer"
        assert request.platforms == ["all"]
        assert request.filters is None

    def test_search_request_empty_platforms_list(self):
        """Test SearchRequest with empty platforms list."""
        request = SearchRequest(
            query="frontend developer",
            platforms=[],
        )

        assert request.query == "frontend developer"
        assert request.platforms == []
        assert request.filters is None

    def test_search_request_missing_query(self):
        """Test SearchRequest validation with missing query."""
        with pytest.raises(ValidationError) as exc_info:
            SearchRequest()

        errors = exc_info.value.errors()
        assert any(error["loc"][0] == "query" for error in errors)

    def test_search_request_empty_query(self):
        """Test SearchRequest validation with empty query."""
        with pytest.raises(ValidationError) as exc_info:
            SearchRequest(query="")

        errors = exc_info.value.errors()
        assert any(error["loc"][0] == "query" for error in errors)

    def test_search_request_with_filters_no_platforms(self):
        """Test SearchRequest with filters but default platforms."""
        filters = SearchFilters(
            experience_level="junior",
            job_type="internship",
            salary_max=1500,
        )
        request = SearchRequest(
            query="python intern",
            filters=filters,
        )

        assert request.query == "python intern"
        assert request.platforms == ["all"]
        assert request.filters.experience_level == "junior"
        assert request.filters.job_type == "internship"
        assert request.filters.salary_max == 1500

    def test_search_request_config_example(self):
        """Test SearchRequest matching the example in Config."""
        request = SearchRequest(
            query="python developer",
            platforms=["linkedin", "dou"],
            filters=SearchFilters(
                keywords=["python", "django"],
                location="Kyiv",
                remote=True,
                experience_level="senior",
                job_type="full-time",
            ),
        )

        assert request.query == "python developer"
        assert request.platforms == ["linkedin", "dou"]
        assert request.filters.keywords == ["python", "django"]
        assert request.filters.location == "Kyiv"

    def test_search_request_platform_examples(self):
        """Test SearchRequest with various platform combinations."""
        platform_sets = [
            ["all"],
            ["linkedin", "dou"],
            ["djinni", "workua"],
            ["linkedin", "dou", "djinni", "workua"],
        ]

        for platforms in platform_sets:
            request = SearchRequest(query="test query", platforms=platforms)
            assert request.platforms == platforms


class TestSearchResponse:
    """Test SearchResponse schema."""

    def test_search_response_with_jobs(self):
        """Test SearchResponse with multiple jobs."""
        jobs = [
            JobListing(
                id="1",
                title="Backend Developer",
                company="Company A",
                url="https://example.com/job/1",
                source="linkedin",
                location="Remote",
                salary="$80k-$120k",
            ),
            JobListing(
                id="2",
                title="Frontend Developer",
                company="Company B",
                url="https://example.com/job/2",
                source="dou",
                description="React developer needed",
            ),
        ]

        response = SearchResponse(
            jobs=jobs,
            total_count=2,
            query="developer",
            platforms=["linkedin", "dou"],
        )

        assert len(response.jobs) == 2
        assert response.total_count == 2
        assert response.query == "developer"
        assert response.platforms == ["linkedin", "dou"]
        assert response.jobs[0].title == "Backend Developer"
        assert response.jobs[1].title == "Frontend Developer"

    def test_search_response_empty_results(self):
        """Test SearchResponse with no jobs."""
        response = SearchResponse(
            jobs=[],
            total_count=0,
            query="very specific query",
            platforms=["all"],
        )

        assert response.jobs == []
        assert response.total_count == 0
        assert response.query == "very specific query"
        assert response.platforms == ["all"]

    def test_search_response_validation_missing_fields(self):
        """Test SearchResponse validation with missing required fields."""
        with pytest.raises(ValidationError) as exc_info:
            SearchResponse(
                jobs=[],
                total_count=0,
                # Missing: query, platforms
            )

        errors = exc_info.value.errors()
        missing_fields = {error["loc"][0] for error in errors}
        assert "query" in missing_fields
        assert "platforms" in missing_fields

    def test_search_response_single_platform(self):
        """Test SearchResponse with single platform."""
        job = JobListing(
            id="123",
            title="QA Engineer",
            company="TestCo",
            url="https://example.com/qa/123",
            source="workua",
        )

        response = SearchResponse(
            jobs=[job],
            total_count=1,
            query="QA engineer",
            platforms=["workua"],
        )

        assert len(response.jobs) == 1
        assert response.total_count == 1
        assert response.platforms == ["workua"]
        assert response.jobs[0].source == "workua"

    def test_search_response_negative_total_count(self):
        """Test SearchResponse validation with negative total_count."""
        with pytest.raises(ValidationError) as exc_info:
            SearchResponse(jobs=[], total_count=-1, query="test", platforms=["all"])

        errors = exc_info.value.errors()
        assert any(error["loc"][0] == "total_count" for error in errors)

    def test_search_response_total_count_mismatch(self):
        """Test SearchResponse with total_count different from jobs length."""
        # This is valid - total_count can be higher than returned jobs (pagination)
        jobs = [
            JobListing(id="1", title="Developer", company="Company", url="https://example.com/1", source="linkedin")
        ]

        response = SearchResponse(
            jobs=jobs,
            total_count=100,  # Total found, but only returning 1
            query="developer",
            platforms=["linkedin"],
        )

        assert len(response.jobs) == 1
        assert response.total_count == 100

    def test_search_response_config_example(self):
        """Test SearchResponse matching the example in Config."""
        response = SearchResponse(
            jobs=[
                JobListing(
                    id="1",
                    title="Backend Developer",
                    company="Company A",
                    url="https://example.com/job/1",
                    source="linkedin",
                    location="Remote",
                    salary="$80k-$120k",
                )
            ],
            total_count=1,
            query="backend developer",
            platforms=["linkedin", "dou"],
        )

        assert len(response.jobs) == 1
        assert response.total_count == 1
        assert response.query == "backend developer"
        assert response.platforms == ["linkedin", "dou"]
        assert response.jobs[0].id == "1"
        assert response.jobs[0].title == "Backend Developer"
        assert response.jobs[0].company == "Company A"
        assert response.jobs[0].location == "Remote"
        assert response.jobs[0].salary == "$80k-$120k"

    def test_search_response_large_result_set(self):
        """Test SearchResponse with many jobs."""
        jobs = [
            JobListing(
                id=str(i),
                title=f"Developer {i}",
                company=f"Company {i}",
                url=f"https://example.com/job/{i}",
                source="linkedin" if i % 2 == 0 else "dou",
            )
            for i in range(50)
        ]

        response = SearchResponse(jobs=jobs, total_count=50, query="developer", platforms=["linkedin", "dou"])

        assert len(response.jobs) == 50
        assert response.total_count == 50
        assert response.jobs[0].id == "0"
        assert response.jobs[49].id == "49"

    def test_search_response_model_dump(self):
        """Test SearchResponse model_dump method."""
        job = JobListing(id="1", title="Python Dev", company="Tech Co", url="https://example.com/1", source="djinni")

        response = SearchResponse(jobs=[job], total_count=1, query="python", platforms=["djinni"])

        dumped = response.model_dump()
        assert dumped["total_count"] == 1
        assert dumped["query"] == "python"
        assert dumped["platforms"] == ["djinni"]
        assert len(dumped["jobs"]) == 1
        assert dumped["jobs"][0]["id"] == "1"
        assert dumped["jobs"][0]["title"] == "Python Dev"

    def test_search_response_model_dump_exclude_none(self):
        """Test SearchResponse model_dump with exclude_none."""
        job = JobListing(id="1", title="Dev", company="Co", url="https://example.com/1", source="workua")

        response = SearchResponse(jobs=[job], total_count=1, query="dev", platforms=["workua"])

        dumped = response.model_dump(exclude_none=True)
        # Check that optional None fields are excluded from job
        job_data = dumped["jobs"][0]
        assert "location" not in job_data
        assert "description" not in job_data
        assert "posted_date" not in job_data
        assert "salary" not in job_data

    def test_search_response_json_serialization(self):
        """Test SearchResponse JSON serialization."""
        response = SearchResponse(
            jobs=[
                JobListing(
                    id="1",
                    title="Engineer",
                    company="Corp",
                    url="https://example.com/1",
                    source="linkedin",
                    posted_date="2024-01-15",
                )
            ],
            total_count=1,
            query="engineer",
            platforms=["linkedin"],
        )

        json_str = response.model_dump_json()
        assert isinstance(json_str, str)
        assert '"total_count":1' in json_str
        assert '"query":"engineer"' in json_str
        assert '"platforms":["linkedin"]' in json_str
        assert '"id":"1"' in json_str
        assert '"title":"Engineer"' in json_str
