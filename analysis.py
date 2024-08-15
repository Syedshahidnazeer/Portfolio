import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats
from statsmodels.stats.power import TTestIndPower
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from lifelines import KaplanMeierFitter
from lifelines import CoxPHFitter
import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots

class AutomatedTestingFramework:
    def __init__(self, data):
        self.data = data

    def identify_column_types(self):
        """Identifies columns with string and integer data types."""
        string_columns = self.data.select_dtypes(include='object').columns.tolist()
        integer_columns = self.data.select_dtypes(include='integer').columns.tolist()
        return {
            'string_columns': string_columns,
            'integer_columns': integer_columns
        }

    def check_data_type(self, columns, allowed_types):
        """Checks if the data types of the specified columns are allowed."""
        invalid_columns = []
        for col in columns:
            if col not in self.data.columns:
                invalid_columns.append(f"Column '{col}' not found.")
            elif self.data[col].dtype not in allowed_types:
                invalid_columns.append(
                    f"Column '{col}' has invalid data type: {self.data[col].dtype}. Allowed types are: {allowed_types}"
                )
        return invalid_columns

    def describe_data(self):
        """Provide basic descriptive statistics of the data."""
        return self.data.describe()

    def check_normality(self, column):
        """Check if a column follows a normal distribution."""
        if column not in self.data.columns:
            return f"Error: Column '{column}' not found in the dataset."
        _, p_value = stats.normaltest(self.data[column])
        is_normal = p_value > 0.05
        return {'is_normal': is_normal, 'p_value': p_value}

    def t_test(self, group_column, value1, value2, metric_column):
        """Perform an independent t-test."""
        if group_column not in self.data.columns or metric_column not in self.data.columns:
            return f"Error: One or more columns not found in the dataset."
        group1 = self.data[self.data[group_column] == value1][metric_column]
        group2 = self.data[self.data[group_column] == value2][metric_column]
        t_stat, p_value = stats.ttest_ind(group1, group2)
        return {'t_statistic': t_stat, 'p_value': p_value, 'significant': p_value < 0.05}

    def anova(self, group_column, metric_column):
        """Perform one-way ANOVA."""
        if group_column not in self.data.columns or metric_column not in self.data.columns:
            return f"Error: One or more columns not found in the dataset."
        groups = [group[metric_column].values for name, group in self.data.groupby(group_column)]
        f_stat, p_value = stats.f_oneway(*groups)
        return {'f_statistic': f_stat, 'p_value': p_value, 'significant': p_value < 0.05}

    def correlation_analysis(self, column1, column2):
        """Perform correlation analysis between two columns."""
        if column1 not in self.data.columns or column2 not in self.data.columns:
            return f"Error: One or more columns not found in the dataset."
        corr, p_value = stats.pearsonr(self.data[column1], self.data[column2])
        return {'correlation': corr, 'p_value': p_value, 'significant': p_value < 0.05}

    def linear_regression(self, X_column, y_column):
        """Perform simple linear regression."""
        if X_column not in self.data.columns or y_column not in self.data.columns:
            return f"Error: One or more columns not found in the dataset."
        X = self.data[X_column].values.reshape(-1, 1)
        y = self.data[y_column].values
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        return {
            'coefficients': model.coef_,
            'intercept': model.intercept_,
            'r2_score': r2_score(y_test, y_pred),
            'mse': mean_squared_error(y_test, y_pred),
        }

    def visualize_distribution(self, column):
        """Visualize the distribution of a column using Plotly."""
        if column not in self.data.columns:
            return f"Error: Column '{column}' not found in the dataset."

        # Convert the column to numeric, handling errors
        try:
            numeric_data = pd.to_numeric(self.data[column], errors='coerce')
            # Remove any NaN values that might have been introduced during conversion
            numeric_data = numeric_data.dropna()

            if len(numeric_data) > 0:  # Check if there's any valid numeric data left
                fig = ff.create_distplot([numeric_data], [column], bin_size=0.2)
                fig.update_layout(title_text=f'Distribution of {column}')
                st.plotly_chart(fig)
            else:
                st.error(
                    f"Error: Column '{column}' does not contain any valid numeric data."
                )

        except ValueError:
            st.error(f"Error: Column '{column}' cannot be converted to numeric.")

    def visualize_boxplot(self, column, group_column):
        """Visualize boxplot of a column grouped by another column using Plotly."""
        if column not in self.data.columns or group_column not in self.data.columns:
            return f"Error: One or more columns not found in the dataset."

        fig = go.Figure()
        for group in self.data[group_column].unique():
            fig.add_trace(
                go.Box(
                    y=self.data[self.data[group_column] == group][column], name=str(group)
                )
            )

        fig.update_layout(title_text=f'Boxplot of {column} by {group_column}')
        st.plotly_chart(fig)

    def visualize_scatter(self, x_column, y_column):
        """Visualize scatter plot between two columns using Plotly."""
        if x_column not in self.data.columns or y_column not in self.data.columns:
            return f"Error: One or more columns not found in the dataset."

        fig = go.Figure(
            data=go.Scatter(x=self.data[x_column], y=self.data[y_column], mode='markers')
        )
        fig.update_layout(
            title=f'Scatter plot of {y_column} vs {x_column}',
            xaxis_title=x_column,
            yaxis_title=y_column,
        )
        st.plotly_chart(fig)

    def chi_squared_test(self, column1, column2):
        """Perform chi-squared test of independence."""
        if column1 not in self.data.columns or column2 not in self.data.columns:
            return f"Error: One or more columns not found in the dataset."
        contingency_table = pd.crosstab(self.data[column1], self.data[column2])
        chi2, p_value, _, _ = stats.chi2_contingency(contingency_table)
        return {'chi2_statistic': chi2, 'p_value': p_value, 'significant': p_value < 0.05}

    def kmeans_clustering(self, n_clusters, columns):
        """Perform K-means clustering."""
        if any(col not in self.data.columns for col in columns):
            return f"Error: One or more columns not found in the dataset."
        X = self.data[columns]
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        kmeans.fit(X)
        self.data['cluster'] = kmeans.labels_
        return self.data

    def pca(self, n_components, columns):
        """Perform Principal Component Analysis (PCA)."""
        if any(col not in self.data.columns for col in columns):
            return f"Error: One or more columns not found in the dataset."
        X = self.data[columns]
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        pca = PCA(n_components=n_components)
        principal_components = pca.fit_transform(X_scaled)
        return principal_components

    def kaplan_meier(self, time_column, event_column):
        """Perform Kaplan-Meier survival analysis."""
        if time_column not in self.data.columns or event_column not in self.data.columns:
            return f"Error: One or more columns not found in the dataset."
        kmf = KaplanMeierFitter()
        kmf.fit(self.data[time_column], event_observed=self.data[event_column])
        kmf.plot()
        st.pyplot()

    def cox_proportional_hazards(self, time_column, event_column, predictors):
        """Perform Cox Proportional Hazards analysis."""
        if any(col not in self.data.columns for col in [time_column, event_column] + predictors):
            return f"Error: One or more columns not found in the dataset."
        cph = CoxPHFitter()
        cph.fit(self.data[[time_column, event_column] + predictors], duration_col=time_column, event_col=event_column)
        cph.print_summary()


