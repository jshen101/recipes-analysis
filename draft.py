def IQR_bounds(df, column):
    # Calculate IQR
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    # Define upper and lower boundaries
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return lower_bound, upper_bound

l , u = IQR_bounds(df, 'minutes')
recipes_clean_out = recipes_clean[(recipes_clean['minutes'] > l) & (recipes_clean['minutes'] < u)]

l, u = IQR_bounds(df, 'n_steps')
recipes_clean_out = recipes_clean_out[(recipes_clean_out['n_steps'] > l) & (recipes_clean_out['n_steps'] < u)]

l, u = IQR_bounds(df, 'n_ingredients')
recipes_clean_out = recipes_clean_out[(recipes_clean_out['n_ingredients'] > l) & (recipes_clean_out['n_ingredients'] < u)]