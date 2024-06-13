#############################################
# Importing all the module
#############################################

import pandas as pd
import streamlit as st 
import matplotlib.pyplot as plt
import plotly.express as px
from millify import prettify
import plotly.graph_objects as go

## This is to set the page configuration
st.set_page_config(
    page_title="Welcome to the EAS Streamlit",
    page_icon="👋",
    layout="wide"
)

#############################################
# Main Page Setup
#############################################

#importing the image
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/SAP_2011_logo.svg/440px-SAP_2011_logo.svg.png", width=100)
st.sidebar.success("Select the option above:")

st.title('Welcome to EAS Pipeline')
st.markdown('Use this as the test to the application - all the information are confidential and not for sharing')
st.divider()


#############################################
# Functions 
#############################################

#@st.cache_data
def load_data(file_name):
    data_df = pd.read_csv(file_name)
    return data_df

def get_unique_values(dataframe, column):
    return dataframe[column].unique()

def deal_classification(x):
    if x>5000:
         return '1: 5M+'
    elif x >= 3000:
        return '2: 3M+ - 5M+'
    elif x >= 1000:
        return '3: 1M+ - 3M+'
    elif x >= 500:
        return '4: 500K - 1M'
    elif x >= 250:
        return '5: 250K - 500K'
    elif x >= 150:
        return '6: 150K - 250K'
    elif x >= 50:
        return '7: 50K - 150K'
    elif x >= 20:
        return '8: 20K - 50K'
    else:
        return '9: <20K'
    
def plot_pie(indicator_number, indicator_label,title_text):
     fig = go.Figure(
          go.Pie(values=indicator_number,
                 labels=indicator_label,
                 hole=.3
                 ))
     fig.update_layout(
        # paper_bgcolor="lightgrey",
        title_text=title_text, #title_x=0.2,
        height=300, width=500,
        margin=dict(l=10, r=10, t=50, b=10, pad=8),
        )
     st.plotly_chart(fig) #,use_container_width=True)

def plot_gauge(
    indicator_number, indicator_color, indicator_suffix, indicator_title, max_bound
):
    fig = go.Figure(
        go.Indicator(
            value=indicator_number,
            mode="gauge+number+delta",
            domain={"x": [0, 1], "y": [0, 1]},
            number={
                "suffix": indicator_suffix,
                "font.size": 24,
            },
            gauge={
                "axis": {"range": [0, max_bound*1.2], "tickwidth": 1},
                "bar": {"color": indicator_color},
                "threshold" : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': max_bound}
            },
            #title={
            #    "text": indicator_title,
            #    "font": {"size": 28},
            #},
            delta = {'reference': max_bound},
        )
    )
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        title_text=indicator_title,#, title_x=0.05,
        height=300, width=300, 
        margin=dict(l=1, r=1, t=50, b=10, pad=2),
    )
    st.plotly_chart(fig) #,use_container_width=True)


def plot_bar(x,y,color,title):
    fig = px.bar(graph_line,x=x,y=y, color=color)

    fig.update_layout(
        # paper_bgcolor="lightgrey",
        title_text=title,#, title_x=0.05,
        height=300, width=500, 
        margin=dict(l=1, r=1, t=50, b=10, pad=2),
    )
    st.plotly_chart(fig, use_container_width=True)

#############################################
# Uploading the file
#############################################

file_name = st.sidebar.file_uploader('Select Your Local EAS CSV: ', key="pipeline")

if file_name is not None:
        data_df = load_data(file_name)
        data_df = data_df.fillna(0)
else:
        st.warning("Please select a CSV file to continue!")
        st.stop()




## Defining the variables to get the unique_values
region_values = get_unique_values(data_df, "Region Lvl 2")
quarter_values = get_unique_values(data_df, "Closing Qtr")
lob_values = get_unique_values(data_df,"Solution Area (L1)")
opp_phase_values = get_unique_values(data_df,"Opp Phase")
drm_values = get_unique_values(data_df, "DRM Category")
industry = ["Transform","Industry Led","Midmarket"]

#############################################
# Side Bar
#############################################

with st.sidebar:
    selected_region = st.multiselect("Please select the region: ", region_values, default=region_values )
with st.sidebar:
    selected_lob = st.multiselect("Please select the LoB: ", lob_values, default=lob_values)
with st.sidebar:
    selected_quarter = st.multiselect("Please select the Closing Qtr: ",quarter_values, default=quarter_values)
with st.sidebar:
    selected_iss = st.multiselect("Please select the Segment: ", industry, default=industry)

## Selecting the data to allow the conditional selection
selected_data = data_df.query("(`Region Lvl 2` == @selected_region) & (`Closing Qtr` == @selected_quarter) & (`Solution Area (L1)` == @selected_lob) & (`ISS` == @selected_iss)")

