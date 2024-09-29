import pytest

from open_news.google import Category, Location


@pytest.fixture(scope="session", params=[
    (
        Category.TOPICS, 
        "CAAqJQgKIh9DQkFTRVFvSUwyMHZNREpmTjNRU0JYcG9MVlJYS0FBUAE",
        Location.Taiwan,
        None,
    ),
    (
        Category.TOPICS, 
        "CAAqJQgKIh9DQkFTRVFvSUwyMHZNREpmTjNRU0JYcG9MVlJYS0FBUAE",
        Location.Taiwan,
        "CAQiW0NCQVNQZ29JTDIwdk1ESmZOM1FTQlhwb0xWUlhJZzhJQkJvTENna3ZiUzh3T1hrMGNHMHFHZ29ZQ2hSTlFWSkxSVlJUWDFORlExUkpUMDVmVGtGTlJTQUJLQUEqKQgAKiUICiIfQ0JBU0VRb0lMMjB2TURKZk4zUVNCWHBvTFZSWEtBQVABUAE",
    ),
    (
        Category.TOPICS, 
        "CAAqJQgKIh9DQkFTRVFvSUwyMHZNREpmTjNRU0JYcG9MVlJYS0FBUAE",
        Location.Taiwan,
        "CAQiR0NCQVNMd29JTDIwdk1ESmZOM1FTQlhwb0xWUlhJZzhJQkJvTENna3ZiUzh3TVRONU4za3FDeElKTDIwdk1ERXplVGQ1S0FBKikIAColCAoiH0NCQVNFUW9JTDIwdk1ESmZOM1FTQlhwb0xWUlhLQUFQAVAB",
    ),
])
def google_news_request(request):
    return request.param
