# Import libraries
import streamlit as st
import plotly.express as px
import pandas as pd
import altair as alt

# Page configuration
st.set_page_config(
    page_title="Comparative Country Dashboard",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS styling
st.markdown("""
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)

# Title and description
st.title("Comparative Country Dashboardd")

# Load data
df_combined = pd.read_csv('df_combined.csv')
df_combined['Year'] = df_combined['Year'].astype(str)

# Select one country for detailed analysis
selected_country = st.selectbox(
    "Select a Country", 
    options=df_combined['Country'].unique(), 
    index=list(df_combined['Country'].unique()).index("Brazil") if "Brazil" in df_combined['Country'].unique() else 0
)

# Center the country name in bold black text with a white background
st.markdown(
    f"""
    <div style="text-align: center; background-color: #393939; padding: 10px; margin-top: 20px; margin-bottom: 20px;">
        <h1 style="font-size: 60px; font-weight: bold; color: white;">{selected_country}</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Filter data for the selected country
country_data = df_combined[df_combined['Country'] == selected_country]

# Get the latest available data for the selected country
latest_data = country_data.sort_values(by='Year', ascending=False).iloc[0]

# Display metrics with the year below
col1, col2, col3, col4 = st.columns(4)

with col1:
    # Check if data is available for 'Population'
    if pd.isna(latest_data['Population']):
        st.metric(label="Total Population (millions)", value="No data found")
    else:
        # Format population in millions
        population_in_millions = f"{latest_data['Population'] / 1_000_000:.1f} M"
        st.metric(label="Total Population (millions)", value=population_in_millions)
    st.caption(f"Year: {latest_data['Year']}")

with col2:
    # Check if data is available for 'GDP'
    if pd.isna(latest_data['GDP']):
        st.metric(label="GDP (billions $)", value="No data found")
    else:
        # Format GDP in billions
        gdp_in_billions = f"${latest_data['GDP'] / 1_000_000_000:.2f} B"
        st.metric(label="GDP (billions $)", value=gdp_in_billions)
    st.caption(f"Year: {latest_data['Year']}")

with col3:
    # Check if data is available for 'GDP Per Capita'
    if pd.isna(latest_data['GDP Per Capita']):
        st.metric(label="GDP Per Capita (thousands $)", value="No data found")
    else:
        # Format GDP Per Capita in thousands
        gdp_per_capita_in_thousands = f"${latest_data['GDP Per Capita'] / 1_000:.2f} K"
        st.metric(label="GDP Per Capita (thousands $)", value=gdp_per_capita_in_thousands)
    st.caption(f"Year: {latest_data['Year']}")

with col4:
    # Check if data is available for 'Inflation Rate'
    if pd.isna(latest_data['Inflation Rate']):
        st.metric(label="Inflation Rate", value="No data found")
    else:
        # Display inflation rate as is
        inflation_rate_display = f"{latest_data['Inflation Rate']:.2f}%"
        st.metric(label="Inflation Rate", value=inflation_rate_display)
    st.caption(f"Year: {latest_data['Year']}")



# Historical and Comparative Analysis
st.header("Historical and Comparative Analysis")

# Select additional countries and years for comparison
selected_countries = st.multiselect(
    "Select Countries to Compare",
    options=df_combined['Country'].unique(),
    default=[selected_country, "United States"]
)
selected_years = st.multiselect(
    "Select Years to Compare",
    options=df_combined['Year'].unique(),
    default=["2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"]
)

# Filter data based on selections
filtered_data = df_combined[
    (df_combined['Country'].isin(selected_countries)) & 
    (df_combined['Year'].isin(selected_years))
]

# Create tabs for Economic and Social Indicators
tab1, tab2, tab3, tab4 = st.tabs(["Economic Indicators", "Infrastructure Indicators", "Social Indicators", "Education Indicators"])

# Economic Indicators
with tab1:
    st.subheader("Economic Indicators")
    col1, col2 = st.columns(2)
    with col1:
        fig = px.line(
            filtered_data,
            x='Year', y='GDP', color='Country',
            title="GDP Over Time"
        )
        st.plotly_chart(fig)
        st.markdown("GDP (Gross Domestic Product) is the total value of all goods and services produced in a country over a specific the year. It measures the size and health of a country's economy.")
    with col2:
        fig = px.line(
            filtered_data,
            x='Year', y='GDP Per Capita', color='Country',
            title="GDP Per Capita Over Time"
        )
        st.plotly_chart(fig)
        st.markdown("GDP per capita measures the average economic output per person within a country. It is calculated by dividing the GDP of a country by its total population.")
    col3, col4 = st.columns(2)
    with col3:
        filtered_data['1/PPP'] = 1 / filtered_data['PPP']
        fig = px.line(
            filtered_data,
            x='Year', y='1/PPP', color='Country',
            title="Purchasing Power Parity Over Time"
        )
        st.plotly_chart(fig)
        st.markdown("Purchasing Power Parity (PPP) compares different countries' currencies by measuring the cost of the same goods in different countries.  In this graph, higher values represent stronger purchasing power because they are calculated as the inverse of PPP (1/PPP).")
    with col4:
        fig = px.line(
            filtered_data,
            x='Year', y='Inflation Rate', color='Country',
            title="Inflation Rate Over Time"
        )
        st.plotly_chart(fig)
        st.markdown("Inflation Rate is the rate at which the general level of prices for goods and services rises.")

# Infrastructure Indicators
with tab2:
    st.subheader("Infrastructure Indicators")
    col1, col2 = st.columns(2)
    with col1:
        fig = px.line(
            filtered_data,
            x='Year', y='Urban Population', color='Country',
            title="Urban Population Over Time"
        )
        st.plotly_chart(fig)
        #st.markdown("Urban Population is the percentage of the total population living in urban areas.")
    with col2:
        fig = px.line(
            filtered_data,
            x='Year', y='Access to Electricity', color='Country',
            title="Access to Electricity Over Time"
        )
        st.plotly_chart(fig)
        #st.markdown("Access to Electricity is the percentage of the population with access to electricity.")
    col3, col4 = st.columns(2)
    with col3:
        fig = px.line(
            filtered_data,
            x='Year', y='Renewable Energy Consumption', color='Country',
            title="Renewable Energy Consumption Over Time"
        )
        st.plotly_chart(fig)
        st.markdown("Renewable Energy Consumption is the share of renewable energy in the total energy consumption.")
    with col4:
        fig = px.line(
            filtered_data,
            x='Year', y='Individuals Using the Internet', color='Country',
            title="Individuals Using the Internet Over Time"
        )
        st.plotly_chart(fig)
        #st.markdown("Individuals Using the Internet is the percentage of the population using the internet.")

# Social Indicators
with tab3:
    st.subheader("Social Indicators")
    col1, col2 = st.columns(2)
    with col1:
        fig = px.line(
            filtered_data,
            x='Year', y='Gross National Income Per Capita', color='Country',
            title="Gross National Income Per Capita Over Time"
        )
        st.plotly_chart(fig)
        st.markdown("Gross National Income Per Capita is the total income of a country divided by its population, adjusted for purchasing power.")
    with col2:
        fig = px.line(
            filtered_data,
            x='Year', y='Life Exp.', color='Country',
            title="Life Expectancy Over Time"
        )
        st.plotly_chart(fig)
        #st.markdown("Life Expectancy is the average number of years a person can expect to live.")
    col3, col4 = st.columns(2)
    with col3:
        fig = px.line(
            filtered_data,
            x='Year', y='Poverty at $2.15 a Day', color='Country',
            title="Poverty at $2.15 a Day Over Time"
        )
        st.plotly_chart(fig)
        st.markdown("Poverty at 2.15 a Day is the percentage of the population living below the international poverty line of 2.15 dollars per day.")
    with col4:
        fig = px.line(
            filtered_data,
            x='Year', y='Employment to Population Ratio', color='Country',
            title="Employment to Population Ratio Over Time"
        )
        st.plotly_chart(fig)
        st.markdown("Employment to Population Ratio is the proportion of a country's working-age population that is employed.")
    col5, col6 = st.columns(2)
    with col5:
        fig = px.line(
            filtered_data,
            x='Year', y='Population', color='Country',
            title="Population Over Time"
        )
        st.plotly_chart(fig)
        st.markdown("...")

# Education Indicators
with tab4:
    st.subheader("Education Indicators")
    col1, col2 = st.columns(2)
    #with col1:
        #fig = px.line(
            #filtered_data,
            #x='Year', y='School Enrollment', color='Country',
            #title="School Enrollment Over Time"
        #)
        #st.plotly_chart(fig)
        #st.markdown("School Enrollment is the percentage of the eligible population enrolled in primary, secondary, or tertiary education.")
    #with col2:
        #st.markdown("**Expected Years of Schooling:** The total number of years of schooling a child of school-entering age can expect to receive.")
        #fig = px.line(
            #filtered_data,
            #x='Year', y='Expected Years of Schooling', color='Country',
            #title="Expected Years of Schooling Over Time"
        #)
        #st.plotly_chart(fig)
    #col3, col4 = st.columns(2)
    #with col3:
        #st.markdown("**Literacy Rate:** The percentage of people aged 15 and above who can read and write.")
        #fig = px.line(
            #filtered_data,
            #x='Year', y='Literacy rate', color='Country',
            #title="Literacy Rate Over Time"
        #)
        #st.plotly_chart(fig)
    with col1:
        fig = px.line(
            filtered_data,
            x='Year', y='Expenditure on education', color='Country',
            title="Expenditure on Education Over Time"
        )
        st.plotly_chart(fig)
        st.markdown("Expenditure on Education is the percentage of GDP spent on education.")

with st.expander('About', expanded=True):
        st.write('''
            - Data: [World Bank Group](https://www.worldbank.org/ext/en/home).