selected_sol_l2 = selected_data.query("`Solution Area (L1)` == @selected_lob")
selected_sol_l2_unique = get_unique_values(selected_sol_l2,"Sub-Solution Area (L2)")

selected_reg_l3 = selected_data.query("`Region Lvl 2` == @selected_region")
selected_reg_l3_unique = get_unique_values(selected_reg_l3,"Region Lvl 3")

## Additional Selection
with st.sidebar:
     selected_l3 = st.multiselect("Please select L2: ", selected_sol_l2_unique, default=selected_sol_l2_unique)
with st.sidebar:
     selected_reg_l3 = st.multiselect("Please select Region L3: ", selected_reg_l3_unique, default=selected_reg_l3_unique)




#######################################
# BASE DATA DEFINITION
#######################################



## Defining the data selection
selected_data = data_df.query("(`Region Lvl 2` == @selected_region) & (`Closing Qtr` == @selected_quarter) & (`Solution Area (L1)` == @selected_lob) & (`ISS` == @selected_iss) & (`Sub-Solution Area (L2)` == @selected_l3) & (`Region Lvl 3` == @selected_reg_l3)")

## Shorter the columns for graph


selected_data_grp = selected_data.groupby(["Region Lvl 2","Region Lvl 3","Planning Entity ID","Account Name","Opportunity ID","Product Name (LPR)","Closing Qtr","DRM Category","Opp Description","Opp Owner Name","Solution Area L3","Solution Area L4"])[["ACV kEUR"]].sum().reset_index()

selected_data_grp_preview = selected_data_grp[["Region Lvl 3","Opportunity ID","Account Name","Opp Owner Name","Opp Description","Solution Area L3","ACV kEUR"]].sort_values('ACV kEUR', ascending=False)

graph_line = round(selected_data.groupby(["Region Lvl 2","Closing Qtr","DRM Category"])[["ACV kEUR"]].sum()).reset_index()





#######################################
# Table - Displaying the items
#######################################


## Region Lvl 2 Data 
selected_data_pivot = selected_data.pivot_table(index="Region Lvl 2", 
                                                columns=["DRM Category"],values="ACV kEUR", fill_value=0, aggfunc="sum")

selected_data_pivot.loc["CS APJ"] = selected_data_pivot.sum(numeric_only=True, axis=0)
selected_data_pivot.loc[:,"Total"] = selected_data_pivot.sum(numeric_only=True, axis=1)

selected_data_pivot = selected_data_pivot.style.set_properties(**{"border": "1px solid black"})\
    .format(precision=0, thousands=',') \
    .highlight_min(color='pink') 


## Region Lvl 3 Data
selected_data_l3_pivot = selected_data.pivot_table(index="Region Lvl 3", 
                                            columns=["DRM Category"],values="ACV kEUR", fill_value=0, aggfunc="sum")
selected_data_l3_pivot.loc["CS APJ"] = selected_data_l3_pivot.sum(numeric_only=True, axis=0)
selected_data_l3_pivot.loc[:,"Total"] = selected_data_l3_pivot.sum(numeric_only=True, axis=1)

selected_data_l3_pivot = selected_data_l3_pivot.style.set_properties(**{"border": "1px solid black"})\
.format(precision=0, thousands=',') \
.highlight_max(color='lightgreen') \
.highlight_min(color='pink') 


## Solution Area L2 DATA
selected_data_sol2_pivot = selected_data.pivot_table(index="Sub-Solution Area (L2)", 
                                                columns=["DRM Category"],values="ACV kEUR", fill_value=0, aggfunc="sum")
selected_data_sol2_pivot.loc["CS APJ"] = selected_data_sol2_pivot.sum(numeric_only=True, axis=0)
selected_data_sol2_pivot.loc[:,"Total"] = selected_data_sol2_pivot.sum(numeric_only=True, axis=1)

selected_data_sol2_pivot = selected_data_sol2_pivot.style.set_properties(**{"border": "1px solid black"})\
    .format(precision=0, thousands=',') \
    .highlight_max(color='lightgreen') \
    .highlight_min(color='pink') 

## Distribution Channel DATA
selected_data_dist_pivot = selected_data.pivot_table(index="Distribution Channel", 
                                                columns=["Sub-Solution Area (L2)"],values="ACV kEUR", fill_value=0, aggfunc="sum")
selected_data_dist_pivot.loc["Total"] = selected_data_dist_pivot.sum(numeric_only=True, axis=0)
selected_data_dist_pivot = selected_data_dist_pivot.style.set_properties(**{"border": "1px solid black"})\
    .format(precision=0, thousands=',') \
    .highlight_max(color='lightgreen') \
    .highlight_min(color='pink')


