# Import python packages
import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

customer_name = st.text_input('Name on Smoothie:')
st.write(f'Your name is {customer_name}')

# activate session
cnx = st.connection('snowflake')
session = cnx.session()

# get table
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'), col('search_on'))

# display the dataframe
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

# convert to pandas
pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections = 5
)

if ingredients_list:

    ingredients_str = ''
    for ingredient in ingredients_list:
        ingredients_str += ingredient + ' '
      
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == ingredient, 'SEARCH_ON'].iloc[0]
        # st.write('The search value for ', ingredient,' is ', search_on, '.')
      
        st.subheader(ingredient + ' Nutrition Information')
        st.subheader(search_on)
        if search_on: 
          smoothiefruit_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        else:
          smoothie_fruit_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{ingredient}")
        sf_df = st.dataframe(data = smoothiefruit_response.json(), use_container_width = True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" + ingredients_str + """','""" + customer_name + """')"""

    
    order_button = st.button('Submit Order')
    
    if order_button:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {customer_name}!', icon="✅")
