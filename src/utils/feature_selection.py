import pandas as pd
import re
import logging
from sklearn.model_selection import train_test_split

logging.basicConfig(level=logging.INFO)

def transformations_data():
    
    # Read the data
    df_2015 = pd.read_csv("data/2015.csv")
    df_2016 = pd.read_csv("data/2016.csv")
    df_2017 = pd.read_csv("data/2017.csv")
    df_2018 = pd.read_csv("data/2018.csv")
    df_2019 = pd.read_csv("data/2019.csv")

    logging.info("correctly loaded data")


    # Remove rows with missing values
    df_2018 = df_2018.dropna(subset=['Perceptions of corruption'])

    logging.info("correctly removed row with missing values")


    # Clean the column names with regular expressions
    dataframes = [df_2015, df_2016, df_2017, df_2018, df_2019]

    def clean_column_names(df: pd.DataFrame):

        clean_columns = []
        for col in df.columns:
            normalized = re.sub(r'[.\(\)]', '_', col.replace(' ', '_').lower())
            normalized = re.sub(r'[^a-zA-Z0-9_]', '', normalized)
            normalized = re.sub(r'_{2,}', '_', normalized)
            normalized = normalized.strip('_')
            clean_columns.append(normalized)
        df.columns = clean_columns

    for df in dataframes:
        clean_column_names(df)

    logging.info("correctly cleaned column names")


    # Rename the columns
    column_names_2015_2017 = {
    'economy_gdp_per_capita': 'gdp_per_capita',
    'trust_government_corruption': 'perceptions_of_corruption',
    'family': 'social_support'
    }

    column_names_2018_2019 = {
        'overall_rank': 'happiness_rank',
        'score': 'happiness_score',
        'freedom_to_make_life_choices': 'freedom',
        'country_or_region': 'country',
        'healthy_life_expectancy': 'health_life_expectancy'
    }

    def rename_columns(df: pd.DataFrame, column_mapping: dict):

        df.rename(columns=column_mapping, inplace=True)

    rename_columns(df_2015, column_names_2015_2017)
    rename_columns(df_2016, column_names_2015_2017)
    rename_columns(df_2017, column_names_2015_2017)
    rename_columns(df_2018, column_names_2018_2019)
    rename_columns(df_2019, column_names_2018_2019)

    logging.info("correctly renamed columns")


    # Remove columns
    df_2015.drop(columns=['region', 'standard_error', 'dystopia_residual'], inplace=True)
    df_2016.drop(columns=['region', 'lower_confidence_interval', 'upper_confidence_interval', 'dystopia_residual'], inplace=True)
    df_2017.drop(columns=['whisker_high', 'whisker_low', 'dystopia_residual'], inplace=True)

    logging.info("correctly removed columns")


    # Concatenate the dataframes
    column_order = ['happiness_rank', 'country', 'happiness_score', 'gdp_per_capita', 'social_support', 'health_life_expectancy', 'freedom', 'generosity', 'perceptions_of_corruption']

    for df in dataframes:
        df = df.reindex(columns=column_order)

    df = pd.concat(dataframes, axis=0, ignore_index=True)
    df = df.reindex(columns=column_order)

    logging.info("correctly concatenated dataframes")
        

    # Add continent column
    def continent(df : pd.DataFrame) -> pd.DataFrame:

        country_to_continent = {
            'New Zealand': 'Oceania',
            'Australia': 'Oceania',
            'Czech Republic': 'Europe',
            'Northern Cyprus': 'Europe',
            'Ireland': 'Europe',
            'Switzerland': 'Europe',
            'Belgium': 'Europe',
            'Finland': 'Europe',
            'North Macedonia': 'Europe',
            'Iceland': 'Europe',
            'United Kingdom': 'Europe',
            'Netherlands': 'Europe',
            'Denmark': 'Europe',
            'Slovenia': 'Europe',
            'Lithuania': 'Europe',
            'Norway': 'Europe',
            'Russia': 'Europe',
            'Austria': 'Europe',
            'Montenegro': 'Europe',
            'Cyprus': 'Europe',
            'North Cyprus': 'Europe',
            'Kosovo': 'Europe',
            'Romania': 'Europe',
            'Hungary': 'Europe',
            'Serbia': 'Europe',
            'Portugal': 'Europe',
            'Estonia': 'Europe',
            'Latvia': 'Europe',
            'Greece': 'Europe',
            'Macedonia': 'Europe',
            'Albania': 'Europe',
            'Bosnia and Herzegovina': 'Europe',
            'Croatia': 'Europe',
            'Sweden': 'Europe',
            'Luxembourg': 'Europe',
            'Spain': 'Europe',
            'Italy': 'Europe',
            'Moldova': 'Europe',
            'Malta': 'Europe',
            'Ukraine': 'Europe',
            'France': 'Europe',
            'Slovakia': 'Europe',
            'Bulgaria': 'Europe',
            'Germany': 'Europe',
            'Peru': 'South America',
            'Uruguay': 'South America',
            'Bolivia': 'South America',
            'Argentina': 'South America',
            'Colombia': 'South America',
            'Venezuela': 'South America',
            'Paraguay': 'South America',
            'Chile': 'South America',
            'Brazil': 'South America',
            'Ecuador': 'South America',
            'Suriname': 'South America',
            'Trinidad and Tobago': 'North America',
            'El Salvador': 'North America',
            'Nicaragua': 'North America',
            'Guatemala': 'North America',
            'Canada': 'North America',
            'Honduras': 'North America',
            'Costa Rica': 'North America',
            'Belize': 'North America',
            'Trinidad & Tobago': 'North America',
            'Puerto Rico': 'North America',
            'Haiti': 'North America',
            'Dominican Republic': 'North America',
            'Jamaica': 'North America',
            'Panama': 'North America',
            'Mexico': 'North America',
            'United States': 'North America',
            'Palestinian Territories': 'Asia',
            'Bangladesh': 'Asia',
            'Thailand': 'Asia',
            'Bahrain': 'Asia',
            'Japan': 'Asia',
            'Malaysia': 'Asia',
            'Saudi Arabia': 'Asia',
            'Uzbekistan': 'Asia',
            'United Arab Emirates': 'Asia',
            'Kazakhstan': 'Asia',
            'Taiwan': 'Asia',
            'Syria': 'Asia',
            'Taiwan Province of China': 'Asia',
            'Yemen': 'Asia',
            'Afghanistan': 'Asia',
            'Hong Kong S.A.R., China': 'Asia',
            'Cambodia': 'Asia',
            'Oman': 'Asia',
            'Singapore': 'Asia',
            'Israel': 'Asia',
            'South Korea': 'Asia',
            'Kuwait': 'Asia',
            'Qatar': 'Asia',
            'Myanmar': 'Asia',
            'Tajikistan': 'Asia',
            'Philippines': 'Asia',
            'Hong Kong': 'Asia',
            'Bhutan': 'Asia',
            'Azerbaijan': 'Asia',
            'Pakistan': 'Asia',
            'Jordan': 'Asia',
            'Kyrgyzstan': 'Asia',
            'Turkmenistan': 'Asia',
            'China': 'Asia',
            'Indonesia': 'Asia',
            'Vietnam': 'Asia',
            'Turkey': 'Asia',
            'Armenia': 'Asia',
            'Laos': 'Asia',
            'Mongolia': 'Asia',
            'India': 'Asia',
            'Georgia': 'Asia',
            'Iraq': 'Asia',
            'Sri Lanka': 'Asia',
            'Lebanon': 'Asia',
            'Nepal': 'Asia',
            'Iran': 'Asia',
            'South Africa': 'Africa',
            'Ghana': 'Africa',
            'Zimbabwe': 'Africa',
            'Tunisia': 'Africa',
            'Liberia': 'Africa',
            'Sudan': 'Africa',
            'Congo (Kinshasa)': 'Africa',
            'Ethiopia': 'Africa',
            'Sierra Leone': 'Africa',
            'Mauritania': 'Africa',
            'Kenya': 'Africa',
            'Djibouti': 'Africa',
            'Botswana': 'Africa',
            'Mauritius': 'Africa',
            'Libya': 'Africa',
            'Mozambique': 'Africa',
            'Lesotho': 'Africa',
            'Somaliland region': 'Africa',
            'Morocco': 'Africa',
            'Nigeria': 'Africa',
            'Swaziland': 'Africa',
            'Algeria': 'Africa',
            'Zambia': 'Africa',
            'Malawi': 'Africa',
            'Cameroon': 'Africa',
            'Egypt': 'Africa',
            'Angola': 'Africa',
            'Burkina Faso': 'Africa',
            'Congo (Brazzaville)': 'Africa',
            'Somaliland Region': 'Africa',
            'Comoros': 'Africa',
            'Uganda': 'Africa',
            'South Sudan': 'Africa',
            'Senegal': 'Africa',
            'Burundi': 'Africa',
            'Namibia': 'Africa',
            'Somalia': 'Africa',
            'Mali': 'Africa',
            'Ivory Coast': 'Africa',
            'Gabon': 'Africa',
            'Niger': 'Africa',
            'Gambia': 'Africa',
            'Tanzania': 'Africa',
            'Madagascar': 'Africa',
            'Benin': 'Africa',
            'Central African Republic': 'Africa',
            'Chad': 'Africa',
            'Rwanda': 'Africa',
            'Togo': 'Africa',
            'Guinea': 'Africa'
        }
        
        df['continent'] = df['country'].map(country_to_continent)
        return df

    df = continent(df)

    logging.info("correctly added continent column")


    # Delete columns unnecessary
    df.drop(columns={'happiness_rank', 'country'}, inplace=True)

    logging.info("correctly removed columns")


    # Add continent dummies
    continent_dummies = pd.get_dummies(df['continent']).astype(int)
    df = pd.concat([df, continent_dummies], axis=1)
    df.drop('continent', axis=1, inplace=True)

    logging.info("correctly added continent dummies")


    # Rename columns
    columns_rename = {
        'Africa': 'africa', 'Asia': 'asia', 'Europe': 'europe', 'North America': 'north_america', 'Oceania': 'oceania', 'South America': 'south_america'
    }

    def rename_columns(df: pd.DataFrame, column_names: dict):

        df.rename(columns=column_names, inplace=True)

    rename_columns(df, columns_rename)

    logging.info("correctly renamed columns")


    # Split the data
    X = df.drop('happiness_score', axis=1)
    y = df['happiness_score'] 

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=50)
    X_test['happiness_score'] = y_test

    logging.info("correctly split data into train and test sets")

    return X_test

