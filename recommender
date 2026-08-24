import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer


class SalesBotRecommender:

    def __init__(self, data_path):
        self.data_path = data_path
        self.df = None
        self.matrix = None
        self.product_codes = None
        self.product_info = {}
        self.product_counts = None
        self.code_to_index = {}

    def load_data(self):
        self.df = pd.read_csv(self.data_path)

        required_columns = [
            "invoice_no",
            "stock_code",
            "description"
        ]

        missing = [
            column
            for column in required_columns
            if column not in self.df.columns
        ]

        if missing:
            raise ValueError(
                f"Missing columns: {missing}"
            )

        self.df = self.df.dropna(
            subset=[
                "invoice_no",
                "stock_code",
                "description"
            ]
        )

        self.df["stock_code"] = (
            self.df["stock_code"]
            .astype(str)
            .str.strip()
        )

        self.df["description"] = (
            self.df["description"]
            .astype(str)
            .str.strip()
        )

        return self.df

    def build_model(self):

        transactions = (
            self.df[
                [
                    "invoice_no",
                    "stock_code",
                    "description"
                ]
            ]
            .drop_duplicates()
        )

        invoice_products = (
            transactions
            .groupby("invoice_no")["stock_code"]
            .agg(list)
        )

        encoder = MultiLabelBinarizer(
            sparse_output=True
        )

        matrix = encoder.fit_transform(
            invoice_products
        )

        self.matrix = matrix

        self.product_codes = encoder.classes_

        self.code_to_index = {
            code: index
            for index, code
            in enumerate(self.product_codes)
        }

        product_info = (
            transactions
            .drop_duplicates("stock_code")
            .set_index("stock_code")["description"]
            .to_dict()
        )

        self.product_info = product_info

        self.product_counts = (
            matrix.sum(axis=0).A1
        )

        return self

    def recommend(
        self,
        product_code,
        number_of_recommendations=5
    ):

        product_code = str(product_code)

        if product_code not in self.code_to_index:
            return []

        product_index = (
            self.code_to_index[product_code]
        )

        product_row = (
            self.matrix.T @ self.matrix
        ).getrow(product_index)

        product_row = product_row.tocoo()

        recommendations = []

        for index, count in zip(
            product_row.col,
            product_row.data
        ):

            recommended_code = (
                self.product_codes[index]
            )

            if recommended_code == product_code:
                continue

            confidence = (
                count /
                self.product_counts[
                    product_index
                ]
            )

            recommendations.append({
                "stock_code": recommended_code,
                "description": self.product_info.get(
                    recommended_code,
                    "Unknown product"
                ),
                "times_bought_together": int(count),
                "confidence": round(
                    float(confidence) * 100,
                    2
                )
            })

        recommendations.sort(
            key=lambda x: x["confidence"],
            reverse=True
        )

        return recommendations[
            :number_of_recommendations
        ]
