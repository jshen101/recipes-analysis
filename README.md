# Recipes Analysis

## Introduction
Food is an indispensable part of our lives. Across the globe, an infinite array of dishes and recipes are readily accessible to anyone through the internet. As a data scientist, the wealth of user reviews on various recipes offers a treasure trove of information. With the rapid evolution of technology, our lives have accelerated, prompting the consideration: does the preparation time required for a recipe influence users' perceptions and attitudes towards it? 

In this project, we will be focusing on a subset of the data from [food.com](https://www.food.com/), which contains recipes and the corresponding reviews posted since 2008. The data has two parts: **RECIPES** and **RATINGS**. The **RECIPES** dataset has 83782 rows and it includes information about *Recipe name*, *Recipe ID*, *Minutes to prepare recipe*, *User ID who submitted this recipe*, *Date recipe was submitted*, *Food.com tags for recipe*, *Nutrition information*, *Number of steps in recipe*, *Text of recipe steps in order*, *User-provided description*. The **RATINGS** dataset has 731927 rows and it includes information about *User ID*, *Recipe ID*, *Date of interaction*, *Rating given*, *Review text*. To delve more into our research question, the columns containing information of recipe ID, minutes, and rating is most relevant.

There are four main parts of this project: introduction, cleaning and EDA, assessment of missing, and hypothesis testing. We will be first cleaning the data and conducting the exploratory data analysis to get a basic understanding of the data. Then, we will be assessing the missingness of this data by analyzing NMAR and missingness dependency. 

After getting a general sense of the data and checking for potential patterns between different variables, we will then conduct a hypothesis test about our research question of "what is the relationship between the cooking time and average rating of the recipes?"

## Cleaning and EDA (Exploratory Data Analysis)
### Data Cleaning
#### Basic setup
- We first imported the downloaded data from csv files. 
- After importing the raw data, since both `RAW_recipes` and `RAW_interactions` has information about recipe ID, we perform left merge on their recipe id column. 
- Then, we fill all ratings of 0 with `np.nan`. This is a reasonable step because a zero in the dataset might not represent an actual rating but rather a placeholder for missing or unrecorded data. Ratings typically start from 1 in most systems, so a zero could indicate an absence of rating rather than a rating of zero. Particularly in this dataset, by looking at an example [directly on food.com](https://www.food.com/recipe/chickpea-and-fresh-tomato-toss-51631), we can see that the recipes rating is in the range of 1-5, and the user can choose to not rate the recipe, which would result in a rating of zero in the raw_interactions dataset. Thus, including zero ratings can skew the results since those zeros are not actual ratings.
- Since we are curious about the average rating of the recipes, we then find the average rating per recipe as a series and merge it back to our dataframe. 
- For the purposes of this project, the 'review' column in the interactions dataset doesn’t have much use, so we decided to drop this column first. 

#### Data type
- After finish setting up our dataframe, we then start focusing on cleaning the data type of each column in our dataframe. Before cleaning, our dataframe has the following type:
```
name               object
id                  int64
minutes             int64
contributor_id      int64
submitted          object
tags               object
nutrition          object
n_steps             int64
steps              object
description        object
ingredients        object
n_ingredients       int64
user_id           float64
recipe_id         float64
date               object
rating            float64
review             object
avg_rating        float64
dtype: object
```
- We noticed that both `submitted` and `date` should be datetime data, we converted them by using `pe.to_datetime()`. 
- `id`, `contributor_id`, `user_id`, `recipe_id` should be categorical data, so we then converted them to string, and assign any nan value that was mistakenly converted to string back to `np.nan`. 
- `nutrition`, `steps`, `tags`, `ingredients` columns are all containing strings that looks like a list, so we decided to conver them to list. 
- `nutrition` column contains interesting information of *calories (#), total fat (PDV), sugar (PDV), sodium (PDV), protein (PDV), saturated fat (PDV), carbohydrates (PDV)*, so we pulled them out and assigned new columns for each of them. 
  - After assigning new columns for each piece of the information in `nutrition`, we then droped the `nutrition` column. 
- Finishing dealing with types of data, our dataframe now has the following types: 
```
name                      object
id                        object
minutes                    int64
contributor_id            object
submitted         datetime64[ns]
tags                      object
n_steps                    int64
steps                     object
description               object
ingredients               object
n_ingredients              int64
user_id                   object
recipe_id                 object
date              datetime64[ns]
rating                   float64
avg_rating               float64
calories                 float64
total_fat                float64
sugar                    float64
sodium                   float64
protein                  float64
saturated_fat            float64
carbohydrates            float64
dtype: object
```
#### Clean for Missing Data
- We when dealing with data types, we also noticed that there are many missing values in the dataframe, so we want to deal with the missingness as well. 
- We found that there is one outlier that has all `np.nan` value on `user_id`, `recipe_id`, `date`, `rating`, and `review` column. This implies that it has no user interactions at all, so we decided to drop this observation. 
- There are columns with information that we will not need when analyze the data, so we also dropped several columns e.g. 'contributor_id', 'submitted', 'tags', 'steps', 'description', 'ingredients', 'user_id', 'date', and one repeated column 'recipe_id'. 

- Here is a preview of our dataset after cleaning. 

| name                                 |     id |   minutes |   n_steps |   n_ingredients |   rating |   avg_rating |   calories |   total_fat |   sugar |   sodium |   protein |   saturated_fat |   carbohydrates |
|:-------------------------------------|-------:|----------:|----------:|----------------:|---------:|-------------:|-----------:|------------:|--------:|---------:|----------:|----------------:|----------------:|
| 1 brownies in the world    best ever | 333281 |        40 |        10 |               9 |        4 |            4 |      138.4 |          10 |      50 |        3 |         3 |              19 |               6 |
| 1 in canada chocolate chip cookies   | 453467 |        45 |        12 |              11 |        5 |            5 |      595.1 |          46 |     211 |       22 |        13 |              51 |              26 |
| 412 broccoli casserole               | 306168 |        40 |         6 |               9 |        5 |            5 |      194.8 |          20 |       6 |       32 |        22 |              36 |               3 |
| 412 broccoli casserole               | 306168 |        40 |         6 |               9 |        5 |            5 |      194.8 |          20 |       6 |       32 |        22 |              36 |               3 |
| 412 broccoli casserole               | 306168 |        40 |         6 |               9 |        5 |            5 |      194.8 |          20 |       6 |       32 |        22 |              36 |               3 |

### Univariate Analysis
In the univariate analysis, we would like to analyze the distribution of minutes. 

#### Minutes
<iframe src="minutes_distribution.html" width=800 height=600 frameBorder=0></iframe>

This shows that the distribution of minutes is highly right skewed, with most of the recipes taking less than 19.9k minutes to prepare. We can easily tell that there is several really extreme outliers which makes the distribution hard to read. Thus, we decided to remove the outliers by using IQR and plot the distribution again.

<iframe src="minutes_distribution_no_outlier.html" width=800 height=600 frameBorder=0></iframe>

This is the distribution of minutes after removing the outliers by using IQR. We can see that the distribution is still right skewed, but the distribution is much more clear. It shows that the recipes preparing minutes is centered around 30 minutes, meaning that most recipes take around 30 minutes to prepare. 

### Bivariate Analysis
Nowadays, people are more focusing on healthy diet, so we would like to see if the common sense of having more sugar means having more calories is true.

<iframe src="calories_sugar.html" width=800 height=600 frameBorder=0></iframe>

From the scatter plot, we can see that there is a positive relationship between calories and sugar. This means that the common sense of having more sugar means having more calories is true. 

Besides seeking relationships from nutrition information, we would also like to see if there is some potential relationship between `n_steps` and `n_ingredients`. 

<iframe src="steps_ingredients.html" width=800 height=600 frameBorder=0></iframe>

We used to think that more ingredients would cause the recipes to have more steps, but from this scatter plot, we can see that there is no obvious relationship between `n_steps` and `n_ingredients`. This means that the number of steps in a recipe is not necessarily related to the number of ingredients in a recipe.

### Interesting Aggregates
For the aggregate analysis, we choose to using a pivot table which has `minutes` as values, `rating` as index, and `n_steps` as columns. 

Here is a preview of the table:

|   rating |       1 |        2 |       3 |        4 |       5 |       6 |       7 |        8 |        9 |      10 |      11 |       12 |       13 |      14 |       15 |      16 |       17 |       18 |      19 |       20 |       21 |       22 |       23 |       24 |      25 |      26 |       27 |       28 |      29 |      30 |       31 |      32 |      33 |      34 |      35 |      36 |       37 |      38 |       39 |      40 |      41 |      42 |     43 |      44 |      45 |      46 |       47 |       48 |      49 |       50 |      51 |      52 |      53 |   54 |      55 |      56 |    57 |      58 |     59 |    60 |       61 |   62 |     63 |   64 |   65 |   66 |     67 |   68 |   69 |   70 |   73 |      76 |   77 |   79 |   80 |   81 |   85 |   86 |   87 |   88 |   93 |   98 |   100 |
|---------:|--------:|---------:|--------:|---------:|--------:|--------:|--------:|---------:|---------:|--------:|--------:|---------:|---------:|--------:|---------:|--------:|---------:|---------:|--------:|---------:|---------:|---------:|---------:|---------:|--------:|--------:|---------:|---------:|--------:|--------:|---------:|--------:|--------:|--------:|--------:|--------:|---------:|--------:|---------:|--------:|--------:|--------:|-------:|--------:|--------:|--------:|---------:|---------:|--------:|---------:|--------:|--------:|--------:|-----:|--------:|--------:|------:|--------:|-------:|------:|---------:|-----:|-------:|-----:|-----:|-----:|-------:|-----:|-----:|-----:|-----:|--------:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|------:|
|        1 | 20.3913 |  85.9167 | 54.2857 | 109.315  | 90.0818 | 65.0759 | 64.0248 | 144.568  |  88.4483 | 64.6887 | 68.905  |  59.9423 |  76.2377 | 68.1074 |  90.766  | 346.333 |  77.5556 |  73.8302 | 152.333 |  89.6765 | 108.771  | 320.37   | 127.444  | 172.692  | 131.875 | 674.706 |  95.8667 | 815      |  75     | 101.167 | 218.5    |  72     | 214.5   |  46.25  | 255     | 126.25  | 112.5    | 300     | nan      | nan     | 210     |  65     | nan    | 233.5   | 234.231 |  67.5   |  nan     | nan      | 125     | nan      | 330     | nan     | nan     |  nan |  50     | nan     | nan   | nan     | nan    | nan   | nan      |  nan | nan    |  nan |  nan |  nan |  nan   |  nan |  nan |  nan |  nan | nan     |  nan |  nan |  nan |  nan |  nan |  nan |  nan |  nan |  nan |  nan |   nan |
|        2 | 13.7222 | 100.302  | 66.7216 |  87.3084 | 88.5    | 68.9209 | 62.575  |  91.4785 |  92.3439 | 53.7551 | 64.1973 |  66.4254 | 122.011  | 74.6111 | 264.558  | 100.027 |  91.1695 |  93.1714 | 147.711 |  65.4375 |  99.4348 | 141.8    |  77.5    | 199.2    | 134.138 | 965.9   | 766.538  |  69.2857 | 132.5   | 257.2   | 100      | 123.286 | 163.333 | 765     | nan     |  45     |  60      | 125     |  60      | nan     |  80     | 210     | nan    | 120     | 352.5   | 165     | 1620     | 105      | nan     | nan      | nan     | nan     | nan     |  nan | nan     | nan     | nan   | nan     | nan    | nan   |  40      |  nan | nan    |  nan |  nan |  nan |  nan   |  nan |  nan |  nan |  nan | nan     |  nan |  nan |  nan |  nan |  nan |  nan |  nan |  nan |  nan |  nan |   nan |
|        3 | 54.831  |  65.0299 | 59.5556 |  99.1744 | 72.5275 | 73.2048 | 60.1691 |  92.5342 |  73.7533 | 71.2259 | 68.9432 |  81.0137 |  72.6182 | 80.3369 |  89.9956 | 103.703 |  65.8355 | 515.109  | 106.812 |  82.4625 |  84.6102 |  88.2333 | 111.385  |  86.6667 | 109.615 | 473.128 |  99.8    | 121.9    | 337.857 | 103.769 |  72.4615 | 106.8   |  92.5   | 346.8   | 275     | 145     |  83.6667 | 180     |  93.3333 |  95     | 430     |  60     | nan    | nan     | 376.545 | 135     |  nan     | 260      |  85     | 150      | 330     |  90     | 100     |  nan | 150     | nan     | 120   | 140     | nan    | nan   | 125      |  nan | nan    |  nan |  nan |  nan |  nan   |  nan |  nan |  nan |  nan | nan     |  nan |  nan |  nan |  nan |  nan |  nan |  nan | 1530 |  nan |  nan |   nan |
|        4 | 26.1739 |  37.2697 | 45.2475 |  78.6316 | 68.6034 | 75.2487 | 87.4331 |  70.9689 |  79.4838 | 96.1135 | 74.7487 | 218.72   |  76.2464 | 74.921  |  80.286  | 148.018 | 194.986  | 144.153  | 102.514 |  70.993  | 146.577  | 197.409  |  97.3333 | 125.725  | 109.092 | 294.769 | 128.839  | 192.322  | 148.316 | 181.164 | 105.658  | 160.045 | 502.846 | 219.316 | 166.409 | 165     | 117.529  | 233.529 | 308.6    | 110.556 | 270     | 123.333 | nan    | 220     | 270.833 | 122.333 |  239     | 360      | 146.667 |  69      |  65     | 150     | 235     |  nan | 100     | nan     | nan   | nan     | nan    | nan   |  40      |  105 | nan    |  nan |  nan |  nan |  nan   |   42 |  nan |  nan |  nan | nan     |  nan |  830 |   60 |  510 |  nan |  nan |  nan | 2880 |  nan |  nan |   nan |
|        5 | 15.5866 |  35.7194 | 45.3343 |  68.6689 | 99.4956 | 62.4593 | 70.71   |  73.263  | 256.634  | 68.5113 | 77.1643 |  76.2406 | 107.242  | 92.1356 |  91.0447 | 485.093 |  90.0668 | 117.098  | 131.634 | 104.594  |  87.9456 | 147.934  | 176.594  | 150.879  | 131.205 | 573.187 | 178.047  | 110.441  | 102.286 | 133.097 | 124.465  | 244.994 | 224.106 | 177.357 | 264.851 | 228.899 | 144.707  | 127.056 | 164.537  | 169.86  | 253.528 | 158.234 | 175.55 | 215.077 | 310.524 | 140     |  445.512 |  90.4839 | 394.238 |  90.5556 | 656.071 | 113.333 | 164.444 |  144 | 106.733 | 213.571 | 103.3 | 248.077 |  86.25 | 105.8 |  46.9231 |  170 | 161.25 | 2940 |   90 |  408 | 1481.5 |   42 |  150 |  273 |  160 | 897.571 |   60 |  830 |   60 | 3000 |  860 |   18 |  195 | 2880 |  360 | 2930 |  1680 |

This table conveys the relationship between the complexity of a recipe (as measured by the number of steps) and the time required to prepare it (in minutes), across different recipe ratings. Although the trend is not very strong, but we tend to see that the average minutes of cooking across each rating increases as the complexity of the recipe increases. It is reasonable to see this trend because more steps tends to cause more time. However, it's important to note that this relationship is not strictly linear or uniformly progressive across different ratings, indicating that other factors beyond mere step count contribute to the preparation time. For example, certain steps may be more time-consuming than others, or some recipes may require longer waiting or cooking times regardless of the number of steps. This insight is crucial for food platforms, as it suggests that while complexity may enhance a dish's appeal, it is the balance of time investment and cooking process efficiency that may optimize user satisfaction and engagement with a recipe.


## Assessment of Missingness
### NMAR Analysis
In the data of `review` in RATINGS is likely to be NMAR. 
The dataset we use is from [food.com](https://www.food.com/). On this website, for each recipe the user can choose to click the `WRITE A REVIEW` button to provide review for the recipe. 
When writing a review, the user can choose to either provide a rating or write a review in text or do both. 
Then users who thinks the recipe is simple and has nothing to talk about would be less likely to provide a text review. 
Thus, the missingness of `review` in data depends on the users' review itself, so `review` is NMAR. 

Additional data about the complexity of the recipe and whether user who use the recipe found it difficult might explain the missingness of review. Complex dish might attract more attention and interaction from users, including text review. Recipe complexity could influence user engagement. Users might be more inclined to give review to difficult recipes that they need to follow step-by-step. 

### Missing Dependency
The `rating` column has non-trivial missingness that we would like to investigate by performing permutation tests to analyze the dependencdy of the missingness of `rating` on `minutes` and on `n_steps`.

#### Missingness of Rating on Minutes
- Null hypothesis: The preparing minutes of when rating is not missing and when rating is missing have the same distribution. (Rating independent from Minutes)
- Alternative hypothsis: The preparing minutes of when rating is not missing and when rating is missing have the different distribution. (Rating dependent on Minutes)
- Observed Statistics: Absolute difference in group means (absolute mean minutes of missing rating - absolute mean minutes of non-missing rating)
- Significance level: a = 0.05

<iframe src="rating_min.html" width=800 height=600 frameBorder=0></iframe>

We performed permutation test, shuffling the missingness of rating 1000 times and get 1000 simulating results about the absolute difference. As a result, we get a p-value of 0.13, which is greater than our significance level 0.05. Thus, we fail to reject the null hypothesis and there is no statistically significant evidence to suggest that the missingness of rating is related to the preparing minutes.

#### Missingness of Rating on Number of Steps
- Null hypothesis: The number of steps when rating is not missing and when rating is missing have the same distribution. (Rating independent from number of steps)
- Alternative hypothsis: The number of steps of when rating is not missing and when rating is missing have the different distribution. (Rating dependent on number of steps)
- Observed Statistics: Absolute difference in group means (absolute mean n_steps of missing rating - absolute mean n_steps of non-missing rating)
- Significance level: a = 0.05

<iframe src="rating_step_1.html" width=800 height=600 frameBorder=0></iframe>

<iframe src="rating_step_2.html" width=800 height=600 frameBorder=0></iframe>

We performed permutation test, shuffling the missingness of rating 1000 times and get 1000 simulating results about the absolute difference. 

<iframe src="rating_step.html" width=800 height=600 frameBorder=0></iframe>

As a result, we get a p-value approaches 0.0, which is greater than our significance level 0.05. Thus, we reject the null hypothesis and there is statistically significant evidence to suggest that the missingness of rating could be related to the number of steps.


## Hypothesis Testing
### Permutation test: What is the relationship between the preparing time and average rating of recipes?
- Null Hypothesis: There is no significant difference in the average rating of recipes between different preparing time groups. 
- Alternative Hypothesis: There is a significant difference in the average rating of recipes between different preparing time groups, higher average rating (rating > 4) group tend to have lower preparing time.
  - The hypotheses choices are good because they are closely related to the questioni of "what is the relationship between the cooking time and average rating of recipes?" that we are curious about. 
- Test statistic: Difference in mean ratings between preparing minutes that is greater than median minutes group and preparing minutes that is less than or equal to median minutes. 
  - The test statistics is a good choice because it could measure the difference in mean preparing time of different rating groups (> 4 or <= 4), whcih could provide good reflection toward the research question.
- Significance level: a = 0.05
  - The significance level is a good choice because it is a common significance level that is used in hypothesis testing.

From the univariate analysis, we have noticed that there are a lot of extreme outliers in the minutes column, so we decided to consider minutes greater than 30240 (3 weeks) as outliers that are not faithful and to not consider them in our hypothesis test.

We performed permutation test, shuffling the minutes 1000 times and get 1000 simulating results about the difference. 


<iframe src="rating_min_perm.html" width=800 height=600 frameBorder=0></iframe>

As a result, we get p_value of 0.01 which is less than our significance level of 0.05. Thus, we reject the null hypothesis of there is no significant difference in the average rating of recipes between different preparing time groups.

