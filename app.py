import streamlit as st
import pandas as pd

from recommender import SalesBotRecommender


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="SalesBot AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="auto"
)


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown(
    """
    <style>

    /* Main page */
    .main {
        padding-top: 1rem;
    }

    /* Hero section */
    .hero-box {
        padding: 2rem;
        border-radius: 20px;
        background: linear-gradient(135deg, #111827, #374151);
        margin-bottom: 1.5rem;
    }

    .hero-box p {
        color: #e5e7eb;
        font-size: 1.1rem;
        margin-bottom: 0;
    }

    /* Recommendation cards */
    .recommendation-card {
        padding: 1.2rem;
        border-radius: 15px;
        border: 1px solid #e5e7eb;
        background: white;
        margin-bottom: 1rem;
    }

    .product-name {
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 0.4rem;
    }

    .product-code {
        color: #6b7280;
        font-size: 0.9rem;
    }

    .confidence {
        font-weight: 700;
    }

    /* Mobile improvements */
    @media (max-width: 768px) {

        .hero-box {
            padding: 1.4rem;
        }

        .hero-box p {
            font-size: 1rem;
        }

        h1 {
            font-size: 2rem !important;
        }

        h2 {
            font-size: 1.5rem !important;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# HERO
# ==========================================

st.markdown(
    """
    <div class="hero-box">
    """,
    unsafe_allow_html=True
)

st.title("🤖 SalesBot AI")

st.markdown(
    """
    <p>
    Intelligent product recommendations powered by
    real-world retail transaction data.
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("</div>", unsafe_allow_html=True)


st.write(
    "Select a product and discover what customers "
    "frequently purchased together."
)


# ==========================================
# LOAD RECOMMENDATION ENGINE
# ==========================================

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


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.header("⚙️ Recommendation Settings")

    number_of_recommendations = st.slider(
        "Number of recommendations",
        min_value=3,
        max_value=10,
        value=5
    )

    st.divider()

    st.subheader("About SalesBot")

    st.write(
        "SalesBot analyzes historical transactions "
        "to identify products frequently purchased "
        "together."
    )


# ==========================================
# PRODUCT SEARCH
# ==========================================

st.header("🔎 Find Product Recommendations")

st.write(
    "Choose a product below to discover related "
    "products based on historical purchase patterns."
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


# ==========================================
# RECOMMENDATION BUTTON
# ==========================================

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

        st.header("🛍️ Recommended Products")

        st.success(
            "Recommendations generated from historical "
            "purchase patterns."
        )

        for number, recommendation in enumerate(
            recommendations,
            start=1
        ):

            with st.container(border=True):

                st.subheader(
                    f"{number}. {recommendation['description']}"
                )

                st.caption(
                    f"Product code: "
                    f"{recommendation['stock_code']}"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        "🛒 **Bought together:** "
                        f"{recommendation['times_bought_together']} times"
                    )

                with col2:

                    st.write(
                        "📊 **Recommendation confidence:** "
                        f"{recommendation['confidence']}%"
                    )


# ==========================================
# DATASET OVERVIEW
# ==========================================

st.divider()

st.header("📊 Dataset Overview")

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


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "SalesBot AI Recommender • Built with Python, "
    "Pandas, Scikit-learn and Streamlit"
)
