import streamlit as st
import pandas as pd

from recommender import SalesBotRecommender


# --------------------------------
# Page configuration
# --------------------------------

st.set_page_config(
    page_title="SalesBot AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="auto"
)


# --------------------------------
# Custom styling
# --------------------------------

st.markdown(
    """
    <style>

    .main {
        padding-top: 1rem;
    }

    .hero {
        padding: 2.5rem;
        border-radius: 20px;
        background: linear-gradient(
            135deg,
            #111827,
            #374151
        );
        color: white;
        margin-bottom: 2rem;
    }

    .hero h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }

    .hero p {
        font-size: 1.15rem;
        color: #e5e7eb;
    }

    .recommendation-card {
        padding: 1.25rem;
        border-radius: 15px;
        border: 1px solid #e5e7eb;
        background: #ffffff;
        margin-bottom: 1rem;
    }

    .product-name {
        font-size: 1.1rem;
        font-weight: 700;
    }

    .product-code {
        color: #6b7280;
        font-size: 0.9rem;
    }

    .confidence {
        font-weight: 600;
    }

    .section-title {
        margin-top: 2rem;
        margin-bottom: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------
# Header
# --------------------------------

st.markdown(
    """
    <div class="hero">

        <h1>🤖 SalesBot AI</h1>

        <p>
            Intelligent product recommendations powered by
            real-world retail transaction data.
        </p>

    </div>
    """,
    unsafe_allow_html=True
)


st.write(
    "Select a product and discover what customers "
    "frequently purchased together."
)


# --------------------------------
# Load recommendation engine
# --------------------------------

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
        "SalesBot could not load the recommendation engine."
    )

    st.exception(error)

    st.stop()


# --------------------------------
# Sidebar
# --------------------------------

with st.sidebar:

    st.header("⚙️ Recommendation Settings")

    number_of_recommendations = st.slider(
        "Number of recommendations",
        min_value=3,
        max_value=10,
        value=5
    )

    st.divider()

    st.write("### About SalesBot")

    st.write(
        "SalesBot analyzes historical transactions "
        "to identify products frequently purchased "
        "together."
    )


# --------------------------------
# Product selection
# --------------------------------

st.markdown(
    '<div class="section-title"><h2>🔎 Find Product Recommendations</h2></div>',
    unsafe_allow_html=True
)


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
    "Select a product",
    product_options
)


selected_code = (
    selected_product
    .split("(")[-1]
    .replace(")", "")
)


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

        st.markdown(
            '<div class="section-title"><h2>🛍️ Recommended Products</h2></div>',
            unsafe_allow_html=True
        )

        st.success(
            "Recommendations generated from historical "
            "purchase patterns."
        )


        for number, recommendation in enumerate(
            recommendations,
            start=1
        ):

            st.markdown(
                f"""
                <div class="recommendation-card">

                    <div class="product-name">
                        {number}. {recommendation['description']}
                    </div>

                    <div class="product-code">
                        Product code:
                        {recommendation['stock_code']}
                    </div>

                    <br>

                    <strong>
                        🛒 Bought together:
                    </strong>

                    {recommendation['times_bought_together']}
                    times

                    <br><br>

                    <strong>
                        📊 Recommendation confidence:
                    </strong>

                    <span class="confidence">
                        {recommendation['confidence']}%
                    </span>

                </div>
                """,
                unsafe_allow_html=True
            )


# --------------------------------
# Project statistics
# --------------------------------

st.divider()

st.markdown(
    '<div class="section-title"><h2>📊 Dataset Overview</h2></div>',
    unsafe_allow_html=True
)


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
        "Invoices",
        f"{recommender.df['invoice_no'].nunique():,}"
    )


st.divider()


st.caption(
    "SalesBot AI Recommender • Built with Python, "
    "Pandas, Scikit-learn and Streamlit"
)
