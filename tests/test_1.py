import pytest
import datetime
from module_1 import days_between_dates, calculate_weighted_moving_average, is_powerful

# Test for days_between_dates function
@pytest.mark.parametrize("date1, date2, expected", [
    ("2023-01-01", "2023-01-02", 1, "ID_01_one_day_difference"),
    ("2023-01-01", "2023-01-01", 0, "ID_02_same_day"),
    ("2023-01-01", "2022-12-31", -1, "ID_03_negative_difference"),
    ("2020-02-29", "2021-02-28", 365, "ID_04_leap_year_to_non_leap"),
])
def test_days_between_dates(date1, date2, expected):
    # Act
    result = days_between_dates(date1, date2)
    
    # Assert
    assert result == expected

# Test for calculate_weighted_moving_average function
@pytest.mark.parametrize("prices, weights, expected", [
    ([10, 20, 30, 40, 50], [1, 2, 3], [30.0, 40.0, 50.0], "ID_01_basic"),
    ([100], [1], [100.0], "ID_02_single_element"),
    ([10, 20], [1, 2], [20.0], "ID_03_two_elements"),
    ([], [], [], "ID_04_empty_lists_error"),
    ([10, 20, 30], [1, 2, 3, 4], [], "ID_05_weights_longer_than_prices_error"),
])
def test_calculate_weighted_moving_average(prices, weights, expected):
    if not prices or not weights or len(weights) > len(prices):
        with pytest.raises(ValueError):
            calculate_weighted_moving_average(prices, weights)
    else:
        # Act
        result = calculate_weighted_moving_average(prices, weights)
        
        # Assert
        assert result == expected

# Test for is_powerful function
@pytest.mark.parametrize("magic, expected", [
    ("Sourcery", True, "ID_01_sourcery"),
    ("More Sourcery", True, "ID_02_more_sourcery"),
    ("Not Sourcery", False, "ID_03_not_sourcery"),
])
def test_is_powerful(magic, expected):
    # Act
    result = is_powerful(magic)
    
    # Assert
    assert result == expected
