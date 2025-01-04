from demo_5 import transform_data


def test_transform_data():
    import pandas as pd

    # Create sample input data
    input_data = {
        "age": [25, 35, 28, 45, 22],
        "city": ["New York", "Chicago", "Boston", "Chicago", "Seattle"],
    }
    df = pd.DataFrame(input_data)

    # Expected output data
    expected_data = {
        "age": [25, 28, 22],
        "city": ["New York", "Boston", "Seattle"],
        "age_category": ["Young", "Young", "Young"],
    }
    expected_df = pd.DataFrame(expected_data)

    # Test the function
    result_df = transform_data(df)

    # Assert the results
    pd.testing.assert_frame_equal(
        result_df.reset_index(drop=True), expected_df.reset_index(drop=True)
    )


def test_transform_data_empty():
    import pandas as pd

    # Test with empty DataFrame
    empty_df = pd.DataFrame({"age": [], "city": []})
    result = transform_data(empty_df)

    assert len(result) == 0
    assert "age_category" in result.columns


def test_transform_data_all_old():
    import pandas as pd

    # Test with all old ages
    input_data = {"age": [45, 50, 35], "city": ["New York", "Boston", "Seattle"]}
    df = pd.DataFrame(input_data)

    result = transform_data(df)
    assert all(result["age_category"] == "Old")


def test_transform_data_all_chicago():
    import pandas as pd

    # Test with all Chicago entries
    input_data = {"age": [25, 35, 45], "city": ["Chicago", "Chicago", "Chicago"]}
    df = pd.DataFrame(input_data)

    result = transform_data(df)
    assert len(result) == 0
