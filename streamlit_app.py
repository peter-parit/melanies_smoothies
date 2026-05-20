# Import python packages
import streamlit as st
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
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))

# display the dataframe
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections = 5
)

if ingredients_list:

    ingredients_str = ''
    for ingredient in ingredients_list:
        ingredients_str += ingredient + ' '

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" + ingredients_str + """','""" + customer_name + """')"""

    
    order_button = st.button('Submit Order')
    
    if order_button:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {customer_name}!', icon="✅")
    
import requests  
smoothiefroot_response = requests.get("[https://my.smoothiefroot.com/api/fruit/watermelon](https://my.smoothiefroot.com/api/fruit/watermelon)")  
st.text(smoothiefroot_response)
