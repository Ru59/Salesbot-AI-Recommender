import streamlit as st
import pandas as pd

from recommender import SalesBotRecommender


# -----------------------------
# Page configuration
# -----------------------------

st.set_page_config(
    page_title="SalesBot AI Recommender",
    page_icon="🤖",
    layout="wide"
)


# -----------------------------
# Custom styling
# -----------------------------

st.markdown(
    """
    <style>
        .main {
            padding-top: 2rem;
        }

        .hero {
            padding: 2rem;
            border-radius: 15px;
            background: linear-gradient(
                135deg,
                #1f2937,
                #374151
            );
            color: white;
            margin-bottom: 2rem;
        }

        .hero h1 {
            margin-bottom: 0.5rem;
        }

        .recommendation-card {
            padding: 1rem;
            border-radius: 12px;
            border: 1px solid #dddddd;
            margin-bottom: 0.8rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Header
# -----------------------------

st.markdown(
    """
    <div class="hero">
        <h1>🤖 SalesBot AI Recommender</h1>
        <p>
            Discover products that customers frequently purchase together.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Load recommendation model
# -----------------------------

@st.cache_resource
def load_recommender():

    recommender = SalesBotRecommender(
        "SalesBot_Data.csv"
    )

    recommender.load_data()
    recommender.build_model()

    return recommender


try:

    recommender = load_recommender()

except Exception as error:

    st.error(
        "SalesBot could not load the recommendation model."
    )

    st.exception(error)

    st.stop()


# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.title("SalesBot")

st.sidebar.write(
    "Select a product to discover related products."
)

st.sidebar.divider()

number_of_recommendations = st.sidebar.slider(
    "Number of recommendations",
    min_value=3,
    max_value=10,
    value=5
)


# -----------------------------
# Product selection
# -----------------------------

products = (
    recommender.df[
        ["stock_code", "description"]
    ]
    .drop_duplicates()
    .sort_values("description")
)

product_options = products.apply(
    lambda row:
    f"{row['description']} ({row['stock_code']})",
    axis=1
).tolist()


selected_product = st.selectbox(
    "🔎 Select a product",
    product_options
)


# Extract stock code
selected_code = selected_product.split("(")[-1].replace(")", "")


# -----------------------------
# Recommendation button
# -----------------------------

if st.button(
    "✨ Get Recommendations",
    type="primary",
    use_container_width=True
):

    recommendations = recommender.recommend(
        selected_code,
        number_of_recommendations
    )

    if not recommendations:

        st.warning(
            "No recommendations were found for this product."
        )

    else:

        st.subheader(
            "Customers who bought this product also bought:"
        )

        for number, recommendation in enumerate(
            recommendations,
            start=1
        ):

            st.markdown(
                f"""
                <div class="recommendation-card">

                <strong>
                {number}. {recommendation['description']}
                </strong>

                <br>

                Product code:
                {recommendation['stock_code']}

                <br>

                Bought together:
                {recommendation['times_bought_together']} times

                <br>

                Recommendation confidence:
                {recommendation['confidence']}%

                </div>
                """,
                unsafe_allow_html=True
            )


# -----------------------------
# Project information
# -----------------------------

st.divider()

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Customers",
        f"{recommender.df['customer_id'].nunique():,}"
    )

with col2:

    st.metric(
        "Products",
        f"{recommender.df['stock_code'].nunique():,}"
    )

with col3:

    st.metric(
        "Transactions",
        f"{recommender.df['invoice_no'].nunique():,}"
    )

st.caption(
    "SalesBot AI Recommender — built using retail transaction data."
)
