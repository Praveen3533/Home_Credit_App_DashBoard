# pages/2_Target & Risk Segmentation.py
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.pre_processing import load_and_clean_data
from utils.filters import load_data, get_global_filters, apply_global_filters



# --- Load Data + Apply Global Filters ---
df = load_data()
filters, apply_filters, reset_filters = get_global_filters(df)

# Default: original data
working_df = df.copy()

if apply_filters:
    working_df = apply_global_filters(df, filters)

# --- Page Title ---
st.title("🎯 Page 2 — Target & Risk Segmentation")

# --- KPIs ---
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)
col7, col8, col9, col10 = st.columns(4)

col1.metric("Total Defaults", f"{working_df['TARGET'].sum():,}")
col2.metric("Default Rate (%)", f"{working_df['TARGET'].mean() * 100:.2f}")
col3.metric("Default Rate (Male %)", f"{working_df[working_df['CODE_GENDER']=='M']['TARGET'].mean()*100:.2f}")
col4.metric("Default Rate (Female %)", f"{working_df[working_df['CODE_GENDER']=='F']['TARGET'].mean()*100:.2f}")
col5.metric("Default Rate (Secondary Ed %)", f"{working_df[working_df['NAME_EDUCATION_TYPE']=='Secondary / secondary special']['TARGET'].mean()*100:.2f}")
col6.metric("Default Rate (Married %)", f"{working_df[working_df['NAME_FAMILY_STATUS']=='Married']['TARGET'].mean()*100:.2f}")
col7.metric("Avg Income — Defaulters", f"{working_df[working_df['TARGET']==1]['AMT_INCOME_TOTAL'].mean():,.0f}")
col8.metric("Avg Credit — Defaulters", f"{working_df[working_df['TARGET']==1]['AMT_CREDIT'].mean():,.0f}")
col9.metric("Avg Annuity — Defaulters", f"{working_df[working_df['TARGET']==1]['AMT_ANNUITY'].mean():,.0f}")
col10.metric("Avg Employment (Years) — Defaulters", f"{working_df[working_df['TARGET']==1]['EMPLOYMENT_YEARS'].mean():.1f}")

st.markdown("---")

# --- Graphs (10) organized into rows of 3 ---

# Row 1
row1_col1, row1_col2, row1_col3 = st.columns(3)

fig1 = px.histogram(working_df, x="TARGET", title="Default vs Repaid (Counts)", text_auto=True,  color="TARGET",  color_discrete_map={0: "#06e02e", 1: "#f60909"})
row1_col1.plotly_chart(fig1, use_container_width=True)

fig2 = px.bar(
    working_df.groupby("CODE_GENDER")["TARGET"].mean().reset_index(),
    x="CODE_GENDER", y="TARGET", title="Default Rate by Gender (%)",color="CODE_GENDER",  color_discrete_map={"M": "#0c48ee", "F": "#f705e3"}
)
fig2.update_yaxes(tickformat=".0%")
row1_col2.plotly_chart(fig2, use_container_width=True)

fig3 = px.bar(
    working_df.groupby("NAME_EDUCATION_TYPE")["TARGET"].mean().reset_index(),
    x="NAME_EDUCATION_TYPE", y="TARGET", title="Default Rate by Education (%)",  color="NAME_EDUCATION_TYPE",
    color_discrete_map={ "Secondary / secondary special": "#0b92ec",  
        "Higher education": "#0fe769",              
        "Incomplete higher": "#f29a0c",            
        "Lower secondary": "#e73623",               
        "Academic degree": "#ad31de"               
    })
fig3.update_yaxes(tickformat=".0%")
row1_col3.plotly_chart(fig3, use_container_width=True)

# Row 2
row2_col1, row2_col2, row2_col3 = st.columns(3)

fig4 = px.bar(
    working_df.groupby("NAME_FAMILY_STATUS")["TARGET"].mean().reset_index(),
    x="NAME_FAMILY_STATUS", y="TARGET", title="Default Rate by Family Status (%)",color="NAME_FAMILY_STATUS",
    color_discrete_map={"Single / not married": "#2e07f2",   
        "Married": "#07f64f",               
        "Civil marriage": "#f0091c",        
        "Separated": "#e8ef08",            
        "Widow": "#07f5f1"                  
    }
)
fig4.update_yaxes(tickformat=".0%")
row2_col1.plotly_chart(fig4, use_container_width=True)

fig5 = px.bar(
    working_df.groupby("NAME_HOUSING_TYPE")["TARGET"].mean().reset_index(),
    x="NAME_HOUSING_TYPE", y="TARGET", title="Default Rate by Housing Type (%)",color="NAME_HOUSING_TYPE",
    color_discrete_map={"Single / not married": "#0dc1d5",   
        "Married": "#a01199",               
        "Civil marriage": "#b41623",        
        "Separated": "#3fb753",            
        "Widow": "#442faf"                  
    }

)
fig5.update_yaxes(tickformat=".0%")
row2_col2.plotly_chart(fig5, use_container_width=True)

fig6 = px.box(working_df, x="TARGET", y="AMT_INCOME_TOTAL", title="Income by Target", color="TARGET",color_discrete_map={0: "#07f5f1", 1: "#fb6305"})
row2_col3.plotly_chart(fig6, use_container_width=True)

# Row 3
row3_col1, row3_col2, row3_col3 = st.columns(3)

fig7 = px.box(working_df, x="TARGET", y="AMT_CREDIT", title="Credit by Target", color="TARGET",color_discrete_map={0: "#f50707", 1: "#05f922"})
row3_col1.plotly_chart(fig7, use_container_width=True)

fig8 = px.violin(working_df, x="TARGET", y="AGE_YEARS", box=True, points="all", title="Age vs Target",color="TARGET", color_discrete_map={ 0:"#1abc9c",1: "#8e44ad"})
row3_col2.plotly_chart(fig8, use_container_width=True)

fig9 = px.histogram(working_df, x="EMPLOYMENT_YEARS", nbins=30,
                    title="Employment Years by Target",
                    color="TARGET",
                    color_discrete_map={0: "#0A5FF2", 1: "#F20707"})
row3_col3.plotly_chart(fig9, use_container_width=True)

# Row 4


row4_col1, row4_col2, row4_col3 = st.columns(3)

fig10 = px.histogram(working_df, x="NAME_CONTRACT_TYPE", text_auto=True,title="Contract Type vs Target", color="NAME_CONTRACT_TYPE",color_discrete_sequence=["#7BC6E9", "#F58A9A", "#57F157", "#EB6BEB", "#F9D60E"])
row4_col1.plotly_chart(fig10, use_container_width=True)

# ---------------------------
# Narrative
# ---------------------------
st.markdown("### Insights")
st.write("""
- **Gender**: One gender group shows a slightly higher default rate.  
- **Education**: Lower education groups tend to default more often.  
- **Housing Type**: Applicants living in rented/municipal apartments show higher default risk.  
- **Financial Factors**: Defaulters generally have lower income but higher credit relative to income.  
- Segments with **highest risk** (low income, rented housing, lower education) may warrant stricter credit checks.  
""")