## Based on the Opp Phase
selected_data_opp_phase_pivot = selected_data.pivot_table(index="Opp Phase", 
                                                columns=["Region Lvl 2"],values="ACV kEUR", fill_value=0, aggfunc="sum")
selected_data_opp_phase_pivot.loc["Total"] = selected_data_opp_phase_pivot.sum(numeric_only=True, axis=0)
selected_data_opp_phase_pivot = selected_data_opp_phase_pivot.style.set_properties(**{"border": "1px solid black"})\
    .format(precision=0, thousands=',') \
    .highlight_max(color='lightgreen') \
    .highlight_min(color='pink')

selected_data_opp_phase_count_pivot = selected_data.pivot_table(index="Opp Phase", 
                                                columns=["Region Lvl 2"],values="ACV kEUR", fill_value=0, aggfunc="count")
selected_data_opp_phase_count_pivot.loc["Total"] = selected_data_opp_phase_count_pivot.sum(numeric_only=True, axis=0)
selected_data_opp_phase_count_pivot = selected_data_opp_phase_count_pivot.style.set_properties(**{"border": "1px solid black"})\
    .format(precision=0, thousands=',') \
    .highlight_max(color='lightgreen') \
    .highlight_min(color='pink')


#######################################
# RISE PARTICIPATION
#######################################

CloudERP = data_df.query('(`Region Lvl 2` == @selected_region) & (`Closing Qtr` == @selected_quarter) & (`Solution Area (L1)` == "Cloud ERP") & (`ISS` == @selected_iss) & (`Region Lvl 3` == @selected_reg_l3)')

CloudERP_Grp = CloudERP.groupby(["Account Name","Opportunity ID","Planning Entity ID","Closing Qtr","DRM Category","Region Lvl 2","Region Lvl 3"])[["ACV kEUR","TCV kEUR"]].sum().reset_index()
CloudERP_Grp["Count"] = 1


## BTP Participation in RISE
btp_participation = data_df.query('(`Region Lvl 2` == @selected_region) & (`Closing Qtr` in @selected_quarter) & (`Solution Area (L1)` == "Business Technology Platform") & (`Sub-Solution Area (L2)` == @selected_l3) & (`Region Lvl 3` == @selected_reg_l3)')

btp_participation_Grp = btp_participation.groupby(["Account Name","Opportunity ID","Planning Entity ID","Closing Qtr","DRM Category","Region Lvl 2","Region Lvl 3"])[["ACV kEUR","TCV kEUR"]].sum().reset_index()
btp_participation_Grp["Count"] = 1
#st.write(btp_participation_Grp)

## Performing the Merging between the CloudERP and BTP
Merge = pd.merge(CloudERP_Grp, btp_participation_Grp, on=["Planning Entity ID","Opportunity ID","Account Name","Closing Qtr","DRM Category","Region Lvl 2","Region Lvl 3"], how="left", suffixes=("_ERP","_BTP"))

Merge = Merge.fillna(0)

Merge_Booked = Merge.query('(`DRM Category` == "Booked/Won")')
Merge_Booked_Pivot = (Merge_Booked.pivot_table(index="Region Lvl 2",
                                values=["ACV kEUR_ERP","Count_ERP","ACV kEUR_BTP","Count_BTP"],
                                fill_value=0, aggfunc="sum"))
Merge_Booked_Pivot.loc["CS APJ"] = Merge_Booked_Pivot.sum(numeric_only=True, axis=0)
Merge_Booked_Pivot = Merge_Booked_Pivot.assign(
    by_value = Merge_Booked_Pivot["ACV kEUR_BTP"]/Merge_Booked_Pivot["ACV kEUR_ERP"]*100,
    by_count = Merge_Booked_Pivot['Count_BTP']/Merge_Booked_Pivot["Count_ERP"]*100)


Merge_ADRM = Merge.query('(`DRM Category` in ["Committed","Probable"])')
Merge_ADRM_Pivot = (Merge_ADRM.pivot_table(index="Region Lvl 2",
                                values=["ACV kEUR_ERP","Count_ERP","ACV kEUR_BTP","Count_BTP"],
                                fill_value=0, aggfunc="sum"))
Merge_ADRM_Pivot.loc["CS APJ"] = Merge_ADRM_Pivot.sum(numeric_only=True, axis=0)
Merge_ADRM_Pivot = Merge_ADRM_Pivot.assign(
    by_value = Merge_ADRM_Pivot["ACV kEUR_BTP"]/Merge_ADRM_Pivot["ACV kEUR_ERP"]*100,
    by_count = Merge_ADRM_Pivot['Count_BTP']/Merge_ADRM_Pivot["Count_ERP"]*100)

Merge_Upside = Merge.query('(`DRM Category` in ["Upside"])')
Merge_Upside_Pivot = (Merge_Upside.pivot_table(index="Region Lvl 2",
                                values=["ACV kEUR_ERP","Count_ERP","ACV kEUR_BTP","Count_BTP"],
                                fill_value=0, aggfunc="sum"))
