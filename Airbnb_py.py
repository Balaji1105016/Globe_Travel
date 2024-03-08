import streamlit as st
import pandas as pd
import base64
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from PIL import Image
from wordcloud import WordCloud as WC
from streamlit_option_menu import option_menu


Airbnb_df = pd.read_csv("MongoDB_Airbnb_DF_1.csv")

st.title("Globe-Travel")
img_path = r"C:\Users\Balaji\AppData\Roaming\Python\Python312\Scripts\Globe.png"
image = Image.open(img_path)
st.image(image)

if 'login_status' not in st.session_state:
    st.session_state.login_status = False
    
username = st.text_input("User Name")
password = st.text_input("Password",type = 'password')
if st.button("Login"):
    if username == "Balaji" and password == "Balaji@123":
        st.session_state.login_status = True
        st.success("Login Successful!")
    
    else:
        st.session_state.login_status = False
        st.error("Invalid Credentials. Please try again.")

if st.session_state.login_status:      
    logout = st.sidebar.button("Logout")
    if logout:
        if 'login_status' in st.session_state:
            st.session_state.login_status = False
            st.experimental_rerun()

    with st.sidebar:
        menu_sel = option_menu("Menu", ["Home","Analysis","About"], 
                    icons=["house","graph-up-arrow", "list-task"],
                    styles={"nav-link": {"font-size": "22 px", "text-align": "left", "margin": "-1px", "--hover-color": "#FF9392"},
                            "nav-link-selected": {"background-color": "#FF9392"}})
        
        
    if menu_sel == "Home":
        st.header("Airbnb Data Importance")
        st.write("""
                Note: Airbnb data is integral to the platform's success, enabling it to offer a personalized and secure experience for both hosts and guests, optimize pricing strategies, and adapt to changing market dynamics.
                
                1) Market Insights: Airbnb data provides valuable insights into the demand and supply dynamics of the short-term rental market. Hosts and property managers can use this information to make informed decisions about pricing, occupancy rates, and property features.\n
                2) User Experience Enhancement: By analyzing user behavior, preferences, and reviews, Airbnb can continually improve its platform to enhance the overall user experience. This includes optimizing search algorithms, suggesting personalized recommendations, and implementing features that resonate with users.\n
                3) Dynamic Pricing: Airbnb uses data to implement dynamic pricing strategies. This involves adjusting rental prices based on factors such as demand, seasonality, local events, and competitor pricing. Dynamic pricing helps hosts maximize their revenue while ensuring affordability for guests.\n
                4) Fraud Detection and Security: Airbnb employs data analytics to detect and prevent fraudulent activities on its platform. This includes identifying fake listings, suspicious payment transactions, and potential security risks. This proactive approach helps maintain trust and safety for both hosts and guests.\n
                5) Host and Guest Matching: Data-driven algorithms are used to match hosts with potential guests based on their preferences, past interactions, and reviews. This ensures a better fit and enhances the likelihood of positive experiences for both parties.\n
                    
                """) 

    if menu_sel == "Analysis":
        st.header("ANALYSIS")
        Analysis = st.selectbox("Options",("Price Analysis Based On Country, Property Type & Room Type","Price Analysis Based on Suburb","Price Analysis Based On Property Type & Room Type","Indepth Price Analysis For Listings Based On Map View","Total Properties Count Based on Country,Property Type & Room Type","Top 10 Host Names","Top 10 Property_Type List","Availability","List Of Amenities","Resources"))
        if Analysis == "Price Analysis Based On Country, Property Type & Room Type":
            st.subheader("Average Price Analysis Based On Country, Property Type & Room Type")
            st.success("Note: This Module Provides the Detailed Analysis About the Average Price Based On Country,Property Type & Room Type")
            Country = st.selectbox("Select the Country", ('Canada', 'Turkey', 'United States', 'Brazil', 'Australia',
                                                    'Portugal', 'Hong Kong', 'Spain', 'China'))
            Property_Type = st.multiselect("Select The Property Type", Airbnb_df.Property_Type.unique())
            Room_Type = st.multiselect("Select The Room Type", Airbnb_df.Room_Type.unique())
            Price_Range = st.slider("Choose the Price Range", Airbnb_df.Price.min(), Airbnb_df.Price.max(), (Airbnb_df.Price.min(), Airbnb_df.Price.max()))
            q1 = f"Country == '{Country}' & Property_Type in {Property_Type} & Room_Type in {Room_Type} & Price >= {Price_Range[0]} & Price <= {Price_Range[1]}"
            submit_button = st.button("Submit")
            if submit_button:
                df_1 = Airbnb_df.query(q1).groupby(['Country', 'Property_Type', 'Room_Type'], as_index=False)['Price'].mean()
                fig = px.scatter_geo(data_frame=df_1, locations='Country',
                                    color='Price',
                                    hover_data=['Price', 'Property_Type', 'Room_Type'],
                                    locationmode='country names',
                                    size='Price',
                                    size_max=100,
                                    title='Average Price Exploration Based On Country, Property Type & Room Type',
                                    color_continuous_scale=px.colors.sequential.Rainbow_r)
                fig.update_traces(hoverlabel=dict(font=dict(color='black')))#-->changing the Hover Data Text Colour
                fig.update_geos(bgcolor='darkcyan')#-->Changing the Map Background Colour
                st.plotly_chart(fig)
                
        elif Analysis == "Price Analysis Based on Suburb":
            st.success("This Module Provides The Information About Top 100 Highiest Priced Properties And Top 100 Least Priced Properties Based On Suburb, Country. It Also Provides The Information About The Country,Street,Property Type,Room Type,Name Of The Property")
            st.subheader("Top 100 Highiest Priced Properties Based On Suburb, Country")
            filter_df_0 = Airbnb_df.nlargest(100,"Price")
            fig_0 = px.line(
                filter_df_0,
                x="Suburb",
                y="Price",
                color="Country",
                labels={"Price": "Price", "Suburb": "Suburb"},
                hover_data=["Country","Suburb","Street","Property_Type","Room_Type","Name","Price"],
                line_shape="spline",
                title="Top 100 Highiest Priced Properties Based On Suburb, Country")
            fig_0.update_traces(hoverlabel=dict(font=dict(color='black')))
            st.plotly_chart(fig_0)
            
            st.subheader("Top 100 Least Priced Properties Based On Suburb")
            filter_df_1 = Airbnb_df[:100].sort_values(by="Price",ascending=True)
            fig_1 = px.line(
                filter_df_1,
                x="Suburb",
                y="Price",
                color="Country",
                labels={"Price": "Price", "Suburb": "Suburb"},
                hover_data=["Country","Suburb","Street","Property_Type","Room_Type","Name","Price"],
                title="Top 100 Least Prices Based on Suburb")
            fig_1.update_traces(hoverlabel=dict(font=dict(color='black')))
            st.plotly_chart(fig_1)   
        
        if Analysis == "Price Analysis Based On Property Type & Room Type":
            st.success("Note: This Module Provides The Information About The Average Price Based On Property Type And The Room Type")
            st.subheader("Average Price Analysis by Room Type & Property Type")
            plt.figure(figsize=(7, 7))
            data = Airbnb_df.pivot_table(index = 'Property_Type',columns='Room_Type', values='Price',aggfunc="mean")
            sns.heatmap(data, cmap='YlGnBu', annot=True, fmt=".2f", linewidths=.20)
            plt.title('Average Price Analysis by Room Type and Property Type')
            st.pyplot(plt)
            
        if Analysis ==  "Indepth Price Analysis For Listings Based On Map View":
            st.success("Note:This Module Provides the Indepth Price Analysis About Almost All The Required Fields For Analysing The Listings And In This Module The Users Can Also Download The Report In the Form Of CSV File")
            
            data = {
                "Name": Airbnb_df["Name"].tolist(),
                "Rating": Airbnb_df["Rating"].tolist(),
                "Total_Number_Of_Reviews":Airbnb_df["Total_Number_Of_Reviews"].tolist(),
                "Price": Airbnb_df["Price"].tolist(),
                "Property_Type": Airbnb_df["Property_Type"].tolist(),
                "Room_Type": Airbnb_df["Property_Type"].tolist(),
                "Accommodates": Airbnb_df["Accommodates"].tolist(),
                "No_Of_Bedrooms": Airbnb_df["No_Of_Bedrooms"].tolist(),
                "No_Of_Beds": Airbnb_df["No_Of_Beds"].tolist(),
                "Bathrooms": Airbnb_df["Bathrooms"].tolist(),
                "Aminities": Airbnb_df["Aminities"].tolist(),
                "Minimum_Nights": Airbnb_df["Minimum_Nights"].tolist(),
                "Maximum_Nights": Airbnb_df["Maximum_Nights"].tolist(),
                "Host_Name": Airbnb_df["Host_Name"].tolist(),
                "Cancellation_Policy": Airbnb_df["Cancellation_Policy"].tolist(),
                "Additional_People_Charge": Airbnb_df["Additional_People_Charge"].tolist(),
                "Cleaning_Charge": Airbnb_df["Cleaning_Charge"].tolist(),
                "Deposit_Amount": Airbnb_df["Deposit_Amount"].tolist(),
                "Country":Airbnb_df["Country"].tolist(),
                "Suburb":Airbnb_df["Suburb"].tolist(),
                "Street":Airbnb_df["Street"].tolist(),
                "Availability_365": Airbnb_df["Availability_365"].tolist(),
                "Availability_90": Airbnb_df["Availability_90"].tolist(),
                "Availability_60": Airbnb_df["Availability_60"].tolist(),
                "Availability_30": Airbnb_df["Availability_30"].tolist(),
                "Lat": Airbnb_df["Lat"].tolist(),
                "Long": Airbnb_df["Long"].tolist()}

            new_df = pd.DataFrame(data)

            fig = px.scatter_mapbox(new_df,
                                lat='Lat',
                                lon='Long',
                                text = "Name",
                                hover_data=["Name","Rating","Total_Number_Of_Reviews","Price","Availability_365","Availability_90","Availability_60","Availability_30","Property_Type",
                                    "Room_Type","Accommodates","No_Of_Bedrooms","No_Of_Beds","Bathrooms",
                                    "Minimum_Nights","Maximum_Nights","Host_Name","Cancellation_Policy",
                                    "Additional_People_Charge","Cleaning_Charge","Deposit_Amount","Street","Suburb",
                                    "Country"],
                                
                                color='Price',
                                color_continuous_scale=px.colors.sequential.Rainbow_r,
                                size = "Price",
                                size_max=50,
                                zoom = -1,
                                height=800)
            
            fig.update_traces(hoverlabel=dict(font=dict(color='black')))#-->#-->changing the Hover Data Text Colour
            fig.update_layout(mapbox_style="open-street-map")
            
            st.plotly_chart(fig)
            
            clicked_data = st.multiselect("Select a data point", new_df['Name'])
            if st.button("Download CSV"):
                selected_data = new_df[new_df['Name'].isin(clicked_data)]
                # Downloading as CSV
                csv_string = selected_data.to_csv(index=False, encoding='utf-8')#--> Using utf-8 for preventing data loss since some characters were in chinese(Multilingual Dataset) 
                b64 = base64.b64encode(csv_string.encode()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download CSV</a>'
                st.markdown(href, unsafe_allow_html=True)
                
        if Analysis == "Total Properties Count Based on Country,Property Type & Room Type":
            st.success("Note: This Module Provides the Information About The Total Property Count Based On Country,Property Type,Room Type")
            Country = st.selectbox("Select the Country", ('Canada', 'Turkey', 'United States', 'Brazil', 'Australia',
                                                    'Portugal', 'Hong Kong', 'Spain', 'China'))

            Property_Type = st.multiselect("Select The Property Type", Airbnb_df.Property_Type.unique())
            Room_Type = st.multiselect("Select The Room Type", Airbnb_df.Room_Type.unique())
            q7 = f"Country == '{Country}' & Property_Type in {Property_Type} & Room_Type in {Room_Type}"
            button = st.button("Submit")
            if button:
                new_df_5 = Airbnb_df.query(q7).groupby(["Country", 'Property_Type', 'Room_Type'],as_index=False)["Name"].value_counts()
                st.write(new_df_5)
                fig_7 = px.sunburst(
                    new_df_5,
                    path=["Room_Type","Property_Type","Country"],
                    hover_data=["Room_Type","Property_Type","Country"],
                    color_continuous_scale= px.colors.sequential.Rainbow_r,
                    title = "Total Properties Count Based on Country,Property Type & Room Type"
                )
                st.plotly_chart(fig_7)
        
        if Analysis == "Top 10 Host Names":
            st.success("Note: This Module Provides The Information About The Top 10 Host Names")
            plt.figure(figsize=(10,8))
            data = sns.countplot(data=Airbnb_df,y=Airbnb_df.Host_Name,order=Airbnb_df.Host_Name.value_counts().index[:10],hue = "Host_Name")
            data.set_title("Top 10 Poperty Owner Name List")
            st.pyplot(plt)
            
        if Analysis == "Top 10 Property_Type List":
            st.success("Note: This Module Provides The Information About The Top 10 Property Type List")
            plt.figure(figsize=(10,8))
            data = sns.countplot(data=Airbnb_df,y=Airbnb_df.Property_Type,order=Airbnb_df.Property_Type.value_counts().index[:10],hue="Property_Type")
            data.set_title("Top 10 Poperty Type List")
            st.pyplot(plt)
            
        if Analysis == "Availability":
            st.success("Note: This Module Provides A Detailed Analysis about Property Average Availability Based On Country,Property Type & Room Type")
            Country = st.selectbox("Select the Country", ('Canada', 'Turkey', 'United States', 'Brazil', 'Australia',
                                                    'Portugal', 'Hong Kong', 'Spain', 'China'))
            Property_Type = st.multiselect("Select The Property Type", Airbnb_df.Property_Type.unique())
            Room_Type = st.multiselect("Select The Room Type", Airbnb_df.Room_Type.unique())
            q2 = f"Country == '{Country}' & Property_Type in {Property_Type} & Room_Type in {Room_Type}"
            submit_button_1 = st.button("Submit")
            if submit_button_1:
                st.subheader("Average Availability For A Year Based On Country,Property Type & Room Type")
                new_df_1 = Airbnb_df.query(q2).groupby(["Country","Property_Type","Room_Type"],as_index=False)["Availability_365"].mean()
                fig_3 = px.scatter_geo(
                    
                                data_frame=new_df_1,
                                locations = "Country",
                                color= "Availability_365",
                                color_continuous_scale= px.colors.sequential.Rainbow_r,
                                hover_data= ["Country","Property_Type","Room_Type","Availability_365"],
                                locationmode= "country names",
                                size="Availability_365",
                                size_max= 100)
                
                fig_3.update_traces(hoverlabel=dict(font=dict(color='black')))#-->changing the Hover Data Text Colour
                fig_3.update_geos(bgcolor='darkcyan')#-->Changing the Map Background Colour
                st.plotly_chart(fig_3)
                
                st.subheader("Average Availability For A Quarter Based On Country,Property Type & Room Type")
                new_df_2 = Airbnb_df.query(q2).groupby(["Country","Property_Type","Room_Type"],as_index=False)["Availability_90"].mean()
                fig_4 = px.scatter_geo(
                    
                                data_frame=new_df_2,
                                locations = "Country",
                                color= "Availability_90",
                                color_continuous_scale= px.colors.sequential.Rainbow,
                                hover_data= ["Country","Property_Type","Room_Type","Availability_90"],
                                locationmode= "country names",
                                size="Availability_90",
                                size_max= 100)
                
                fig_4.update_traces(hoverlabel=dict(font=dict(color='black')))#-->changing the Hover Data Text Colour
                fig_4.update_geos(bgcolor='darkcyan')#-->Changing the Map Background Colour
                st.plotly_chart(fig_4)
                
                st.subheader("Average Availability For Two Months Based On Country,Property Type & Room Type")
                new_df_3 = Airbnb_df.query(q2).groupby(["Country","Property_Type","Room_Type"],as_index=False)["Availability_60"].mean()
                fig_5 = px.scatter_geo(
                    
                    data_frame=new_df_3,
                    locations = "Country",
                    color= "Availability_60",
                    color_continuous_scale= px.colors.sequential.Agsunset,
                    hover_data= ["Country","Property_Type","Room_Type","Availability_60"],
                    locationmode= "country names",
                    size="Availability_60",
                    size_max= 100
                    
                )
                fig_5.update_traces(hoverlabel=dict(font=dict(color='black')))#-->changing the Hover Data Text Colour
                fig_5.update_geos(bgcolor='darkcyan')#-->Changing the Map Background Colour
                st.plotly_chart(fig_5)
                
                st.subheader("Average Availability For A Month Based On Country,Property Type & Room Type")
                new_df_4 = Airbnb_df.query(q2).groupby(["Country","Property_Type","Room_Type"],as_index=False)["Availability_30"].mean()
                fig_6 = px.scatter_geo(
                    
                    data_frame=new_df_4,
                    locations = "Country",
                    color= "Availability_30",
                    color_continuous_scale= px.colors.sequential.Agsunset_r,
                    hover_data= ["Country","Property_Type","Room_Type","Availability_30"],
                    locationmode= "country names",
                    size="Availability_30",
                    size_max= 100
                    
                )
                fig_6.update_traces(hoverlabel=dict(font=dict(color='black')))#-->changing the Hover Data Text Colour
                fig_6.update_geos(bgcolor='darkcyan')#-->Changing the Map Background Colour
                st.plotly_chart(fig_6)
                
        if Analysis == "List Of Amenities":
            st.subheader("List Of Famous Amenities in Airbnb")
            st.success("Note: This Module Provides The Information About The List Of Famous Amenities in Airbnb")
            
            Airbnb_df['Aminities'] = Airbnb_df['Aminities'].fillna('')
            text = " ".join(Airbnb_df['Aminities'])
            
            wordcloud = WC(width=1200, height=600, background_color='white').generate(text)
            st.image(wordcloud.to_image(), caption='Amenities WordCloud', use_column_width=True)
            
        if Analysis == "Resources":
            st.subheader("Resources")
            st.success("Note: This Module Provides The Information About The List Of Available Resources")
            st.subheader("Country Information")
            st.dataframe(Airbnb_df["Country"].unique())
            st.subheader("Suburb Information")
            st.dataframe(Airbnb_df["Suburb"].unique())
            st.subheader("Property Type Information")
            st.dataframe(Airbnb_df["Property_Type"].unique())
            st.subheader("Room Type Information")
            st.dataframe(Airbnb_df["Room_Type"].unique())
            
    if menu_sel == "About":
        img_path = r"C:\Users\Balaji\Music\Personal_Pic\Balaji_pic.jpeg"
        img = Image.open(img_path)
        st.image(img, caption="""Name: BALAJI BALAKRISHNAN(Data Engineer)""", use_column_width=True)
        st.write("Applitaion Name: ")
        st.write("Developed By: Balaji Balakrishnan")
        st.write("Designation: Data Engineer")
        st.write("Industry Experience: 7+ Years")
        st.write("Worked Companies: FLEX,TCS,DvSuM India Private Limited")
        st.write("Tech Skills: SQL,PL-SQL,Oracle,Python,MongoDB,AWS,Tableau,Streamlit,ServiceNow")
        st.markdown("Linkedin URL: https://www.linkedin.com/in/balaji-balakrishnan-34471b167/")
        st.markdown("GitHub URL: ")


        

            
            
        
            
            
            
            
            


     
    
    
    
    
    
    
    
    
    
    
    
