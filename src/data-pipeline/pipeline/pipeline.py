import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline as SklearnPipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

mlflow.sklearn.autolog()


class Pipeline:
    def __init__(
        self,
        target_col="y",
        drop_cols=None,
        bad_dep_codes=None,
        selected_k=20,
        random_state=42,
    ):
        self.target_col = target_col
        self.drop_cols = drop_cols or ["dep_nom", "reg_nom", "variation"]
        self.bad_dep_codes = bad_dep_codes or ["2A", "2B"]
        self.selected_k = selected_k
        self.random_state = random_state

        categorical_cols = ["dep_code", "reg_code", "code_postal"]

        numeric_cols = [
            "annee",
            "population",
            "superficie_km2",
            "zone_emploi",
            "taux_global_tfb",
            "taux_global_tfnb",
            "taux_plein_teom",
            "taux_global_th",
            "nb_ventes",
            "densite",
            "ratio_taxe",
            "ventes_par_habitant",
            "taxe_x_population",
        ]

        preprocessor = ColumnTransformer(
            transformers=[
                ("num", SimpleImputer(strategy="mean"), numeric_cols),
                ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
            ]
        )

        self.model = SklearnPipeline(
            [
                ("preprocessing", preprocessor),
                ("selector", SelectKBest(f_classif, k=self.selected_k)),
                (
                    "classifier",
                    RandomForestClassifier(
                        random_state=self.random_state,
                        n_estimators=300,
                        max_depth=20,
                        min_samples_split=5,
                        min_samples_leaf=2,
                        class_weight="balanced",
                    ),
                ),
            ]
        )

    def load_csv(self, csv_path: str, sep=";") -> pd.DataFrame:
        return pd.read_csv(csv_path, sep=sep)

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        existing_drop = [c for c in self.drop_cols if c in df.columns]
        df = df.drop(columns=existing_drop)

        if "dep_code" in df.columns:
            df = df[~df["dep_code"].isin(self.bad_dep_codes)]

        df = df.dropna().reset_index(drop=True)
        # Feature engineering ici

        df["densite"] = df["population"] / (df["superficie_km2"] + 1)

        df["ratio_taxe"] = df["taux_global_tfb"] / (df["taux_global_th"] + 1)

        df["ventes_par_habitant"] = df["nb_ventes"] / (df["population"] + 1)

        df["taxe_x_population"] = df["taux_global_tfb"] * (df["population"] + 1)

        return df


    def split(self, df: pd.DataFrame, features, year_col="annee"):
        if year_col not in df.columns:
            raise ValueError(f"Colonne de split '{year_col}' introuvable")

        train_df = df[df[year_col] < 2024]
        test_df = df[df[year_col] == 2024]

        X_train = train_df[features]
        y_train = train_df[self.target_col]
        X_test = test_df[features]
        y_test = test_df[self.target_col]

        return X_train, X_test, y_train, y_test

    def train(self, X_train: pd.DataFrame, y_train: pd.Series):
        self.model.fit(X_train, y_train)
        return self

    def evaluate(self, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
        y_pred = self.model.predict(X_test)
        return {
            "accuracy": accuracy_score(y_test, y_pred),
            "classification_report": classification_report(y_test, y_pred, zero_division=0),
            "confusion_matrix": confusion_matrix(y_test, y_pred, labels=["hausse", "baisse", "stable"]),
        }

    def predict(self, X: pd.DataFrame):
        return self.model.predict(X)


if __name__ == "__main__":
    print("Ce module est prévu pour être importé depuis une commande de type 'python train.py'")
