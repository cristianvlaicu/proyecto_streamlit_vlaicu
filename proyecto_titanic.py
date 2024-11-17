import streamlit as st
import pandas as pd
import plotly.express as px
import copy

st.set_page_config(
    page_title="Titanic Passenger Data",
    page_icon="favicon.ico",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    body {

    background: #ffffff;
    background: linear-gradient(270deg,#ffffff 10%, rgba(255,255,0,0.25) 40%, rgba(255,0,0,0.25) 60%, rgba(0,0,0,0.25) 80%);
    background: -webkit-linear-gradient(270deg,#ffffff 10%, rgba(255,255,0,0.25) 40%, rgba(255,0,0,0.25) 60%, rgba(0,0,0,0.25) 80%);
    background: -moz-linear-gradient(270deg,#ffffff 10%, rgba(255,255,0,0.25) 40%, rgba(255,0,0,0.25) 60%, rgba(0,0,0,0.25) 80%);

    }

    [data-testid="stAppViewContainer"] {

    background: #ffffff;
    background: linear-gradient(270deg,#ffffff 10%, rgba(255,255,0,0.25) 40%, rgba(255,0,0,0.25) 60%, rgba(0,0,0,0.25) 80%);
    background: -webkit-linear-gradient(270deg,#ffffff 10%, rgba(255,255,0,0.25) 40%, rgba(255,0,0,0.25) 60%, rgba(0,0,0,0.25) 80%);
    background: -moz-linear-gradient(270deg,#ffffff 10%, rgba(255,255,0,0.25) 40%, rgba(255,0,0,0.25) 60%, rgba(0,0,0,0.25) 80%);

    }
    </style>
    """,
    unsafe_allow_html=True
)


if 'df' not in st.session_state:
    st.session_state['df'] = pd.DataFrame()

if 'df_fil' not in st.session_state:
    st.session_state['df_fil'] = pd.DataFrame()


def clean_data(df):

    survived_dict = {1: "Yes", 0: "No"}    
    pclass_dict = {1: "1st", 2: "2nd", 3: "3rd"}    
    embarkment_dict = {"C" : "Cherbourg", "Q" : "Queenstown", "S" : "Southampton"}

    df.replace({"Survived": survived_dict}, inplace=True)
    df.replace({"Pclass": pclass_dict}, inplace=True)
    df.replace({"Embarked": embarkment_dict}, inplace=True)

    df.dropna(subset=['Fare'], inplace=True)
    df.dropna(subset=['Age'], inplace=True)
    df.dropna(subset=['Embarked'], inplace=True)

    df['count'] = 1

    return df

@st.cache_data
def get_data(data_base):

    df = pd.read_csv(data_base)
    df = clean_data(df)

    return df

@st.cache_data
def get_values(col):

    return sorted(st.session_state['df'][col].dropna().unique())


def update_df():

    st.session_state['df_fil'] = st.session_state['df'][
        (st.session_state["df"]["Survived"].isin(st.session_state["Survived"])) &
        (st.session_state["df"]["Pclass"].isin(st.session_state["Pclass"])) &
        (st.session_state["df"]["Sex"].isin(st.session_state["Sex"])) &
        (st.session_state["df"]["Embarked"].isin(st.session_state["Embarked"])) & 
        ((st.session_state["df"]["Age"] >= st.session_state["Age"][0]) & (st.session_state["df"]["Age"] <= st.session_state["Age"][1])) &
        ((st.session_state["df"]["SibSp"] >= st.session_state["SibSp"][0]) & (st.session_state["df"]["SibSp"] <= st.session_state["SibSp"][1])) &
        ((st.session_state["df"]["Parch"] >= st.session_state["Parch"][0]) & (st.session_state["df"]["Parch"] <= st.session_state["Parch"][1])) &
        ((st.session_state["df"]["Fare"] >= st.session_state["Fare"][0]) & (st.session_state["df"]["Fare"] <= st.session_state["Fare"][1])) 
    ]


def generate_plot(var1, var2, var3, color_var, num_var, plot_type):

    if plot_type == "Bar":

        fig = px.bar(
            st.session_state['df_fil'],
            x = var1,
            y = num_var,
            color = color_var,
        )

    elif plot_type == "Pie":

        fig = px.pie(
            st.session_state['df_fil'],
            values = num_var,
            names = var1,
        )

    elif plot_type == "Scatter":

        fig = px.scatter(
            st.session_state['df_fil'],
            x = var1,
            y = var2,
            size = num_var,
            color=color_var,
        )

    elif plot_type == "Heatmap":

        fig = px.density_heatmap(
            st.session_state['df_fil'],
            x = var1,
            y = var2,
            z = num_var,
            text_auto=True,
        )

    elif plot_type == "Treemap":

        fig = px.treemap(
            st.session_state['df_fil'],
            path = [var1, var2, var3],
            values = num_var,
            color = color_var,
        )

    return fig

data_base = r"./titanic_data.csv"  
st.session_state['df'] = get_data(data_base)

def page_0():

    st.markdown(f"""
        <div style="text-align: center;">
            <h2 style="font-size:32px;">What will you find here?</h2>
            <p style="font-size: 22px";>
            In this page you can see a left side bar with tow aditional pages.<br>
            👉 In the first one you will find a data base and one Stats table with some interesting information.<br>
            &nbsp;&nbsp;&nbsp;👉 In the second page you will find some sliders to filter the data as you wish and with that you can <br> visualize some amazing plots with that filterated data.<br>
            Hope you enjoy the page and find inside useful and interesting information. Thank you very much! 🤗
            <p/>
        </div>""", 
        unsafe_allow_html=True
    )

    st.image("titanic_1200x630.png", use_column_width=True)



def page_1():

    st.subheader("🚢 Data description.")
    descr = st.markdown(open(r"./titanic_table_description.html").read(), unsafe_allow_html = True)

    with st.expander("Data Base:"):
        st.write(st.session_state['df'].shape)
        st.write(st.session_state['df'])

    with st.expander("Stats:"):
        st.write(st.session_state['df'].describe())

def page_2():

    if st.session_state['df_fil'].empty:
        st.session_state['df_fil'] = copy.copy(st.session_state['df'])

    st.subheader("📈 Data analytics.")

    col_plot_1, col_plot_2 = st.columns([5,1])

    with col_plot_1:

        fig_plot = st.empty()

    with col_plot_2:

        plot_type = st.selectbox(
            "Type of plot:",
            options = ['Bar', 'Pie', 'Scatter', 'Heatmap', 'Treemap']
            )

        var1, var2, var3, num_var, color_var = None, None, None, None, None

        var1 = st.selectbox(
            "1st variable:",
            options = st.session_state['df_fil'].columns,
            )

        num_var = st.selectbox(
            "Numeric variable:",
            options = ['count', 'Fare', 'Age', 'SibSp', 'Parch']
            )

        if plot_type in ['Bar', 'Scatter', 'Treemap']:
            color_var = st.selectbox(
                "Color variable:",
                options = st.session_state['df_fil'].columns,
                )

        if plot_type in ['Scatter', 'Heatmap', 'Treemap']:
            var2 = st.selectbox(
                "2nd variable:",
                options = st.session_state['df_fil'].columns,
                )

        if plot_type in ['Treemap']:
            var3 = st.selectbox(
                "3rd variable:",
                options = st.session_state['df_fil'].columns,
                )

    with st.expander("Filters"):

        with st.form(key = "filter_form"):

            col_fil_1, col_fil_2 = st.columns([1,1])

            with col_fil_1:
                surv_values = get_values("Survived")
                sel_surv = st.multiselect(
                    'Survived',
                    options = surv_values,
                    help = "Survival: 0 = No, 1 = Yes",
                    default = surv_values,
                    key = "Survived",
                    )

                pclass_values = get_values("Pclass")
                sel_pclass = st.multiselect(
                    'Pclass',
                    options = pclass_values,
                    help = "Class of the passenger (1,2,3)",
                    default = pclass_values,
                    key = "Pclass",
                    )

                sex_values = get_values("Sex") 
                sel_sex = st.multiselect(
                    'Sex',
                    options = sex_values,
                    help="Gender of passenger",
                    default = sex_values,
                    key = "Sex",
                    )

                embark_values = get_values("Embarked")
                sel_embark = st.multiselect(
                    'Embarked',
                    options = embark_values,
                    help="Embarked port",
                    default = embark_values,
                    key = "Embarked",
                    )

            with col_fil_2:

                age_values = get_values("Age")
                sel_age = st.slider(
                        'Age',
                        min_value = min(age_values),
                        max_value = max(age_values),
                        value = [min(age_values), max(age_values)],
                        help = "Age in years",
                        key = "Age",
                    )

                sibsp_values = get_values("SibSp")
                sel_sibsp = st.slider(
                        'SibSp',
                        min_value = min(sibsp_values),
                        max_value = max(sibsp_values),
                        value = [min(sibsp_values), max(sibsp_values)],
                        help = "n of siblings / spouses aboard the Titanic",
                        key = "SibSp",
                    )

                parch_values = get_values("Parch")
                sel_parch = st.slider(
                        'Parch',
                        min_value = min(parch_values),
                        max_value = max(parch_values),
                        value = [min(parch_values), max(parch_values)],
                        help = "n of parents / children aboard the Titanic",
                        key = "Parch",
                    )

                fare_values = get_values("Fare")
                sel_fare = st.slider(
                        'Fare',
                        min_value = min(fare_values),
                        max_value = max(fare_values),
                        value = [min(fare_values), max(fare_values)],
                        help = "Passenger fare",
                        key = "Fare",
                    )

                submit = st.form_submit_button("Update")

        if submit:
            update_df()

    fig = generate_plot(var1, var2, var3, color_var, num_var, plot_type)
    fig_plot.write(fig)



st.markdown(f"""
    <h1 style="text-align: center; font-size:44px;">Titanic Passenger Data.</h1>
""", unsafe_allow_html=True
    )

pg = st.navigation(
        {"":
            [
            st.Page(page_0, title="Home", icon="🏠"),
            st.Page(page_1, title="Data description", icon="🚢"),
            st.Page(page_2, title="Data analytics", icon="📈"),
            ],
        }
    )
pg.run()