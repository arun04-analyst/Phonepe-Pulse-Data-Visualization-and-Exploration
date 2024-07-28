# Importing Necessary libraries

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import json
import requests

# MySQL Connection

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="example2",
  port="3306"
)

# Converting MySQL Database to pandas Dataframe

mycursor = mydb.cursor()

#Aggregated_insurance
mycursor.execute("select * from aggregated_insurance;")

table1 = mycursor.fetchall()

Aggre_insurance = pd.DataFrame(table1,columns = ("States", "Years", "Quarter", "Transaction_type", "Transaction_count","Transaction_amount"))

#Aggregated_transsaction
mycursor.execute("select * from aggregated_transaction;")

table2 = mycursor.fetchall()
Aggre_transaction = pd.DataFrame(table2,columns = ("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))

#Aggregated_user
mycursor.execute("select * from aggregated_user")

table3 = mycursor.fetchall()
Aggre_user = pd.DataFrame(table3,columns = ("States", "Years", "Quarter", "Brands", "Transaction_count", "Percentage"))

#Map_insurance
mycursor.execute("select * from map_insurance")

table4 = mycursor.fetchall()

Map_insurance = pd.DataFrame(table4,columns = ("States", "Years", "Quarter", "Districts", "Transaction_count","Transaction_amount"))

#Map_transaction
mycursor.execute("select * from map_transaction")

table5 = mycursor.fetchall()
Map_transaction = pd.DataFrame(table5,columns = ("States", "Years", "Quarter", "Districts", "Transaction_count", "Transaction_amount"))

#Map_user
mycursor.execute("select * from map_user")

table6 = mycursor.fetchall()
Map_user = pd.DataFrame(table6,columns = ("States", "Years", "Quarter", "Districts", "RegisteredUser", "AppOpens"))

#Top_insurance
mycursor.execute("select * from top_insurance")

table7 = mycursor.fetchall()

Top_insurance = pd.DataFrame(table7,columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))

#Top_transaction
mycursor.execute("select * from top_transaction")

table8 = mycursor.fetchall()
Top_transaction = pd.DataFrame(table8,columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))

#Top_user
mycursor.execute("select * from top_user")

table9 = mycursor.fetchall()
Top_user = pd.DataFrame(table9, columns = ("States", "Years", "Quarter", "Pincodes", "RegisteredUser"))

# Funtion defining for geo visualisation

# Map Analysis
def Map_insur_plot1(df,state,year):
    
    miyd = df[(df["States"] == state) & (df["Years"] == year)]
    miyd.reset_index(drop=True,inplace=True)


    miydg= miyd.groupby(["Districts"])[["Transaction_count","Transaction_amount"]].sum()
    miydg.reset_index(inplace=True)

    Map_insur_plot1= px.bar(miydg, x= "Districts", y="Transaction_count", title= f"{state} TRANSACTION COUNT ({year})")
    st.plotly_chart(Map_insur_plot1)

    Map_insur_plot2= px.bar(miydg, x= "Districts", y="Transaction_amount", title= f"{state} TRANSACTION AMOUNT ({year})")
    st.plotly_chart(Map_insur_plot2)

def Map_Tranc_plot2(df,state,year):
    
    miyd = df[(df["States"] == state) & (df["Years"] == year)]
    miyd.reset_index(drop=True,inplace=True)


    miydg= miyd.groupby(["Districts"])[["Transaction_count","Transaction_amount"]].sum()
    miydg.reset_index(inplace=True)

    Map_insur_plot1= px.bar(miydg, x= "Districts", y="Transaction_count", title= f"{state} TRANSACTION COUNT ({year})")
    st.plotly_chart(Map_insur_plot1)

    Map_insur_plot2= px.bar(miydg, x= "Districts", y="Transaction_amount", title= f"{state} TRANSACTION AMOUNT ({year})")
    st.plotly_chart(Map_insur_plot2)


