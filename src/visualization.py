"""
Visualization module for interactive dashboards and reports.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from pathlib import Path


def create_interactive_forecast(
    actual: pd.Series,
    predicted: pd.Series,
    title: str = "Sales Forecast"
) -> go.Figure:
    """
    Create interactive forecast visualization with Plotly.
    
    Args:
        actual: Actual time series
        predicted: Predicted time series
        title: Chart title
        
    Returns:
        Plotly figure
    """
    fig = go.Figure()
    
    # Add actual values
    fig.add_trace(go.Scatter(
        x=actual.index,
        y=actual.values,
        mode='lines',
        name='Actual',
        line=dict(color='steelblue', width=2)
    ))
    
    # Add predicted values
    fig.add_trace(go.Scatter(
        x=predicted.index,
        y=predicted.values,
        mode='lines',
        name='Predicted',
        line=dict(color='red', width=2, dash='dash')
    ))
    
    # Update layout
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Sales (£)',
        hovermode='x unified',
        template='plotly_white',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    
    return fig


def create_forecast_with_confidence(
    actual: pd.Series,
    predicted: pd.Series,
    lower_bound: pd.Series = None,
    upper_bound: pd.Series = None,
    title: str = "Sales Forecast with Confidence Interval"
) -> go.Figure:
    """
    Create forecast visualization with confidence intervals.
    
    Args:
        actual: Actual time series
        predicted: Predicted time series
        lower_bound: Lower confidence bound
        upper_bound: Upper confidence bound
        title: Chart title
        
    Returns:
        Plotly figure
    """
    fig = go.Figure()
    
    # Add confidence interval if provided
    if lower_bound is not None and upper_bound is not None:
        fig.add_trace(go.Scatter(
            x=pd.concat([upper_bound.index, upper_bound.index[::-1]]),
            y=pd.concat([upper_bound, lower_bound[::-1]]),
            fill='toself',
            fillcolor='rgba(255, 0, 0, 0.1)',
            line=dict(color='rgba(255, 0, 0, 0)'),
            name='95% Confidence',
            showlegend=True
        ))
    
    # Add actual values
    fig.add_trace(go.Scatter(
        x=actual.index,
        y=actual.values,
        mode='lines',
        name='Actual',
        line=dict(color='steelblue', width=2)
    ))
    
    # Add predicted values
    fig.add_trace(go.Scatter(
        x=predicted.index,
        y=predicted.values,
        mode='lines',
        name='Predicted',
        line=dict(color='red', width=2, dash='dash')
    ))
    
    # Update layout
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Sales (£)',
        hovermode='x unified',
        template='plotly_white',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    
    return fig


def create_seasonal_decomposition_plot(
    observed: pd.Series,
    trend: pd.Series,
    seasonal: pd.Series,
    residual: pd.Series
) -> go.Figure:
    """
    Create interactive time series decomposition plot.
    
    Args:
        observed: Observed values
        trend: Trend component
        seasonal: Seasonal component
        residual: Residual component
        
    Returns:
        Plotly figure with 4 subplots
    """
    fig = make_subplots(
        rows=4, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=('Observed', 'Trend', 'Seasonal', 'Residual')
    )
    
    # Observed
    fig.add_trace(go.Scatter(x=observed.index, y=observed.values, mode='lines', name='Observed'), row=1, col=1)
    
    # Trend
    fig.add_trace(go.Scatter(x=trend.index, y=trend.values, mode='lines', name='Trend'), row=2, col=1)
    
    # Seasonal
    fig.add_trace(go.Scatter(x=seasonal.index, y=seasonal.values, mode='lines', name='Seasonal'), row=3, col=1)
    
    # Residual
    fig.add_trace(go.Scatter(x=residual.index, y=residual.values, mode='lines', name='Residual'), row=4, col=1)
    
    # Update layout
    fig.update_layout(
        height=800,
        title_text="Time Series Decomposition",
        showlegend=False,
        template='plotly_white'
    )
    
    return fig


def create_monthly_sales_plot(df: pd.DataFrame, date_col: str = "Date", sales_col: str = "total_sales") -> go.Figure:
    """
    Create interactive monthly sales visualization.
    
    Args:
        df: DataFrame with date and sales columns
        date_col: Name of date column
        sales_col: Name of sales column
        
    Returns:
        Plotly figure
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df['Month'] = df[date_col].dt.to_period('M')
    
    monthly = df.groupby('Month')[sales_col].sum().reset_index()
    monthly['Month'] = monthly['Month'].astype(str)
    
    fig = px.bar(
        monthly,
        x='Month',
        y=sales_col,
        title='Monthly Sales',
        labels={sales_col: 'Total Sales (£)', 'Month': 'Month'},
        template='plotly_white'
    )
    
    fig.update_layout(xaxis_tickangle=-45)
    
    return fig