Merge_Upside_Pivot.loc["CS APJ"] = Merge_Upside_Pivot.sum(numeric_only=True, axis=0)
Merge_Upside_Pivot = Merge_Upside_Pivot.assign(
    by_value = Merge_Upside_Pivot["ACV kEUR_BTP"]/Merge_Upside_Pivot["ACV kEUR_ERP"]*100,
    by_count = Merge_Upside_Pivot['Count_BTP']/Merge_Upside_Pivot["Count_ERP"]*100)





Merge_Pivot = (Merge.pivot_table(index="Region Lvl 2",
                                values=["ACV kEUR_ERP","Count_ERP","ACV kEUR_BTP","Count_BTP"],
                                fill_value=0, aggfunc="sum"))

#######################################
# STANDALONE BTP DEALS - TAKING OUT THE RISE PARTICIPATION 
#######################################

btp = data_df.query("(`Region Lvl 2` == @selected_region) & (`Closing Qtr` == @selected_quarter) & (`Solution Area (L1)` == 'Business Technology Platform') & (`ISS` == @selected_iss) & (`Sub-Solution Area (L2)` == @selected_l3) & (`Region Lvl 3` == @selected_reg_l3)")

merged_df = pd.merge(btp, Merge, how='outer', indicator=True)

standalone_data = merged_df[merged_df['_merge'] != 'both']

standalone_pivot = standalone_data.pivot_table(index="Region Lvl 2",
                                               columns="Sub-Solution Area (L2)",
                                               values="ACV kEUR",
                                               aggfunc="sum")
#standalone_pivot.loc["CS APJ"] = standalone_pivot.sum(numeric_only=True, axis=0)

standalone_data_booked = standalone_data.query('(`DRM Category` == "Booked/Won")')
standalone_booked_pivot = standalone_data_booked.pivot_table(index="Region Lvl 2",
                                               columns="Sub-Solution Area (L2)",
                                               values="ACV kEUR",
                                               aggfunc="sum")
#standalone_booked_pivot.loc["CS APJ"] = standalone_booked_pivot.sum(numeric_only=True, axis=0)

standalone_data_adrm = standalone_data.query('(`DRM Category` in ["Committed","Probable"])')
standalone_adrm_pivot = standalone_data_adrm.pivot_table(index="Region Lvl 2",
                                               columns="Sub-Solution Area (L2)",
                                               values="ACV kEUR",
                                               aggfunc="sum")
#standalone_adrm_pivot.loc["CS APJ"] = standalone_adrm_pivot.sum(numeric_only=True, axis=0)

standalone_data_upside = standalone_data.query('(`DRM Category` == "Upside")')
standalone_upside_pivot = standalone_data_upside.pivot_table(index="Region Lvl 2",
                                               columns="Sub-Solution Area (L2)",
                                               values="ACV kEUR",
                                               aggfunc="sum")
#standalone_upside_pivot.loc["CS APJ"] = standalone_upside_pivot.sum(numeric_only=True, axis=0)



standalone_pivot_l3 = standalone_data.pivot_table(index="Region Lvl 2",
                                               columns="Solution Area L3",
                                               values="ACV kEUR", fill_value=0,
                                               aggfunc="sum")
standalone_pivot_l3.loc["CS APJ"] = standalone_pivot_l3.sum(numeric_only=True, axis=0)

standalone_data_short = standalone_data[["Account Name","Opportunity ID","Opp Description","Opp Owner Name","DRM Category","Opp Phase","ACV kEUR","TCV kEUR"]].sort_values("ACV kEUR", ascending=False)

top_standalone_data = standalone_data_short.query("`DRM Category` != 'Booked/Won'")
top_standalone_data = top_standalone_data.sort_values("ACV kEUR", ascending=False).head(25)

top_standalone_100K = top_standalone_data.query("`ACV kEUR` >= 100")
#st.write(top_standalone_100K,hide_index=True)


adai_nodsp = standalone_data.query('(`Sub-Solution Area (L2)` == "AppDev/Automation and Integration") & (`Solution Area L3` == "Cross BTP")')
standalone_data_nodatasphere = adai_nodsp[adai_nodsp["Opp Description"].astype('string').str.contains('datasphere', case=False)]#==False]

stt_pivot = standalone_data_nodatasphere.pivot_table(index="Region Lvl 2",
                                                     columns="DRM Category",
                                                     values="ACV kEUR",
                                                     aggfunc="sum")


