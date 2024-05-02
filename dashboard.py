import pandas as pd
import streamlit as st 
import matplotlib.pyplot as plt
from millify import prettify


## This is to set the page configuration
st.set_page_config(
    page_title="Welcome to the EAS Streamlit",
    page_icon="👋",
    layout="wide"
)


     

#if "data" in st.session_state:
#    data_df = st.session_state["data"]
#else:
#     data_df = None

#importing the image
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/SAP_2011_logo.svg/440px-SAP_2011_logo.svg.png", width=100)


st.sidebar.success("Select the option above:")


st.title('Welcome to EAS Pipeline')
#st.subheader('This is an experiment project to understand on how to utilize the Streamlit and deploy this in the CF')


st.markdown('Use this as the test to the application - all the information are confidential and not for sharing')
st.divider()


## Function to load the data:
@st.cache_data
def load_data(file_name):
    data_df = pd.read_csv(file_name)
    return data_df

#if data_df is None:
file_name = st.sidebar.file_uploader('Select Your Local EAS CSV: ')
if file_name is not None:
        data_df = load_data(file_name)
        data_df = data_df.fillna(0)
        st.session_state["data"] = data_df
else:
        st.warning("Please select a CSV file to continue!")
        st.stop()


## Setup the variables for data filtering
btp = data_df.query('`Solution Area (L1)` == "Business Technology Platform"')


## Function to retrieve unique values from DataFrame columns
def get_unique_values(dataframe, column):
    return dataframe[column].unique()

## Defining the variables to get the unique_values
region_values = get_unique_values(data_df, "Region Lvl 2")
quarter_values = get_unique_values(data_df, "Closing Qtr")
lob_values = get_unique_values(data_df,"Solution Area (L1)")
opp_phase_values = get_unique_values(data_df,"Opp Phase")
drm_values = get_unique_values(data_df, "DRM Category")
industry = get_unique_values(data_df,"ISS")
btp_l2 = get_unique_values(btp,"Sub-Solution Area (L2)")

## Input widgets in the sidebar
with st.sidebar:
    selected_region = st.multiselect("Please select the region: ", region_values, default=region_values )
with st.sidebar:
    selected_lob = st.multiselect("Please select the region: ", lob_values, default="Business Technology Platform")
with st.sidebar:
    selected_quarter = st.multiselect("Please select the Closing Qtr: ",quarter_values, default=quarter_values)
with st.sidebar:
    selected_drm = st.multiselect("Please select the DRM Category: ", drm_values, default=drm_values )
with st.sidebar:
    selected_iss = st.multiselect("Please select the Industry: ", industry, default=industry)

## Data Filtering
selected_data = data_df.query("(`Region Lvl 2` == @selected_region) & (`Closing Qtr` == @selected_quarter) & (`Solution Area (L1)` == @selected_lob) & (`DRM Category` == @selected_drm) & (`ISS` == @selected_iss) ")
selected_data_pivot = selected_data.pivot_table(index="Region Lvl 2", 
                                                columns=["DRM Category"],values="ACV kEUR", fill_value=0, aggfunc="sum")
selected_data_pivot.loc["CS APJ"] = selected_data_pivot.sum(numeric_only=True, axis=0)
selected_data_pivot.loc[:,"Total"] = selected_data_pivot.sum(numeric_only=True, axis=1)

selected_data_pivot = selected_data_pivot.style.set_properties(**{"border": "1px solid black"})\
    .format(precision=0, thousands=',') \
    .highlight_max(color='lightgreen') \
    .highlight_min(color='pink') 


selected_data_sol2_pivot = selected_data.pivot_table(index="Sub-Solution Area (L2)", 
                                                columns=["DRM Category"],values="ACV kEUR", fill_value=0, aggfunc="sum")
selected_data_sol2_pivot.loc["CS APJ"] = selected_data_sol2_pivot.sum(numeric_only=True, axis=0)
selected_data_sol2_pivot.loc[:,"Total"] = selected_data_sol2_pivot.sum(numeric_only=True, axis=1)

