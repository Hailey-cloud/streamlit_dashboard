import streamlit as st
import pandas as pd
import altair as alt


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv("data/real_estate_listings.csv")
    df.columns = df.columns.str.strip()
    df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")
    df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")
    return df.dropna(subset=["Latitude", "Longitude"])

df = load_data()

st.title('🏠 Real Estate Price Analysis Dashboard')
st.write("""
In this project, we present an interactive dashboard using Streamlit to 
analyze real estate prices. Users can explore various factors influencing property prices, 
visualize trends, and gain insights from the dataset.
""")


st.subheader("📊 Data Overview")
st.dataframe(df.head())


st.sidebar.header("🔎 Filter Listings")


min_price, max_price = int(df["Price"].min()), int(df["Price"].max())
price_range = st.sidebar.slider("Price Range", min_price, max_price, (min_price, max_price), step=10000)

# Bedrooms - slider
min_beds, max_beds = int(df["Bedrooms"].min()), int(df["Bedrooms"].max())
bedroom_range = st.sidebar.slider("Bedrooms", min_beds, max_beds, (min_beds, max_beds))

# Bathrooms - slider
min_baths, max_baths = int(df["Bathrooms"].min()), int(df["Bathrooms"].max())
bathroom_range = st.sidebar.slider("Bathrooms", min_baths, max_baths, (min_baths, max_baths))

# SquareFeet Range
min_sqft, max_sqft = int(df["SquareFeet"].min()), int(df["SquareFeet"].max())
sqft_range = st.sidebar.slider("SquareFeet Range", min_sqft, max_sqft, (min_sqft, max_sqft), step=100)

# filter
filtered_df = df[
    (df["Price"].between(*price_range)) &
    (df["Bedrooms"].between(*bedroom_range)) &
    (df["Bathrooms"].between(*bathroom_range)) &
    (df["SquareFeet"].between(*sqft_range))
]


st.subheader(f"🔎 Filtered Results ({len(filtered_df)} listings)")
st.dataframe(filtered_df)


st.subheader("📈 Price Distribution")


filtered_df["PriceBin"] = (filtered_df["Price"] // 100000) * 100000

hist = alt.Chart(filtered_df).mark_bar().encode(
    x=alt.X("PriceBin:O", title="Price Bin ($100k each)"),
    y=alt.Y("count()", title="Number of Listings"),
    tooltip=["count()", "PriceBin"]
).properties(width=700).interactive()

st.altair_chart(hist, use_container_width=True)


# sqft vs price
st.subheader("📉 SquareFeet vs Price")
scatter = alt.Chart(filtered_df).mark_circle(size=60, opacity=0.6).encode(
    x=alt.X("SquareFeet", title="Area (sqft)"),
    y=alt.Y("Price", title="Price ($)"),
    tooltip=["Address", "SquareFeet", "Price", "Bedrooms", "Bathrooms"]
).properties(width=700).interactive()
st.altair_chart(scatter, use_container_width=True)



# map
st.subheader("🗺️ Price vs Property Locations on Map")
filtered_df["Size"] = filtered_df["Price"] / 2000
st.map(filtered_df, latitude="Latitude", longitude="Longitude", size="Size", zoom=11, use_container_width=True)

st.subheader("✍️ Insight")
st.markdown("""

The project data includes real estate prices in Vancouver, which range from 100k to 900k. 
The bar graph of the price distribution shows that most of the homes are in the 300k to 400k range. 
There is also almost no correlation between the SquareFeet of a home and its price,which mean it does not appear that 
a larger SquareFeet means a higher price.
The map and price visualization shows a wide distribution of properties in the Vancouver area, and while it is obvious,
 the closer to the downtown area, the higher the price tends to be.


""")