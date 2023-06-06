 
import pandas as pd

import streamlit as st

import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


import mysql.connector as connection

db = connection.connect(host="relational.fit.cvut.cz", database="GOSales", user="guest", passwd="relational", use_pure=True)

st.image("Camping Equipment.JPG", use_column_width=True)


#JOINS
products_df = pd.read_sql_query("SELECT * FROM go_daily_sales as gds\
 LEFT JOIN go_products as gp ON gds.`Product number` = gp.`Product number`\
 LEFT JOIN go_retailers as gr ON gds.`Retailer code` = gr.`Retailer code`", db)


st.sidebar.title("Filter Retailer")   



duplicate_cols = products_df.columns[products_df.columns.duplicated()]
products_df = products_df.loc[:, ~products_df.columns.duplicated(keep='first')]




products_df['Total Sales'] = products_df['Unit sale price'] * products_df['Quantity']


products_df['Total cost'] = products_df['Unit cost'] * products_df['Quantity']

products_df['Revennue'] = products_df['Unit price'] * products_df['Quantity']

products_df['Profit Margin'] = products_df['Unit price'] - products_df['Unit cost']

        
Retailer_name = st.sidebar.selectbox('Select Retailer name', products_df['Retailer name'].unique())


st.sidebar.title("Filter Product line")
Product_line = st.sidebar.selectbox('Select Product line', products_df['Product line'].unique())

if Retailer_name:
    filtered_df = products_df[(products_df['Retailer name'] == Retailer_name)]
    
        
    if Product_line:
         filtered_df = products_df[(products_df['Product line'] == Product_line)]
        
st.title("GOExplorer")
st.write(filtered_df)














PL_count = products_df['Product line'].value_counts().to_frame().reset_index().rename(columns = {'Product line':'count','index':'Product line'})


Product_line_Profit = products_df.groupby('Product line')['Profit Margin'].mean()


    
#Bar Chart
def bc():
    grouped_df = products_df.groupby('Country')['Total Sales'].sum()
    fig, ax = plt.subplots(figsize=(10, 6))
    grouped_df.plot(kind='barh', ax=ax, color='#051094', width=0.7)

    ax.set_title('Country by Total Sales', fontsize=20, c='black')
    ax.set_xlabel('Country', fontsize=20, c='black')
    ax.set_ylabel('Total Sales', fontsize=20, c='black')
    plt.grid()
    
    return st.pyplot(fig)



#Pie Chart
def pc():
    fig, ax2 = plt.subplots(figsize=(7,7))
    ax2.pie(PL_count['count'], labels=PL_count['Product line'], autopct='%1.2f%%', explode=[0.09, 0.0, 0.0, 0.0, 0.0])                                
    ax2.axis('equal')                                
    ax2.set_title('Percentage Distribution of Products by Product line')                                             

    fig1, ax1 = plt.subplots(figsize=(7,7))
    ax1.pie(Product_line_Profit, labels=Product_line_Profit.index,autopct='%1.2f%%', explode=[0.0, 0.09, 0.0, 0.0, 0.0])
    ax1.axis('equal')
    ax1.set_title('Product line Profit Margin')

    st.pyplot(fig)
    st.pyplot(fig1)

#Scatter Plot  
def sp():
    x = products_df['Total cost']
    y = products_df['Revennue']
    fig, ax2 = plt.subplots(figsize=(7, 7))
    ax2.scatter(x, y, alpha=0.6, s=10, color='#468ED1')
    ax2.set_title("Scatter plot of Total cost vs Revennue")
    ax2.set_xlabel("Total cost")
    ax2.set_ylabel("Revennue")
    return st.pyplot(fig)


#Line Chart
def lc():
    grouped_df = products_df.groupby('Date')['Total Sales'].sum()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(grouped_df.index, grouped_df.values, color='#1520A6')
    ax.set_title('Total Sales over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Total Sales')
    return st.pyplot(fig)





#Heatmap


def hm(products_df):
    products_df['Date'] = pd.to_datetime(products_df['Date'])
    products_df['Retailer code'] = products_df['Retailer code'].astype('category')
    products_df['Product number'] = products_df['Product number'].astype('category')
    products_df['Order method code'] = products_df['Order method code'].astype('category')
    products_df = products_df.reset_index(drop=True)
    corr_matrix = products_df.corr()
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.heatmap(corr_matrix, annot=True, cmap="BuGn", ax=ax)
    ax.set_title("Correlation Heatmap")
    return st.pyplot(fig)







Charts = st.sidebar.selectbox('Select Chart', ['Bar Chart','Pie Chart','Line Chart','Scatterplot','Heatmap'])

if Charts == 'Bar Chart':
    bc()
elif Charts == 'Pie Chart':
    pc()

elif Charts == 'Line Chart':
    lc()
elif Charts == 'Scatterplot':
    sp()
else:
    hm(products_df)
    





















    
    
    
    
    