standalone_data_nodatasphere_short = standalone_data_nodatasphere[["Account Name","Opp Description","Product Name (LPR)","DRM Category","ACV kEUR","TCV kEUR"]]
standalone_data_nodatasphere_won = standalone_data_nodatasphere.query("(`DRM Category`=='Booked/Won')")
standalone_data_nodatasphere_won_short = standalone_data_nodatasphere_won[["Account Name","Opp Description","Product Name (LPR)","ACV kEUR","TCV kEUR"]]




### Function to calculate the Total, Percentage by ACV and Percentage by Value
Merge_Pivot.loc["Total"]=Merge_Pivot.sum(numeric_only=True, axis=0)
Merge_Pivot = Merge_Pivot.assign(
    by_value = Merge_Pivot["ACV kEUR_BTP"]/Merge_Pivot["ACV kEUR_ERP"]*100,
    by_count = Merge_Pivot['Count_BTP']/Merge_Pivot["Count_ERP"]*100
)

### Function to calculate the Participation at Region Lvl 3
Merge_L3_Pivot = round(Merge.pivot_table(index="Region Lvl 3",
                                values=["ACV kEUR_ERP","Count_ERP","ACV kEUR_BTP","Count_BTP"],
                                fill_value=0, aggfunc="sum"))

Merge_L3_Pivot.loc["Total"]=Merge_L3_Pivot.sum(numeric_only=True, axis=0)

Merge_L3_Pivot = Merge_L3_Pivot.assign(
    by_value = Merge_L3_Pivot["ACV kEUR_BTP"]/Merge_L3_Pivot["ACV kEUR_ERP"]*100,
    by_count = Merge_L3_Pivot['Count_BTP']/Merge_L3_Pivot["Count_ERP"]*100
)

#######################################
# RISE/GROW - NO BTP 
#######################################

Merge_no_BTP = Merge.query('(`ACV kEUR_BTP` == 0)')

Merge_no_BTP = Merge_no_BTP[["Region Lvl 2","Region Lvl 3","Account Name","ACV kEUR_ERP","ACV kEUR_BTP"]]

#Merge_no_BTP = Merge_no_BTP.rename(columns={"Planning Entity ID_ERP":"Planning Entity ID"})
Merge_no_BTP = Merge_no_BTP.sort_values("ACV kEUR_ERP", ascending=False)



## For Top Deals
selected_data_top = selected_data[["Region Lvl 2","Account Name","Opportunity ID","Opp Description","Closing Qtr","DRM Category","Opp Phase","ACV kEUR"]]
selected_data_top["# of Opp"] = 1

selected_data_top_table = round(selected_data_top.groupby(["Region Lvl 2","Account Name","Opportunity ID","Opp Description","Opp Phase"])[["ACV kEUR"]].sum(),2).reset_index()

selected_data_top_table = selected_data_top_table.sort_values('ACV kEUR', ascending=False).style.format(precision=0, thousands=',') 


## Selected Data for Metric
selected_data_booked= selected_data.query('(`DRM Category` == "Booked/Won")')["ACV kEUR"].sum()
selected_data_adrm = selected_data.query('(`DRM Category` in ["Committed","Probable"])')["ACV kEUR"].sum()
selected_data_upside = selected_data.query('(`DRM Category` in ["Upside"])')["ACV kEUR"].sum()

## Deal Classification
selected_deal_classification = selected_data.copy()
selected_deal_classification = selected_deal_classification.groupby(["Opportunity ID","Account Name","Planning Entity ID","Closing Qtr","Region Lvl 2"])[["ACV kEUR"]].sum().reset_index()
selected_deal_classification["Deal Classification"] = selected_deal_classification["ACV kEUR"].apply(deal_classification)


selected_deal_classification_Pivot = selected_deal_classification.pivot_table(index="Deal Classification",
                                                                              columns="Region Lvl 2",
                                                                              values="ACV kEUR", fill_value=0,
                                                                              aggfunc='count')

selected_deal_classification_Pivot["Total"] =selected_deal_classification_Pivot.sum(axis=1)
selected_deal_classification_Pivot.loc["Total deals",:] =selected_deal_classification_Pivot.sum(axis=0)




def search():
    title = st.text_input('Customer Name: ',"Sample Customer Name")
    if title is None:
        st.write('No input is detected')
        st.stop()
    else:
        data_df_search = data_df.query("(`Solution Area (L1)` == @selected_lob)")
        selected_title = data_df_search[data_df_search["Account Name"].astype('string').str.contains(title,case=False)]
        #selected_title = data_df_btp[data_df_btp["Account Name"].astype('string').str.contains('|'.join([title]),case=False)]
        filtered_title = selected_title.groupby(["Account Name","Opportunity ID","Opp Description","Closing Qtr","Opp Phase","Opp Owner Name","Product Name (LPR)"])[["ACV kEUR"]].sum().sort_values('ACV kEUR', ascending=False)
        filtered_title_ACV = filtered_title["ACV kEUR"].sum()
 
        filtered_title_ACV = '{:,.02f}'.format(filtered_title_ACV)
        st.write('The current opportunities: ', filtered_title)#.style.format(precision=0, thousands=','))
        st.metric('Expected Total ACV: ', filtered_title_ACV)









