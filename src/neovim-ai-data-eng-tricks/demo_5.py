def transform_data(df):
    df["age_category"] = df["age"].apply(lambda x: "Young" if x < 30 else "Old")
    df_filtered = df[df["city"] != "Chicago"]
    return df_filtered
