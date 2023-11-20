# Recipes Analysis

## Introduction

## Cleaning and EDA (Exploratory Data Analysis)
### Data Cleaning
### Univariate Analysis

### Bivariate Analysis
- Calories vs. Sugar
- Calories vs. Total Fat

Besides seeking relationships from nutrition information, we would also like to analyze the potention relationship between `n_steps` and `n_ingredients`


- Number of Steps vs. Number of Ingredients

more ingredients, more steps, more difficult, less rating. 
but no obvious relationship between rating vs. step
- Average Ratings vs. Number of Steps 

### Interesting Aggregates

## Assessment of Missingness
### NMAR Analysis
In the data of `rating` in RATINGS is likely to be NMAR. 
The dataset we use is from [food.com](food.com). On this website, for each recipe the user can choose to click the `WRITE A REVIEW` button to provide review for the recipe. 
When writing a review, the user can choose to either provide a rating or write a review in text or do both. 
Then users with very positive experiences with a recipe would be more inclined to provide both a review by both rating and text; users with neutral opinions or negative experiences might not want to come back and rate, so they would be less motivated to give a numerical rating, leading to missing values in the `rating` column. 
Thus, the missingness of rating in data depends on the users' rating itself, so `rating` is NMAR. 

Additional data about the popularity of the recipe and whether user who use the recipe found it difficult might explain the missingness of rating. Popular dish might attract more attention and interaction from users, including ratings. Recipe complexity could influence user engagement. Users might be more inclined to rate recipes that are not difficult. 

### Missing Dependency

## Hypothesis Testing
### Permutation Test

n_ingredients, n_steps

minutes, rating

#### Null Hypothesis: 
#### Alternative Hypothesis: 