#######################################
# DISPLAYING ALL THE COLUMNS
#######################################




status = "Based on Selected Data"
st.write(f":green[{status}]")
         
col1, col2, col3, col4 = st.columns(4)
col1.metric("Booked/Won", prettify(round(selected_data_booked,2)))
col2.metric("ADRM", prettify(round(selected_data_adrm,2)))
col3.metric("Upside", prettify(round(selected_data_upside,2)))
selected_data_total = selected_data_adrm + selected_data_upside
col4.metric("Total Pipeline (Excl. Booked)", prettify(round(selected_data_total,2)))
st.divider()

btp_rise = "BTP Participation in RISE"
st.write(f":blue[{btp_rise}]")
        
rise_data_booked = Merge.query('(`DRM Category` == "Booked/Won")')["ACV kEUR_BTP"].sum()
rise_data_ADRM = Merge.query('(`DRM Category` in ["Committed","Probable"])')["ACV kEUR_BTP"].sum()
rise_data_upside = Merge.query('(`DRM Category` == "Upside")')["ACV kEUR_BTP"].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Booked/Won", prettify(round(rise_data_booked,2)))
col2.metric("ADRM", prettify(round(rise_data_ADRM,2)))
col3.metric("Upside", prettify(round(rise_data_upside,2)))
rise_data_total = rise_data_ADRM + rise_data_upside
col4.metric("Total Pipeline (Excl. Booked)", prettify(round(rise_data_total,2)))
st.divider()

btp_rise = "Standalone BTP"
st.write(f":red[{btp_rise}]")

standalone_data_booked = standalone_data.query('(`DRM Category` == "Booked/Won")')["ACV kEUR"].sum()
standalone_data_ADRM = standalone_data.query('(`DRM Category` in ["Committed","Probable"])')["ACV kEUR"].sum()
standalone_data_upside = standalone_data.query('(`DRM Category` == "Upside")')["ACV kEUR"].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Booked/Won", prettify(round(standalone_data_booked,2)))
col2.metric("ADRM", prettify(round(standalone_data_ADRM,2)))
col3.metric("Upside", prettify(round(standalone_data_upside,2)))
standalone_data_total = standalone_data_ADRM + standalone_data_upside
col4.metric("Total Pipeline (Excl. Booked)", prettify(round(standalone_data_total,2)))
st.divider()


adai_nodsp_title = "CPEA/BTPEA based on Opp Description that includes Datasphere"
st.write(f":black[{adai_nodsp_title}]")

standalone_data_nodatasphere_booked = standalone_data_nodatasphere.query('(`DRM Category` == "Booked/Won")')["ACV kEUR"].sum()
standalone_data_nodatasphere_ADRM = standalone_data_nodatasphere.query('(`DRM Category` in ["Committed","Probable"])')["ACV kEUR"].sum()
standalone_data_nodatasphere_upside = standalone_data_nodatasphere.query('(`DRM Category` == "Upside")')["ACV kEUR"].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Booked/Won", prettify(round(standalone_data_nodatasphere_booked,2)))
col2.metric("ADRM", prettify(round(standalone_data_nodatasphere_ADRM,2)))
col3.metric("Upside", prettify(round(standalone_data_nodatasphere_upside,2)))
standalone_data_nodatasphere_total = standalone_data_nodatasphere_ADRM + standalone_data_nodatasphere_upside
col4.metric("Total Pipeline (Excl. Booked)", prettify(round(standalone_data_nodatasphere_total,2)))

with st.expander("CPEA that includes Datasphere keywords"):
    st.dataframe(stt_pivot.style.set_properties(**{"border": "1px solid black"})\
            .format(precision=0, thousands=',') \
            .highlight_max(color='lightgreen') \
            .highlight_min(color='pink'), use_container_width=True)
    st.subheader("List of the Won/Booked")
    st.dataframe(standalone_data_nodatasphere_won_short.style.set_properties(**{"border": "1px solid black"})\
            .format(precision=0, thousands=','), hide_index=True,use_container_width=True)
    st.subheader("List of All the Opportunities")
    st.dataframe(standalone_data_nodatasphere_short.style.set_properties(**{"border": "1px solid black"})\
            .format(precision=0, thousands=','), hide_index=True,use_container_width=True)
st.divider()


top_left_column, top_right_column = st.columns(2)

with top_left_column:
    top_adrm = selected_data.query("`DRM Category` in ['Probable','Committed']").sort_values("ACV kEUR", ascending=False)
    selected_data_top_table_adrm = top_adrm.head(10)
    fig = px.bar(selected_data_top_table_adrm, x="Account Name", y=["ACV kEUR"], text_auto='.2s',
            title="Top 10 Opportunities in ADRM")
    st.plotly_chart(fig, use_container_width=True)

