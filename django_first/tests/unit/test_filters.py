from django_first.views import HomeView


def test_filter_url():
    url = '/?category=fruits'
    name = 'size'
    value = 'large'
    url = HomeView._filter_url(url, name, value)
    assert url.count('category=fruits') == 1
    assert url.count('size=large') == 1

    url = '/?category=fruits&color=yellow'
    name = 'size'
    value = 'large'
    url = HomeView._filter_url(url, name, value)
    assert url.count('category=fruits') == 1
    assert url.count('color=yellow') == 1
    assert url.count('size=large') == 1

    url = '/?category=fruits&size=large'
    name = 'size'
    value = 'large'
    url = HomeView._filter_url(url, name, value)
    assert url.count('category=fruits') == 1
    assert url.count('size=large') == 1