selected_data_sol2_pivot = selected_data_sol2_pivot.style.set_properties(**{"border": "1px solid black"})\
    .format(precision=0, thousands=',') \
    .highlight_max(color='lightgreen') \
    .highlight_min(color='pink') 



selected_data_dist_pivot = selected_data.pivot_table(index="Distribution Channel", 
                                                columns=["Sub-Solution Area (L2)"],values="ACV kEUR", fill_value=0, aggfunc="sum")
selected_data_dist_pivot.loc["Total"] = selected_data_dist_pivot.sum(numeric_only=True, axis=0)
selected_data_dist_pivot = selected_data_dist_pivot.style.set_properties(**{"border": "1px solid black"})\
    .format(precision=0, thousands=',') \
    .highlight_max(color='lightgreen') \
    .highlight_min(color='pink')

## RISE Participation
CloudERP = data_df.query('(`Region Lvl 2` == @selected_region) & (`Closing Qtr` in @selected_quarter) & (`Solution Area (L1)` == "Cloud ERP") & (`DRM Category` == @selected_drm) & (`ISS` == @selected_iss)')

CloudERP_Grp = CloudERP.groupby(["Planning Entity ID","Opportunity ID","Account Name","Region Lvl 2","Closing Qtr", "ISS"])[["ACV kEUR","TCV kEUR","# of Opps"]].sum()
CloudERP_Grp = CloudERP_Grp.reset_index()


Merge_CloudERP_Pivot = CloudERP_Grp.pivot_table(index="Region Lvl 2",
                                                columns="Closing Qtr",
                                                values = ["ACV kEUR","# of Opps"], fill_value=0,
                                                aggfunc="sum")
# Uncomment below if you want to find out the Summary of ERP
# st.write(Merge_CloudERP_Pivot)

## BTP Participation in RISE
selected_participation = data_df.query('(`Region Lvl 2` == @selected_region) & (`Closing Qtr` in @selected_quarter) & (`Solution Area (L1)` == @selected_lob) & (`DRM Category` == @selected_drm) & (`ISS` == @selected_iss)')

selected_participation_4Merge = selected_participation.groupby(["Planning Entity ID","Opportunity ID","Account Name","Region Lvl 2","Closing Qtr","ISS"])[["ACV kEUR","TCV kEUR","# of Opps"]].sum()

selected_participation_4Merge = selected_participation_4Merge.reset_index()

Merge_selected_participation_4Merge_Pivot = selected_participation_4Merge.pivot_table(index="Region Lvl 2",columns="Closing Qtr", values = ["ACV kEUR","# of Opps"], fill_value=0, aggfunc="sum")
# Uncomment below if you want to find out the Summary of BTP
#st.write(Merge_selected_participation_4Merge_Pivot)

## Calculating the BTP Participation in RISE
BTP4RISE = pd.merge(CloudERP_Grp,selected_participation_4Merge, 
                        on=["Planning Entity ID","Opportunity ID","Account Name","Region Lvl 2","Closing Qtr","ISS"], 
                        how="left",suffixes=("_ERP","_BTP"))
BTP4RISE = BTP4RISE.fillna(0)


## To find out top deals without BTP
BTP4RISE_noBTP = BTP4RISE.query('(`ACV kEUR_BTP` ==0)')
BTP4RISE_noBTP = BTP4RISE_noBTP.reset_index() \
    .sort_values("ACV kEUR_ERP", ascending=False).head(25)

BTP4RISE_noBTP_All = pd.merge(CloudERP, BTP4RISE_noBTP,
                            on=["Opportunity ID","Planning Entity ID"], how="left")
BTP4RISE_noBTP_All_Grp = round(BTP4RISE_noBTP_All.groupby(
    ["Account Name_x","Opp Description","Product Name (LPR)"])[["ACV kEUR"]].sum(),2)
                                                    
BTP4RISE_noBTP_All_Grp = BTP4RISE_noBTP_All_Grp.reset_index() \
    .sort_values("ACV kEUR", ascending=False).head(25)

## To calculate the participation including % by value and % by count
BTP4RISE_pivot = BTP4RISE.pivot_table(index="Region Lvl 2",
                                                values = ["ACV kEUR_ERP","ACV kEUR_BTP",
                                                        "# of Opps_ERP","# of Opps_BTP"],
                                                aggfunc="sum")