with top_right_column:
    top_upside = selected_data.query("`DRM Category` in ['Upside']").sort_values("ACV kEUR", ascending=False)
    selected_data_top_table_upside = top_upside.head(10)
    fig = px.bar(selected_data_top_table_upside, x="Account Name", y=["ACV kEUR"], text_auto='.2s',
            title="Top 10 Opportunities in Upside")
    st.plotly_chart(fig, use_container_width=True)



## Container
container = st.container(border=True)
#with st.expander("Budget Data Preview"):
#     st.data_editor(budget_data, use_container_width=True, key="budget_expand")
with st.expander("Top Deals - Data Preview based on Selection"):
     st.data_editor(selected_data_top_table,hide_index=True, use_container_width=True)
st.container(border=True)






st.divider()

top_left_column, top_right_column = st.columns(2)

with top_left_column:
    st.subheader("Based on Region Lvl 2")
    st.write(selected_data_pivot, use_container_width=True)

with top_right_column:
    #st.write("Graphical Representation based on Region Lvl 2")
    selected_data_grp_bar = selected_data.groupby(["Region Lvl 2","DRM Category"])[["ACV kEUR"]].sum().reset_index()
    fig = px.bar(selected_data_grp_bar, y="ACV kEUR", x="Region Lvl 2", color="DRM Category")#, barmode="group")
    st.plotly_chart(fig)
    #st.bar_chart(selected_data_pivot, width=680)
    
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Summary","RISE Participation","Stand-alone Deals","BTP Top Deals","Deal Classification","Search ALL"])