def Map_User_plot(df,state,year):
    muyd = df[(df["States"] == state) & (df["Years"] == year)]
    muyd.reset_index(drop=True,inplace=True)

    muydg=muyd.groupby(["Districts"])[["RegisteredUser","AppOpens"]].sum()
    muydg.reset_index(inplace=True)

    Map_user_plot1=px.pie(muydg, values="RegisteredUser", names="Districts",color_discrete_sequence=px.colors.qualitative.Bold,
                          title=f"{state} REGISTERED USERS ({year})" )
    st.plotly_chart(Map_user_plot1)
    

    Map_user_plot2=px.pie(muydg, values="AppOpens", names="Districts",color_discrete_sequence=px.colors.qualitative.Vivid,
                          title=f"{state} AppOpens ({year})" )
    st.plotly_chart(Map_user_plot2)

#top chart analysis

def ques1():
    brand= Aggre_user[["Brands","Transaction_count"]]
    brand1= brand.groupby("Brands")["Transaction_count"].sum().sort_values(ascending=False)
    brand2= pd.DataFrame(brand1).reset_index()

    fig_brands= px.pie(brand2, values= "Transaction_count", names= "Brands", color_discrete_sequence=px.colors.sequential.dense_r,
                       title= "Top Mobile Brands of Transaction_count")
    return st.plotly_chart(fig_brands)

def ques2():
    lt= Aggre_transaction[["States", "Transaction_amount"]]
    lt1= lt.groupby("States")["Transaction_amount"].sum().sort_values(ascending= True)
    lt2= pd.DataFrame(lt1).reset_index().head(10)

    fig_lts= px.bar(lt2, x= "States", y= "Transaction_amount",title= "LOWEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques3():
    htd= Map_transaction[["Districts", "Transaction_amount"]]
    htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=False)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Transaction_amount", names= "Districts", title="TOP 10 DISTRICTS OF HIGHEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Emrld_r)
    return st.plotly_chart(fig_htd)

def ques4():
    htd= Map_transaction[["Districts", "Transaction_amount"]]
    htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Transaction_amount", names= "Districts", title="TOP 10 DISTRICTS OF LOWEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Greens_r)
    return st.plotly_chart(fig_htd)


def ques5():
    sa= Map_user[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=False)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "AppOpens", title="Top 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.deep_r)
    return st.plotly_chart(fig_sa)

def ques6():
    sa= Map_user[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=True)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "AppOpens", title="lowest 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.dense_r)
    return st.plotly_chart(fig_sa)

def ques7():
    stc= Aggre_transaction[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=True)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH LOWEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Jet_r)
    return st.plotly_chart(fig_stc)

def ques8():
    stc= Aggre_transaction[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=False)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH HIGHEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Magenta_r)
    return st.plotly_chart(fig_stc)

