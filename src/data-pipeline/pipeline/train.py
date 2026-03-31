import logging
from pipeline import Pipeline

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def main(csv_path="../merge/raw/csv_full_post.csv"):
    pipeline = Pipeline(
        target_col="y",
        drop_cols=["dep_nom", "reg_nom", "variation"],
        bad_dep_codes=["2A", "2B"],
        selected_k=5,
    )

    logging.info("Chargement des données")
    df = pipeline.load_csv(csv_path)

    logging.info("Nettoyage des données")
    df_clean = pipeline.clean(df)

    features = [
        "annee",
        "dep_code",
        "reg_code",
        "code_postal",
        "population",
        "superficie_km2",
        "zone_emploi",
        "taux_global_tfb",
        "taux_global_tfnb",
        "taux_plein_teom",
        "taux_global_th",
        "nb_ventes",
    ]

    X_train, X_test, y_train, y_test = pipeline.split(df_clean, features)

    logging.info("Entraînement du modèle")
    pipeline.train(X_train, y_train)

    logging.info("Évaluation du modèle")
    result = pipeline.evaluate(X_test, y_test)

    logging.info("Accuracy: %.4f", result["accuracy"])
    logging.info("Classification report:\n%s", result["classification_report"])
    logging.info("Confusion matrix:\n%s", result["confusion_matrix"])

    return pipeline, result


if __name__ == "__main__":
    main()