def create_country_sales_map(df: pd.DataFrame, country_col: str = "Country", sales_col: str = "Sales") -> go.Figure:
    """
    Create interactive choropleth map of sales by country.
    
    Args:
        df: DataFrame with country and sales columns
        country_col: Name of country column
        sales_col: Name of sales column
        
    Returns:
        Plotly figure
    """
    # Aggregate by country
    country_sales = df.groupby(country_col)[sales_col].sum().reset_index()
    
    # Create choropleth
    fig = px.choropleth(
        country_sales,
        locations=country_col,
        locationmode='country names',
        color=sales_col,
        title='Sales by Country',
        color_continuous_scale='Viridis',
        labels={sales_col: 'Total Sales (£)'},
        template='plotly_white'
    )
    
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='equirectangular'
        )
    )
    
    return fig


def create_forecast_dashboard(
    actual: pd.Series,
    predicted: pd.Series,
    metrics: dict,
    seasonal_pattern: pd.Series = None
) -> go.Figure:
    """
    Create comprehensive forecast dashboard.
    
    Args:
        actual: Actual time series
        predicted: Predicted time series
        metrics: Dictionary with MAPE, RMSE, MAE
        seasonal_pattern: Optional seasonal pattern data
        
    Returns:
        Plotly figure with multiple subplots
    """
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Sales Forecast',
            'Model Performance',
            'Weekly Pattern' if seasonal_pattern is not None else 'Residuals',
            'Forecast Summary'
        ),
        specs=[
            [{"type": "scatter"}, {"type": "indicator"}],
            [{"type": "bar"}, {"type": "table"}]
        ]
    )
    
    # Forecast plot
    fig.add_trace(go.Scatter(x=actual.index, y=actual.values, name='Actual', line=dict(color='steelblue')), row=1, col=1)
    fig.add_trace(go.Scatter(x=predicted.index, y=predicted.values, name='Predicted', line=dict(color='red', dash='dash')), row=1, col=1)
    
    # MAPE indicator
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=metrics.get('mape', 0),
        title={'text': "MAPE (%)"},
        delta={'reference': 15, 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
        gauge={'axis': {'range': [0, 50]}, 'bar': {'color': "steelblue"}}
    ), row=1, col=2)
    
    # Seasonal pattern or residuals
    if seasonal_pattern is not None:
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        fig.add_trace(go.Bar(x=days[:len(seasonal_pattern)], y=seasonal_pattern.values, name='Weekly Pattern'), row=2, col=1)
    else:
        residuals = actual - predicted
        fig.add_trace(go.Bar(x=residuals.index, y=residuals.values, name='Residuals'), row=2, col=1)
    
    # Summary table
    fig.add_trace(go.Table(
        header=dict(values=['Metric', 'Value'], fill_color='steelblue', font=dict(color='white', size=12)),
        cells=dict(values=[
            ['MAPE', 'RMSE', 'MAE'],
            [f"{metrics.get('mape', 0):.2f}%", f"£{metrics.get('rmse', 0):,.2f}", f"£{metrics.get('mae', 0):,.2f}"]
        ], fill_color='white', font=dict(size=11))
    ), row=2, col=2)
    
    # Update layout
    fig.update_layout(
        height=800,
        title_text="Sales Forecasting Dashboard",
        showlegend=True,
        template='plotly_white'
    )
    
    return fig


def save_interactive_plot(fig: go.Figure, filename: str, output_dir: str = "../reports/interactive") -> str:
    """
    Save interactive plot as HTML.
    
    Args:
        fig: Plotly figure
        filename: Output filename (without extension)
        output_dir: Output directory
        
    Returns:
        Path to saved file
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    filepath = output_path / f"{filename}.html"
    fig.write_html(str(filepath))
    
    return str(filepath)
