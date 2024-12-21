
import pandas as pd
def convert_to_camel_case(text):
    """
    Converts a string with spaces into camelCase.

    Parameters:
        text (str): The input string to be converted.

    Returns:
        str: The camelCase version of the input string.
    """
    words = text.split()
    if not words:
        return ""

    # Convert the first word to lowercase, and capitalize subsequent words
    return words[0].lower() + ''.join(word.capitalize() for word in words[1:])




def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    # Remove unwanted characters (spaces, hyphens, etc.) from column names
    df.columns = df.columns.str.replace(r'[\s\-]', '', regex=True)  # Replace space and hyphen with ''
    
    # Optionally, remove unwanted characters from the values in the DataFrame
    df = df.applymap(lambda x: str(x).replace(' ', '').replace('-', '') if isinstance(x, str) else x)
    
    return df