def ques9():
    ht= Aggre_transaction[["States", "Transaction_amount"]]
    ht1= ht.groupby("States")["Transaction_amount"].sum().sort_values(ascending= False)
    ht2= pd.DataFrame(ht1).reset_index().head(10)

    fig_lts= px.bar(ht2, x= "States", y= "Transaction_amount",title= "HIGHEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques10():
    dt= Map_transaction[["Districts", "Transaction_amount"]]
    dt1= dt.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    dt2= pd.DataFrame(dt1).reset_index().head(50)

    fig_dt= px.bar(dt2, x= "Districts", y= "Transaction_amount", title= "DISTRICTS WITH LOWEST TRANSACTION AMOUNT",
                color_discrete_sequence= px.colors.sequential.Mint_r)
    return st.plotly_chart(fig_dt)



#Stream lit part

st.set_page_config(layout= "wide", )
st.title(":violet[PHONE DATA VISUALISATION AND EXPLORATION]")


 

with st.sidebar:
    
    select= option_menu("Main Menu", ["HOME","TOP CHARTS"])

if select == "HOME":

    col1,col2= st.columns(2)
    

    with col1:
        st.header(":violet[PHONEPE]")
        st.subheader(":violet[INDIA'S BEST TRANSACTION APP]")
        st.markdown(":violet[PhonePe  is an Indian digital payments and financial technology company]")
        st.write("****:violet[FEATURES:]****")
        st.write("****~Credit & Debit card linking****")
        st.write("****~Bank Balance check****")
        st.write("****~Money Storage****")
        st.write("****~PIN Authorization****")
        st.download_button(":orange[DOWNLOAD THE APP NOW]", "https://www.phonepe.com/app-download/")
        st.write("")
        st.write("")
        st.write("")
        
        st.divider()
        
        
        st.header(":violet[AGGRAGATED ANALYSIS]")
        
        year= st.slider("**Select the Year**", Aggre_transaction["Years"].min(), Aggre_transaction["Years"].max())
        
        tacy=Aggre_transaction[Aggre_transaction["Years"] == year]
        tacy.reset_index(drop=True,inplace=True)


        tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
        tacyg.reset_index(inplace=True)

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1= json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()


        fig_india_1=px.choropleth(tacyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                color="Transaction_amount", color_continuous_scale= "Inferno",
                                range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                hover_name= "States", title= f"{year} Transaction Amount", fitbounds= "locations",
                                height= 500, width= 650,projection= "mercator" )
        
        fig_india_1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)

        fig_india_2=px.choropleth(tacyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                color="Transaction_count", color_continuous_scale= "Rainbow",
                                range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                hover_name= "States", title= f"{year} Transaction count", fitbounds= "locations",
                                height= 500, width= 650,projection= "mercator" )
        
        fig_india_2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)
        st.divider()
        
        auy=Aggre_transaction[Aggre_transaction["Years"] == year]
        auy.reset_index(drop=True,inplace=True)

        auyg=auy.groupby(["Transaction_type"])[["Transaction_count","Transaction_amount"]].sum().reset_index()

        fig_count= px.bar(auyg, x= "Transaction_type", y= "Transaction_count", title=f"{year} TRANSACTION TYPES DISTRIBITION")
        st.plotly_chart(fig_count)
        
        year= st.slider("**Select the Year**", Aggre_user["Years"].min(), Aggre_user["Years"].max())

        auy=Aggre_user[Aggre_user["Years"] == year]
        auy.reset_index(drop=True,inplace=True)

        auyg=auy.groupby(["Brands"])["Transaction_count"].sum().reset_index()

        fig_count= px.bar(auyg, x= "Brands", y= "Transaction_count", title=f"{year} USERS BRANDS DISTRIBITION")
        st.plotly_chart(fig_count)

        fig_count1=px.pie(auyg, values= "Transaction_count", names= "Brands")
        st.plotly_chart(fig_count1)




    with col2:

        st.image("H:/Downloads/PhonePe_Logo.png",use_column_width="always")
        st.video("H:/Downloads/phonepevideo.mp4",autoplay=True)
        st.divider()

        st.header(":violet[MAP ANALYSIS]")
        st.subheader("**INSURANCE**")

        year= st.slider("**Select the Year**", Map_insurance["Years"].min(), Map_insurance["Years"].max())
        state= st.selectbox("**Select the State**", Map_insurance["States"].unique())
        Map_insur_plot1(Map_insurance,state,year)

        st.subheader("**TRANSACTION**")

        Map_Tranc_plot2(Map_transaction,state,year)

        st.subheader("**USER**")

        Map_User_plot(Map_user,state,year)



elif select == "TOP CHARTS":

    ques= st.selectbox("**Select the Question**",('Top Brands Of Mobiles Used','States With Lowest Trasaction Amount',
                                  'Districts With Highest Transaction Amount','Top 10 Districts With Lowest Transaction Amount',
                                  'Top 10 States With AppOpens','Least 10 States With AppOpens','States With Lowest Trasaction Count',
                                 'States With Highest Trasaction Count','States With Highest Trasaction Amount',
                                 'Top 50 Districts With Lowest Transaction Amount'))
    
    if ques=="Top Brands Of Mobiles Used":
        ques1()

    elif ques=="States With Lowest Trasaction Amount":
        ques2()

    elif ques=="Districts With Highest Transaction Amount":
        ques3()

    elif ques=="Top 10 Districts With Lowest Transaction Amount":
        ques4()

    elif ques=="Top 10 States With AppOpens":
        ques5()

    elif ques=="Least 10 States With AppOpens":
        ques6()

    elif ques=="States With Lowest Trasaction Count":
        ques7()

    elif ques=="States With Highest Trasaction Count":
        ques8()

    elif ques=="States With Highest Trasaction Amount":
        ques9()

    elif ques=="Top 50 Districts With Lowest Transaction Amount":
        ques10()
    
        

        