with container:
    with tab1:
        with st.expander("Region Lvl 3"):
            if selected_l3 is not None:
                st.header("Based on Region Lvl 3")
                st.dataframe(selected_data_l3_pivot, use_container_width=True)
            st.subheader("Graphical Representation based on Region Lvl 3")
            selected_data_l3_grp_bar = selected_data.groupby(["Region Lvl 3","DRM Category"])[["ACV kEUR"]].sum().reset_index()
            selected_data_l3_grp_bar = selected_data_l3_grp_bar.sort_values('ACV kEUR', ascending=False)
            fig = px.bar(selected_data_l3_grp_bar, y="ACV kEUR", x="Region Lvl 3", color="DRM Category")#, barmode="group")
            fig.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
            st.divider()
        with st.expander("Product Name (LPR)"):
            st.subheader("Based on Product Name (LPR)")
            selected_data_l3_grp_bar = selected_data.groupby(["Product Name (LPR)","DRM Category"])[["ACV kEUR"]].sum().reset_index()
            selected_data_l3_grp_bar = selected_data_l3_grp_bar.sort_values('ACV kEUR', ascending=False).head(25)
            fig = px.bar(selected_data_l3_grp_bar, y="ACV kEUR", x="Product Name (LPR)", color="DRM Category", barmode="group")
            fig.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
            st.divider()
        with st.expander("Distribution Channel"):           
            st.subheader("Based on Distribution Channel ")
            st.dataframe(selected_data_dist_pivot, use_container_width=True)
            st.subheader("Graphical Representation based on Distribution Channel")
            st.bar_chart(selected_data_dist_pivot, width=680)
            st.divider()
        with st.expander("Based on Solution Area (L2)"):            
            st.subheader("Based on Solution Area (L2)")
            st.dataframe(selected_data_sol2_pivot, use_container_width=True)
            st.subheader("Graphical Representation based on Solution Area (L2)")
            st.bar_chart(selected_data_sol2_pivot)
    
    with tab2:
        with st.expander("Top 25 Cloud ERP deals without BTP"):
            st.subheader('This is the Top 25 Cloud ERP deals without BTP')
            st.dataframe(round(Merge_no_BTP).head(25), hide_index=True, use_container_width=True)
        st.subheader("BTP Inclusion in RISE (ACV kEUR) - Level 2")
        
        st.dataframe(Merge_Pivot.style.set_properties(**{"border": "1px solid black"})\
            .format(precision=0, thousands=',') \
            .format('{:.02f}%', subset=["by_value","by_count"])
            .highlight_max(color='lightgreen') \
            .highlight_min(color='pink'), use_container_width=True)
        st.divider()

        with st.expander("RISE and BTP - Booked"):
            st.dataframe(Merge_Booked_Pivot.style.set_properties(**{"border": "1px solid black"})\
                .format(precision=0, thousands=',') \
                .format('{:.02f}%', subset=["by_value","by_count"])
                .highlight_max(color='lightgreen') \
                .highlight_min(color='pink'), use_container_width=True)
        
        with st.expander("RISE and BTP - ADRM"):
            st.dataframe(Merge_ADRM_Pivot.style.set_properties(**{"border": "1px solid black"})\
                .format(precision=0, thousands=',') \
                .format('{:.02f}%', subset=["by_value","by_count"])
                .highlight_max(color='lightgreen') \
                .highlight_min(color='pink'), use_container_width=True)
       
        with st.expander("RISE and BTP - Upside"):
            st.dataframe(Merge_Upside_Pivot.style.set_properties(**{"border": "1px solid black"})\
                .format(precision=0, thousands=',') \
                .format('{:.02f}%', subset=["by_value","by_count"])
                .highlight_max(color='lightgreen') \
                .highlight_min(color='pink'), use_container_width=True)
        
        st.divider()
        
        with st.expander("BTP Inclusion in RISE (ACV kEUR) - Level 3"):
            st.subheader("BTP Inclusion in RISE (ACV kEUR) - Level 3")
            st.dataframe(Merge_L3_Pivot.style.set_properties(**{"border": "1px solid black"})\
                .format(precision=0, thousands=',') \
                .format('{:.02f}%', subset=["by_value","by_count"])
                .highlight_max(color='lightgreen') \
                .highlight_min(color='pink'),use_container_width=True)
    
    with tab3:
        st.subheader("Stand-alone BTP deals (taking out the RISE components)")
        st.dataframe(standalone_pivot.style.set_properties(**{"border": "1px solid black"})\
            .format(precision=0, thousands=',') \
            .highlight_max(color='lightgreen') \
            .highlight_min(color='pink'),use_container_width=True)
        
        with st.expander("Standalone Booked: "):
            st.dataframe(standalone_booked_pivot.style.set_properties(**{"border": "1px solid black"})\
            .format(precision=0, thousands=',') \
            .highlight_max(color='lightgreen') \
            .highlight_min(color='pink'),use_container_width=True)
        
        with st.expander("Standalone ADRM: "):
            st.dataframe(standalone_adrm_pivot.style.set_properties(**{"border": "1px solid black"})\
            .format(precision=0, thousands=',') \
            .highlight_max(color='lightgreen') \
            .highlight_min(color='pink'),use_container_width=True)
        
        with st.expander("Standalone Upside: "):
            st.dataframe(standalone_upside_pivot.style.set_properties(**{"border": "1px solid black"})\
            .format(precision=0, thousands=',') \
            .highlight_max(color='lightgreen') \
            .highlight_min(color='pink'),use_container_width=True)
        
        st.divider()

        with st.expander("Standalone Top 25 deals in Pipelines"):
            st.dataframe(top_standalone_data.style.format(precision=2), hide_index=True,use_container_width=True)

        with st.expander("Standalone BTP deals at Solution L3"):
            st.dataframe(standalone_pivot_l3.style.set_properties(**{"border": "1px solid black"})\
                .format(precision=0, thousands=',') \
                .highlight_max(color='lightgreen') \
                .highlight_min(color='pink'),use_container_width=True)
            st.divider()
            st.subheader("Stand-alone BTP deals (Details)")
            st.dataframe(standalone_data_short.style.format(precision=2), hide_index=True,use_container_width=True)

    with tab4:
        st.dataframe(selected_data_top_table, hide_index=True, use_container_width=True)
        st.subheader("Graphical Representation based on All deals")
        #st.scatter_chart(selected_data, x="Region Lvl 2", y="Opp Phase", color="DRM Category", size="ACV kEUR", height=400, width=800)
        st.scatter_chart(selected_data, y="Opp Phase", x="Closing Qtr", color="DRM Category", size="ACV kEUR")
        #st.bar_chart(selected_data_top, x="Closing Qtr", y="ACV kEUR", color="DRM Category")

    with tab5:
        st.header("Deal Classification")
        st.subheader("This is the classification based on count of opportunities")
        st.dataframe(selected_deal_classification_Pivot.style.set_properties(**{"border": "1px solid black"})\
            .format(precision=0, thousands=',') \
            .highlight_max(color='lightgreen') \
            .highlight_min(color='pink'),use_container_width=True)
        st.divider()
        st.subheader('This data is showing you all the deals at the Opp Phase (Count)')
        st.dataframe(selected_data_opp_phase_count_pivot, use_container_width=True)
        st.divider()
        st.subheader('This data is showing you all the deals at the Opp Phase (ACV)')
        st.dataframe(selected_data_opp_phase_pivot, use_container_width=True)
        st.divider()
        st.subheader('This data is showing you all the deals at the Solution Area L3 and L4')
        st.data_editor(round(selected_data_grp_preview).sort_values('ACV kEUR', ascending=False), key="data_expand", hide_index=True,use_container_width=True)

        
    with tab6:
        search()
        st.divider()
        #search_lpr()

    