def data_analysis_page():
    # Streamlit app
    st.title("Automated Statistical Testing and Visualization")

    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        try:
            data = pd.read_csv(uploaded_file, encoding='latin-1', errors='replace')
        except TypeError:
            data = pd.read_csv(uploaded_file, encoding='latin-1')

        atf = AutomatedTestingFramework(data)
        # Display column names
        st.write("## Columns in the dataset:")
        st.write(data.columns.tolist())

        st.write("## Column Types")
        column_types = atf.identify_column_types()
        st.write("**String Columns:**", column_types['string_columns'])
        st.write("**Integer Columns:**", column_types['integer_columns'])

        # Descriptive Statistics
        if st.checkbox("Show Descriptive Statistics"):
            invalid_columns = atf.check_data_type(data.columns, [np.number])
            if invalid_columns:
                st.error("Error in Descriptive Statistics: " + ", ".join(invalid_columns))
            else:
                st.write(atf.describe_data())

        # Normality Test
        st.write("## Normality Test")
        selected_column_normality = st.selectbox("Select a column for normality test:", data.columns)
        if st.button("Run Normality Test"):
            invalid_columns = atf.check_data_type([selected_column_normality], [np.number])
            if invalid_columns:
                st.error("Error in Normality Test: " + ", ".join(invalid_columns))
            else:
                result = atf.check_normality(selected_column_normality)
                st.write(result)

        # T-Test
        st.write("## T-Test")
        selected_group_column = st.selectbox("Select group column for t-test:", data.columns)
        group_values = data[selected_group_column].unique()
        selected_value1 = st.selectbox("Select first group value:", group_values)
        selected_value2 = st.selectbox("Select second group value:", group_values)
        selected_metric_column = st.selectbox("Select metric column for t-test:", data.columns)
        if st.button("Run T-Test"):
            invalid_columns = atf.check_data_type([selected_metric_column], [np.number])
            if invalid_columns:
                st.error("Error in T-Test: " + ", ".join(invalid_columns))
            else:
                result = atf.t_test(selected_group_column, selected_value1, selected_value2, selected_metric_column)
                st.write(result)

        # ANOVA
        st.write("## ANOVA")
        selected_group_column_anova = st.selectbox("Select group column for ANOVA:", data.columns)
        selected_metric_column_anova = st.selectbox("Select metric column for ANOVA:", data.columns)
        if st.button("Run ANOVA"):
            invalid_columns = atf.check_data_type([selected_metric_column_anova], [np.number])
            if invalid_columns:
                st.error("Error in ANOVA: " + ", ".join(invalid_columns))
            else:
                result = atf.anova(selected_group_column_anova, selected_metric_column_anova)
                st.write(result)

        # Correlation Analysis
        st.write("## Correlation Analysis")
        selected_column1 = st.selectbox("Select first column for correlation analysis:", data.columns)
        selected_column2 = st.selectbox("Select second column for correlation analysis:", data.columns)
        if st.button("Run Correlation Analysis"):
            invalid_columns = atf.check_data_type([selected_column1, selected_column2], [np.number])
            if invalid_columns:
                st.error("Error in Correlation Analysis: " + ", ".join(invalid_columns))
            else:
                result = atf.correlation_analysis(selected_column1, selected_column2)
                st.write(result)

        # Linear Regression
        st.write("## Linear Regression")
        selected_x_column = st.selectbox("Select X column for linear regression:", data.columns)
        selected_y_column = st.selectbox("Select Y column for linear regression:", data.columns)
        if st.button("Run Linear Regression"):
            invalid_columns = atf.check_data_type([selected_x_column, selected_y_column], [np.number])
            if invalid_columns:
                st.error("Error in Linear Regression: " + ", ".join(invalid_columns))
            else:
                result = atf.linear_regression(selected_x_column, selected_y_column)
                st.write(result)

        # Visualizations
        st.write("## Visualizations")
        selected_column_viz = st.selectbox("Select column for visualization:", data.columns)
        if st.button("Show Distribution Plot"):
            atf.visualize_distribution(selected_column_viz)

        selected_column_boxplot = st.selectbox("Select column for boxplot:", data.columns)
        selected_group_column_boxplot = st.selectbox("Select group column for boxplot:", data.columns)
        if st.button("Show Boxplot"):
            atf.visualize_boxplot(selected_column_boxplot, selected_group_column_boxplot)

        selected_x_column_scatter = st.selectbox("Select X column for scatter plot:", data.columns)
        selected_y_column_scatter = st.selectbox("Select Y column for scatter plot:", data.columns)
        if st.button("Show Scatter Plot"):
            atf.visualize_scatter(selected_x_column_scatter, selected_y_column_scatter)

        # Chi-Squared Test
        st.write("## Chi-Squared Test")
        selected_column1_chi2 = st.selectbox("Select first column for chi-squared test:", data.columns)
        selected_column2_chi2 = st.selectbox("Select second column for chi-squared test:", data.columns)
        if st.button("Run Chi-Squared Test"):
            invalid_columns = atf.check_data_type([selected_column1_chi2, selected_column2_chi2], ['object', 'category'])
            if invalid_columns:
                st.error("Error in Chi-Squared Test: " + ", ".join(invalid_columns))
            else:
                result = atf.chi_squared_test(selected_column1_chi2, selected_column2_chi2)
                st.write(result)

        # K-Means Clustering
        st.write("## K-Means Clustering")
        selected_columns_kmeans = st.multiselect("Select columns for K-means clustering:", data.columns)
        n_clusters = st.number_input("Number of clusters:", min_value=2, value=3)
        if st.button("Run K-Means Clustering"):
            invalid_columns = atf.check_data_type(selected_columns_kmeans, [np.number])
            if invalid_columns:
                st.error("Error in K-Means Clustering: " + ", ".join(invalid_columns))
            else:
                result = atf.kmeans_clustering(n_clusters, selected_columns_kmeans)
                st.write(result)

        # PCA
        st.write("## Principal Component Analysis (PCA)")
        selected_columns_pca = st.multiselect("Select columns for PCA:", data.columns)
        n_components = st.number_input("Number of components:", min_value=1, value=2)
        if st.button("Run PCA"):
            invalid_columns = atf.check_data_type(selected_columns_pca, [np.number])
            if invalid_columns:
                st.error("Error in PCA: " + ", ".join(invalid_columns))
            else:
                result = atf.pca(n_components, selected_columns_pca)
                st.write(result)

        # Survival Analysis - Kaplan-Meier
        st.write("## Survival Analysis - Kaplan-Meier")
        selected_time_column = st.selectbox("Select time column:", data.columns)
        selected_event_column = st.selectbox("Select event column:", data.columns)
        if st.button("Run Kaplan-Meier"):
            invalid_columns = atf.check_data_type([selected_time_column], [np.number])
            if invalid_columns:
                st.error("Error in Kaplan-Meier: " + ", ".join(invalid_columns))
            else:
                atf.kaplan_meier(selected_time_column, selected_event_column)

        # Survival Analysis - Cox Proportional Hazards
        st.write("## Survival Analysis - Cox Proportional Hazards")
        selected_time_column_cph = st.selectbox("Select time column (CPH):", data.columns)
        selected_event_column_cph = st.selectbox("Select event column (CPH):", data.columns)
        selected_predictors_cph = st.multiselect("Select predictors (CPH):", data.columns)
        if st.button("Run Cox Proportional Hazards"):
            invalid_columns = atf.check_data_type([selected_time_column_cph] + selected_predictors_cph, [np.number])
            if invalid_columns:
                st.error("Error in Cox Proportional Hazards: " + ", ".join(invalid_columns))
            else:
                atf.cox_proportional_hazards(selected_time_column_cph, selected_event_column_cph, selected_predictors_cph)