BTP4RISE_pivot.loc["CS APJ"]=BTP4RISE_pivot.sum(numeric_only=True, axis=0)

BTP4RISE_pivot = BTP4RISE_pivot.assign(
    by_value = BTP4RISE_pivot["ACV kEUR_BTP"]/BTP4RISE_pivot["ACV kEUR_ERP"]*100,
    by_count = BTP4RISE_pivot['# of Opps_BTP']/BTP4RISE_pivot["# of Opps_ERP"]*100
)

## For Top Deals
selected_data_top = selected_data[["Region Lvl 2","Account Name","Opp Description","Closing Qtr",
                                                "DRM Category","Opp Phase","ACV kEUR"]]
selected_data_top["# of Opp"] = 1
selected_data_top_table = round(selected_data_top.groupby(["Region Lvl 2","Account Name","Opp Description","Opp Phase"])[["ACV kEUR"]].sum(),2)
selected_data_top_table = selected_data_top_table.reset_index()
selected_data_top = selected_data_top.reset_index()
selected_data_top_table = selected_data_top_table.sort_values('ACV kEUR', ascending=False).head(25).style.format(precision=0, thousands=',') \
    .highlight_max(color='lightgreen') \
    .highlight_min(color='pink')

selected_data_booked= selected_data.query('(`DRM Category` == "Booked/Won")')["ACV kEUR"].sum()
selected_data_adrm = selected_data.query('(`DRM Category` in ["Committed","Probable"])')["ACV kEUR"].sum()
selected_data_upside = selected_data.query('(`DRM Category` in ["Upside"])')["ACV kEUR"].sum()



## Displaying 
container = st.container(border=True)
tab1, tab2, tab3 = st.tabs(["Summary", "RISE Participation","Top Deals"])

with container:
    with tab1:
        st.header("Based on DRM Category")
        st.dataframe(selected_data_pivot, width=680)
        st.subheader("Graphical Representation based on DRM Category")
        st.bar_chart(selected_data_pivot, width=680)
        st.divider()

        st.header("Based on Distribution Channel ")
        st.dataframe(selected_data_dist_pivot, use_container_width=True)
        st.subheader("Graphical Representation based on Distribution Channel")
        st.bar_chart(selected_data_dist_pivot, width=680)
        st.divider()

        st.header("Based on Solution Area (L2)")
        st.dataframe(selected_data_sol2_pivot, use_container_width=True)
        st.subheader("Graphical Representation based on Solution Area (L2)")
        st.bar_chart(selected_data_sol2_pivot)
    
    with tab2:
        st.markdown('This is the Top 25 deals without BTP')
        st.data_editor(BTP4RISE_noBTP_All_Grp, hide_index=True)
        st.divider()
        st.subheader("BTP Inclusion in RISE (ACV kEUR)")
        st.write(BTP4RISE_pivot.style.set_properties(**{"border": "1px solid black"})\
            .format(precision=0, thousands=',') \
            .format('{:.02f}%', subset=["by_value","by_count"])
            .highlight_max(color='lightgreen') \
            .highlight_min(color='pink') )
    
    with tab3:
        st.header("Top 25 deals")
        st.write("Key Metrics - All deals")
        col1, col2, col3 = st.columns(3)
        col1.metric("Booked/Won", prettify(round(selected_data_booked,2)))
        col2.metric("ADRM", prettify(round(selected_data_adrm,2)))
        col3.metric("Upside", prettify(round(selected_data_upside,2)))

        st.divider()
        st.data_editor(selected_data_top_table, hide_index=True, height=800)
        st.subheader("Graphical Representation based on All deals")
        #st.scatter_chart(selected_data, x="Region Lvl 2", y="Opp Phase", color="DRM Category", size="ACV kEUR", height=400, width=800)
        st.scatter_chart(selected_data, y="Opp Phase", x="Closing Qtr", color="DRM Category", size="ACV kEUR")
        #st.bar_chart(selected_data_top, x="Closing Qtr", y="ACV kEUR", color="DRM Category")
