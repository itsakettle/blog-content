import polars as pl
from scipy import stats 
from sklearn import tree
from sklearn.model_selection import cross_val_score
from sklearn.metrics import make_scorer, root_mean_squared_error
import numpy as np

def y_expr() -> pl.Expr:
    
    multiply_error_expr = (pl.col("x1") * pl.col("x2") * pl.col("x3")) + pl.col("e")
    relu_expr = pl.when(multiply_error_expr <0).then(pl.lit(0)).otherwise(multiply_error_expr)
    return relu_expr

def create_population(n: int = 10):
    data = {"x1": stats.expon.rvs(scale=10, size=n),
            "x2": stats.poisson.rvs(mu=10, size=n),
            "x3": stats.norm.rvs(loc=50, scale=5, size=n),
            "e": stats.norm.rvs(loc=0, scale=2000, size=n)
           }
    df = pl.DataFrame(data).lazy()
    df = df.with_columns(y_expr().alias("y"))
    df = df.drop("e")
    return df.collect()

def polars_to_sklearn(df: pl.DataFrame):
    X = df.select([pl.all().exclude("y")]).to_numpy()
    Y = df.select(pl.col("y")).to_numpy()
    return X, Y

def fit_tree_on_sample_and_cv(df: pl.DataFrame, sample_n: int, max_depth: int, folds: int):
    df = df.sample(n=sample_n)
    X, Y = polars_to_sklearn(df)
    cv_error_estimate = tree_cv_estimate(X=X, Y=Y, max_depth=max_depth, folds=folds)
    new_tree = tree.DecisionTreeRegressor(max_depth=max_depth).fit(X, Y)
    return new_tree, cv_error_estimate

def tree_cv_estimate(X: np.ndarray, Y: np.ndarray, max_depth: int, folds: int):
    new_tree = tree.DecisionTreeRegressor(max_depth=max_depth)
    rmse_scorer = make_scorer(root_mean_squared_error)
    cv_score = cross_val_score(estimator=new_tree, X=X, y=Y, scoring=rmse_scorer, cv=folds)
    return np.mean(cv_score)

def tree_population_error(population_X: np.ndarray, population_Y: np.ndarray, fitted_tree: tree.DecisionTreeRegressor):
    predicted_Y = fitted_tree.predict(population_X).reshape(-1, 1)
    error = root_mean_squared_error(y_true=population_Y, y_pred=predicted_Y)
    return error



def delta_cv_population_error_squared():
    delta = pl.col("population_error") - pl.col("cv_estimate")
    return delta.pow(2).alias("delta_cv_population_error_squared")

def delta_cv_mean_population_error_squared(): 
    delta = pl.col("mean_population_error") - pl.col("cv_estimate")
    return delta.pow(2).alias("delta_cv_mean_population_error_squared")


def main():
    df = create_population(n=1000009)
    population_X, population_Y = polars_to_sklearn(df=df)
    
    population_errors = []
    cv_estimates = []
    
    for i in range(0, 1000):
        fitted_tree, cv_estimate = fit_tree_on_sample_and_cv(df=df, sample_n=1000, max_depth=10, folds=10)
        error = tree_population_error(population_X=population_X,
                                  population_Y=population_Y,
                                  fitted_tree=fitted_tree)
        population_errors.append(error)
        cv_estimates.append(cv_estimate)

    df_results = pl.DataFrame({"population_error": population_errors, 
                               "cv_estimate": cv_estimates})

    df_results = df_results.with_columns(pl.mean("population_error").alias("mean_population_error"),
                            delta_cv_population_error_squared())\
            .with_columns(delta_cv_mean_population_error_squared())

    df_results = df_results.select(pl.mean("delta_cv_mean_population_error_squared"),
                                   pl.mean("delta_cv_population_error_squared"))

    print(df_results)

if __name__ == "__main__":
    main()



