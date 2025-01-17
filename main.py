import streamlit as st
import pandas as pd
import requests


def random_drank() -> pd.DataFrame:
    url = 'https://www.thecocktaildb.com/api/json/v1/1/random.php'
    response = requests.get(url)
    data = response.json()
    df = pd.json_normalize(data['drinks'])
    df = df.dropna(how='all', axis=1)
    return df


st.title('Random Cocktail')
df = random_drank()

# 숫자가 포함된 컬럼을 정리하여 매칭
ingredients = [col for col in df.columns if 'strIngredient' in col]
measures = [col for col in df.columns if 'strMeasure' in col]

# 이미지 출력
if 'strDrinkThumb' in df.columns:
    image_url = df['strDrinkThumb'].iloc[0]
    st.image(image_url, caption='Cocktail Image', use_container_width=True)

# 각 컬럼에 대해 텍스트 출력
if 'strDrink' in df.columns:
    st.write(f'name: {df["strDrink"].iloc[0]}')

if 'strCategory' in df.columns:
    st.write(f'category: {df["strCategory"].iloc[0]}')

if 'strAlcoholic' in df.columns:
    st.write(f'Alcoholic: {df["strAlcoholic"].iloc[0]}')

if 'strGlass' in df.columns:
    st.write(f'glass: {df["strGlass"].iloc[0]}')

if 'strInstructions' in df.columns:
    st.write(f'instructions: {df["strInstructions"].iloc[0]}')

st.subheader('Recipe')

# 숫자를 추출하여 매칭
ingredient_measure_pairs = []
for i in range(1, len(ingredients) + 1):
    ingredient_col = f'strIngredient{i}'
    measure_col = f'strMeasure{i}'

    if ingredient_col in df.columns and measure_col in df.columns:
        ingredient_measure_pairs.append((ingredient_col, measure_col))

# 짝지어서 출력
for ingredient_col, measure_col in ingredient_measure_pairs:
    ingredient = df[ingredient_col].iloc[0]
    measure = df[measure_col].iloc[0]

    # NaN 체크 후 출력
    if pd.notna(ingredient) and pd.notna(measure):
        st.write(f"{ingredient} : {measure}")
