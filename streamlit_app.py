import altair as alt
import pandas as pd
import streamlit as st

# Show the page title and description.
st.set_page_config(page_title="Real Estate Price Analysis Dashboard", page_icon="🏚️")
st.title("🏚️ Real Estate Price Analysis Dashboard")
st.write(
    """
    An interactive dashboard to analyze real estate prices.
    You can explore various factors influencing property prices, visualize trends,
    and gain insights from the real estate dataset.
    """
)

# Load the data from a CSV
@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv("data/real_estate_listings.csv")
    return df

df = load_data()

st.header("Data Overview")
st.write(df.head())

st.header("Interactive Filters")

# Show slider widgets
prices = st.slider(label="Price", min_value=100000, max_value=1000000, value=(100000, 1000000), step=10000)
bedrooms = st.slider(label="Bedrooms", min_value=1, max_value=5, value=(1, 5))
bathrooms = st.slider(label="Bathrooms", min_value=1, max_value=3, value=(1, 3))
squarefeet = st.slider(label="SquareFeet", min_value=500, max_value=3500, value=(500, 3500), step=100)

# Filter the dataframe based on the widget input.
df_filtered = df[
    (df["Price"].between(prices[0], prices[1])) &
    (df["Bedrooms"].between(bedrooms[0], bedrooms[1])) &
    (df["Bathrooms"].between(bathrooms[0], bathrooms[1])) &
    (df["SquareFeet"].between(squarefeet[0], squarefeet[1]))
]

# Display the data as a table using `st.dataframe`.
st.dataframe(
    df_filtered,
    use_container_width=True,
    hide_index=True
)

st.header("Visualizations")
st.subheader("Price Histogram")
hist = alt.Chart(df_filtered).mark_bar().encode(
    alt.X("Price", bin=alt.Bin(maxbins=30), title="Price"),
    y='count()',
)
st.altair_chart(hist, use_container_width=True)

st.subheader("Price vs. Square Feet")
st.scatter_chart(
    df_filtered,
    x="SquareFeet",
    y="Price",
    size="Price",
)

st.subheader("Price vs. Area")
df_filtered["Size"] = df_filtered["Price"] / 2000
st.map(df_filtered, latitude="Latitude", longitude="Longitude", size="Size", zoom=11, use_container_width=True)

st.header("Insights Summary")
st.markdown(
    """
    - The price histogram shows many properties prices between 400,000 and 500,000.
    - The scatter plot shows no coreleation between price and square feet.
    - The map plotting property location and price does not show any correlation between area and price.
    """
)
