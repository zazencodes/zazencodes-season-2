#!/usr/bin/env python3
"""
Japan Trade Statistics Analysis Notebook Generator

This script generates a comprehensive Jupyter notebook for analyzing Japan trade statistics data.
The generated notebook includes data exploration, trade balance analysis, top partners/commodities,
time series analysis, and visualizations.

Usage: python generate_trade_analysis_notebook.py <database_file> [output_notebook]
Example: python generate_trade_analysis_notebook.py input-data/ym_2020.db trade_analysis_2020.ipynb
"""

import argparse
import json
import sqlite3
from pathlib import Path
import sys


def create_notebook_cell(cell_type, source, metadata=None):
    """Create a Jupyter notebook cell."""
    cell = {
        "cell_type": cell_type,
        "metadata": metadata or {},
        "source": source if isinstance(source, list) else [source]
    }
    
    if cell_type == "code":
        cell["execution_count"] = None
        cell["outputs"] = []
    
    return cell


def generate_notebook_content(db_path):
    """Generate the content for the Jupyter notebook."""
    db_name = Path(db_path).stem
    year = db_name.split('_')[-1] if '_' in db_name else "unknown"
    
    # Get basic info about the database
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {db_name}")
        total_rows = cursor.fetchone()[0]
        
        cursor.execute(f"SELECT MIN(Year || '-' || CASE WHEN LENGTH(month) = 1 THEN '0' || month ELSE month END), MAX(Year || '-' || CASE WHEN LENGTH(month) = 1 THEN '0' || month ELSE month END) FROM {db_name}")
        min_ym, max_ym = cursor.fetchone()
        
        cursor.execute(f"SELECT COUNT(DISTINCT Country) FROM {db_name}")
        num_countries = cursor.fetchone()[0]
        
        cursor.execute(f"SELECT COUNT(DISTINCT hs2) FROM {db_name}")
        num_hs2 = cursor.fetchone()[0]
        
        conn.close()
    except:
        total_rows = "unknown"
        min_ym, max_ym = "unknown", "unknown"
        num_countries = "unknown"
        num_hs2 = "unknown"

    cells = []
    
    # Title and Introduction
    cells.append(create_notebook_cell("markdown", [
        f"# Japan Trade Statistics Analysis - {year}\n",
        "\n",
        "This notebook provides a comprehensive analysis of Japan's trade statistics data.\n",
        "\n",
        f"**Data Overview:**\n",
        f"- Database: `{db_path}`\n",
        f"- Total Records: {total_rows:,}\n" if isinstance(total_rows, int) else f"- Total Records: {total_rows}\n",
        f"- Time Period: {min_ym} to {max_ym}\n",
        f"- Countries: {num_countries}\n",
        f"- HS2 Categories: {num_hs2}\n",
        "\n",
        "**Key Questions to Explore:**\n",
        "1. What is Japan's trade balance (exports vs imports)?\n",
        "2. Who are Japan's top trading partners?\n",
        "3. What are the most traded commodities?\n",
        "4. How do trade patterns change over time?\n",
        "5. What are the geographic patterns in trade?\n"
    ]))
    
    # Imports and Setup
    cells.append(create_notebook_cell("code", [
        "# Import required libraries\n",
        "import sqlite3\n",
        "import pandas as pd\n",
        "import numpy as np\n",
        "import matplotlib.pyplot as plt\n",
        "import seaborn as sns\n",
        "from pathlib import Path\n",
        "import warnings\n",
        "\n",
        "# Configure plotting\n",
        "plt.style.use('seaborn-v0_8')\n",
        "plt.rcParams['figure.figsize'] = (12, 8)\n",
        "sns.set_palette('husl')\n",
        "warnings.filterwarnings('ignore')\n",
        "\n",
        "# Display all columns in pandas\n",
        "pd.set_option('display.max_columns', None)\n",
        "pd.set_option('display.width', None)\n",
        "pd.set_option('display.max_colwidth', None)"
    ]))
    
    # Data Loading
    cells.append(create_notebook_cell("markdown", [
        "## 1. Data Loading and Basic Exploration"
    ]))
    
    cells.append(create_notebook_cell("code", [
        f"# Load data from SQLite database\n",
        f"db_path = '{db_path}'\n",
        f"table_name = '{db_name}'\n",
        "\n",
        "# Connect and load data\n",
        "conn = sqlite3.connect(db_path)\n",
        "df = pd.read_sql_query(f'SELECT * FROM {table_name}', conn)\n",
        "conn.close()\n",
        "\n",
        "print(f'Data shape: {df.shape}')\n",
        "print(f'Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB')\n",
        "df.head()"
    ]))
    
    # Data Info and Overview
    cells.append(create_notebook_cell("code", [
        "# Basic data information\n",
        "print('Data types and null values:')\n",
        "print(df.info())\n",
        "print('\\nBasic statistics:')\n",
        "df.describe()"
    ]))
    
    # Data Quality Check
    cells.append(create_notebook_cell("code", [
        "# Data quality checks\n",
        "print('Missing values by column:')\n",
        "print(df.isnull().sum())\n",
        "\n",
        "print('\\nUnique values in key categorical columns:')\n",
        "for col in ['exp_imp', 'Year', 'month']:\n",
        "    print(f'{col}: {sorted(df[col].unique())}')\n",
        "\n",
        "print(f'\\nYear-Month range: {df.Year.min()}-{df.month.min().zfill(2)} to {df.Year.max()}-{df.month.max().zfill(2)}')\n",
        "print(f'Number of countries: {df.Country.nunique()}')\n",
        "print(f'Number of HS2 categories: {df.hs2.nunique()}')"
    ]))
    
    # Create Trade Type Labels
    cells.append(create_notebook_cell("code", [
        "# Create more readable labels\n",
        "df['trade_type'] = df['exp_imp'].map({1: 'Export', 2: 'Import'})\n",
        "df['year_month'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['month'].astype(str).str.zfill(2), format='%Y-%m')\n",
        "\n",
        "# Convert Value to billions of yen for easier reading\n",
        "df['value_billion_yen'] = df['Value'] / 1e9\n",
        "\n",
        "print('Trade type distribution:')\n",
        "print(df['trade_type'].value_counts())\n",
        "print('\\nSample of processed data:')\n",
        "df[['trade_type', 'year_month', 'Country', 'hs2', 'value_billion_yen', 'Q1', 'Q2']].head()"
    ]))
    
    # Trade Balance Analysis
    cells.append(create_notebook_cell("markdown", [
        "## 2. Trade Balance Analysis"
    ]))
    
    cells.append(create_notebook_cell("code", [
        "# Overall trade balance\n",
        "trade_summary = df.groupby('trade_type')['Value'].agg(['sum', 'count', 'mean']).round(2)\n",
        "trade_summary['sum_billion_yen'] = trade_summary['sum'] / 1e9\n",
        "\n",
        "print('Overall Trade Summary:')\n",
        "print(trade_summary)\n",
        "\n",
        "exports = trade_summary.loc['Export', 'sum']\n",
        "imports = trade_summary.loc['Import', 'sum']\n",
        "balance = exports - imports\n",
        "\n",
        "print(f'\\nTrade Balance:')\n",
        "print(f'Total Exports: ¥{exports/1e12:.2f} trillion')\n",
        "print(f'Total Imports: ¥{imports/1e12:.2f} trillion')\n",
        "print(f'Trade Balance: ¥{balance/1e12:.2f} trillion ({'Surplus' if balance > 0 else 'Deficit'})')"
    ]))
    
    # Monthly Trade Balance
    cells.append(create_notebook_cell("code", [
        "# Monthly trade balance\n",
        "monthly_trade = df.groupby(['year_month', 'trade_type'])['Value'].sum().unstack()\n",
        "monthly_trade['Balance'] = monthly_trade['Export'] - monthly_trade['Import']\n",
        "monthly_trade = monthly_trade / 1e12  # Convert to trillions\n",
        "\n",
        "# Plot monthly trade\n",
        "fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))\n",
        "\n",
        "# Trade volumes\n",
        "monthly_trade[['Export', 'Import']].plot(kind='line', ax=ax1, marker='o')\n",
        "ax1.set_title('Monthly Trade Volumes')\n",
        "ax1.set_ylabel('Value (Trillion Yen)')\n",
        "ax1.legend()\n",
        "ax1.grid(True, alpha=0.3)\n",
        "\n",
        "# Trade balance\n",
        "monthly_trade['Balance'].plot(kind='line', ax=ax2, marker='o', color='green')\n",
        "ax2.axhline(y=0, color='red', linestyle='--', alpha=0.7)\n",
        "ax2.set_title('Monthly Trade Balance')\n",
        "ax2.set_ylabel('Balance (Trillion Yen)')\n",
        "ax2.grid(True, alpha=0.3)\n",
        "\n",
        "plt.tight_layout()\n",
        "plt.show()\n",
        "\n",
        "print('Monthly Trade Data:')\n",
        "print(monthly_trade.round(3))"
    ]))
    
    # Top Trading Partners
    cells.append(create_notebook_cell("markdown", [
        "## 3. Top Trading Partners Analysis"
    ]))
    
    cells.append(create_notebook_cell("code", [
        "# Top trading partners by total trade value\n",
        "partner_trade = df.groupby(['Country', 'trade_type'])['Value'].sum().unstack(fill_value=0)\n",
        "partner_trade['Total'] = partner_trade['Export'] + partner_trade['Import']\n",
        "partner_trade['Balance'] = partner_trade['Export'] - partner_trade['Import']\n",
        "partner_trade = partner_trade.sort_values('Total', ascending=False)\n",
        "\n",
        "# Convert to billions for display\n",
        "partner_display = partner_trade.copy()\n",
        "for col in ['Export', 'Import', 'Total', 'Balance']:\n",
        "    partner_display[col] = partner_display[col] / 1e9\n",
        "\n",
        "print('Top 15 Trading Partners (Billions of Yen):')\n",
        "print(partner_display.head(15).round(2))"
    ]))
    
    cells.append(create_notebook_cell("code", [
        "# Visualize top trading partners\n",
        "top_partners = partner_display.head(10)\n",
        "\n",
        "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))\n",
        "\n",
        "# Trade volumes\n",
        "top_partners[['Export', 'Import']].plot(kind='barh', ax=ax1)\n",
        "ax1.set_title('Top 10 Trading Partners - Export vs Import')\n",
        "ax1.set_xlabel('Value (Billion Yen)')\n",
        "ax1.legend()\n",
        "\n",
        "# Trade balance\n",
        "colors = ['green' if x > 0 else 'red' for x in top_partners['Balance']]\n",
        "top_partners['Balance'].plot(kind='barh', ax=ax2, color=colors)\n",
        "ax2.axvline(x=0, color='black', linestyle='-', alpha=0.7)\n",
        "ax2.set_title('Top 10 Trading Partners - Trade Balance')\n",
        "ax2.set_xlabel('Balance (Billion Yen)')\n",
        "\n",
        "plt.tight_layout()\n",
        "plt.show()"
    ]))
    
    # Commodity Analysis
    cells.append(create_notebook_cell("markdown", [
        "## 4. Commodity Analysis (HS Codes)"
    ]))
    
    cells.append(create_notebook_cell("code", [
        "# HS2 level analysis (major categories)\n",
        "hs2_trade = df.groupby(['hs2', 'trade_type'])['Value'].sum().unstack(fill_value=0)\n",
        "hs2_trade['Total'] = hs2_trade['Export'] + hs2_trade['Import']\n",
        "hs2_trade['Balance'] = hs2_trade['Export'] - hs2_trade['Import']\n",
        "hs2_trade = hs2_trade.sort_values('Total', ascending=False)\n",
        "\n",
        "# Convert to billions\n",
        "hs2_display = hs2_trade.copy()\n",
        "for col in ['Export', 'Import', 'Total', 'Balance']:\n",
        "    hs2_display[col] = hs2_display[col] / 1e9\n",
        "\n",
        "print('Top 15 HS2 Categories by Total Trade (Billions of Yen):')\n",
        "print(hs2_display.head(15).round(2))"
    ]))
    
    cells.append(create_notebook_cell("code", [
        "# Visualize top HS2 categories\n",
        "top_hs2 = hs2_display.head(12)\n",
        "\n",
        "fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(18, 12))\n",
        "\n",
        "# Export pie chart\n",
        "top_hs2['Export'].plot(kind='pie', ax=ax1, autopct='%1.1f%%')\n",
        "ax1.set_title('Top HS2 Categories - Exports')\n",
        "ax1.set_ylabel('')\n",
        "\n",
        "# Import pie chart\n",
        "top_hs2['Import'].plot(kind='pie', ax=ax2, autopct='%1.1f%%')\n",
        "ax2.set_title('Top HS2 Categories - Imports')\n",
        "ax2.set_ylabel('')\n",
        "\n",
        "# Trade balance bar chart\n",
        "colors = ['green' if x > 0 else 'red' for x in top_hs2['Balance']]\n",
        "top_hs2['Balance'].plot(kind='bar', ax=ax3, color=colors)\n",
        "ax3.axhline(y=0, color='black', linestyle='-', alpha=0.7)\n",
        "ax3.set_title('Top HS2 Categories - Trade Balance')\n",
        "ax3.set_ylabel('Balance (Billion Yen)')\n",
        "ax3.tick_params(axis='x', rotation=45)\n",
        "\n",
        "# Total trade bar chart\n",
        "top_hs2['Total'].plot(kind='bar', ax=ax4)\n",
        "ax4.set_title('Top HS2 Categories - Total Trade')\n",
        "ax4.set_ylabel('Total (Billion Yen)')\n",
        "ax4.tick_params(axis='x', rotation=45)\n",
        "\n",
        "plt.tight_layout()\n",
        "plt.show()"
    ]))
    
    # Time Series Analysis
    cells.append(create_notebook_cell("markdown", [
        "## 5. Time Series Analysis"
    ]))
    
    cells.append(create_notebook_cell("code", [
        "# Monthly trends by trade type\n",
        "monthly_trends = df.groupby(['year_month', 'trade_type'])['Value'].agg(['sum', 'count', 'mean'])\n",
        "monthly_trends.columns = ['Total_Value', 'Count', 'Avg_Value']\n",
        "monthly_trends = monthly_trends.reset_index()\n",
        "\n",
        "# Pivot for easier plotting\n",
        "monthly_pivot = monthly_trends.pivot(index='year_month', columns='trade_type', values='Total_Value')\n",
        "monthly_pivot = monthly_pivot / 1e12  # Convert to trillions\n",
        "\n",
        "print('Monthly Trade Trends (Trillion Yen):')\n",
        "print(monthly_pivot.round(3))"
    ]))
    
    cells.append(create_notebook_cell("code", [
        "# Advanced time series visualization\n",
        "fig, axes = plt.subplots(2, 2, figsize=(16, 12))\n",
        "\n",
        "# Monthly volume trends\n",
        "monthly_pivot.plot(ax=axes[0,0], marker='o')\n",
        "axes[0,0].set_title('Monthly Trade Volume Trends')\n",
        "axes[0,0].set_ylabel('Value (Trillion Yen)')\n",
        "axes[0,0].legend()\n",
        "axes[0,0].grid(True, alpha=0.3)\n",
        "\n",
        "# Growth rates (if multiple months available)\n",
        "if len(monthly_pivot) > 1:\n",
        "    growth_rates = monthly_pivot.pct_change() * 100\n",
        "    growth_rates.plot(ax=axes[0,1], marker='o')\n",
        "    axes[0,1].set_title('Month-over-Month Growth Rates')\n",
        "    axes[0,1].set_ylabel('Growth Rate (%)')\n",
        "    axes[0,1].axhline(y=0, color='black', linestyle='--', alpha=0.7)\n",
        "    axes[0,1].legend()\n",
        "    axes[0,1].grid(True, alpha=0.3)\n",
        "else:\n",
        "    axes[0,1].text(0.5, 0.5, 'Insufficient data for growth rates', \n",
        "                   ha='center', va='center', transform=axes[0,1].transAxes)\n",
        "    axes[0,1].set_title('Growth Rates (Insufficient Data)')\n",
        "\n",
        "# Trade balance over time\n",
        "balance_series = monthly_pivot['Export'] - monthly_pivot['Import']\n",
        "balance_series.plot(ax=axes[1,0], marker='o', color='green')\n",
        "axes[1,0].axhline(y=0, color='red', linestyle='--', alpha=0.7)\n",
        "axes[1,0].set_title('Trade Balance Over Time')\n",
        "axes[1,0].set_ylabel('Balance (Trillion Yen)')\n",
        "axes[1,0].grid(True, alpha=0.3)\n",
        "\n",
        "# Number of transactions over time\n",
        "monthly_count = monthly_trends.pivot(index='year_month', columns='trade_type', values='Count')\n",
        "monthly_count.plot(ax=axes[1,1], marker='o')\n",
        "axes[1,1].set_title('Number of Trade Transactions Over Time')\n",
        "axes[1,1].set_ylabel('Number of Records')\n",
        "axes[1,1].legend()\n",
        "axes[1,1].grid(True, alpha=0.3)\n",
        "\n",
        "plt.tight_layout()\n",
        "plt.show()"
    ]))
    
    # Geographic Analysis
    cells.append(create_notebook_cell("markdown", [
        "## 6. Geographic Patterns"
    ]))
    
    cells.append(create_notebook_cell("code", [
        "# Country concentration analysis\n",
        "country_stats = df.groupby('Country')['Value'].agg(['sum', 'count', 'mean']).sort_values('sum', ascending=False)\n",
        "country_stats['cum_sum'] = country_stats['sum'].cumsum()\n",
        "country_stats['cum_pct'] = country_stats['cum_sum'] / country_stats['sum'].sum() * 100\n",
        "\n",
        "print('Trade Concentration Analysis:')\n",
        "print(f'Top 5 countries account for {country_stats.iloc[4][\"cum_pct\"]:.1f}% of total trade')\n",
        "print(f'Top 10 countries account for {country_stats.iloc[9][\"cum_pct\"]:.1f}% of total trade')\n",
        "print(f'Top 20 countries account for {country_stats.iloc[19][\"cum_pct\"]:.1f}% of total trade')\n",
        "\n",
        "# Plot concentration curve\n",
        "plt.figure(figsize=(12, 6))\n",
        "plt.plot(range(1, len(country_stats)+1), country_stats['cum_pct'], marker='o')\n",
        "plt.axhline(y=80, color='red', linestyle='--', alpha=0.7, label='80% threshold')\n",
        "plt.axhline(y=90, color='orange', linestyle='--', alpha=0.7, label='90% threshold')\n",
        "plt.xlabel('Number of Countries (ranked by trade value)')\n",
        "plt.ylabel('Cumulative Percentage of Total Trade')\n",
        "plt.title('Trade Concentration: Cumulative Distribution by Country')\n",
        "plt.legend()\n",
        "plt.grid(True, alpha=0.3)\n",
        "plt.show()"
    ]))
    
    # Detailed Analysis Functions
    cells.append(create_notebook_cell("markdown", [
        "## 7. Advanced Analysis Functions"
    ]))
    
    cells.append(create_notebook_cell("code", [
        "def analyze_country_detail(country_code, top_n=10):\n",
        "    \"\"\"Analyze trade details for a specific country.\"\"\"\n",
        "    country_data = df[df['Country'] == country_code]\n",
        "    \n",
        "    if len(country_data) == 0:\n",
        "        print(f'No data found for country code {country_code}')\n",
        "        return\n",
        "    \n",
        "    print(f'\\nDetailed Analysis for Country {country_code}:')\n",
        "    print(f'Total records: {len(country_data):,}')\n",
        "    \n",
        "    # Trade summary\n",
        "    trade_summary = country_data.groupby('trade_type')['Value'].agg(['sum', 'count'])\n",
        "    print('\\nTrade Summary:')\n",
        "    print(trade_summary)\n",
        "    \n",
        "    # Top commodities\n",
        "    top_commodities = country_data.groupby(['hs2', 'trade_type'])['Value'].sum().unstack(fill_value=0)\n",
        "    top_commodities['Total'] = top_commodities.sum(axis=1)\n",
        "    top_commodities = top_commodities.sort_values('Total', ascending=False).head(top_n)\n",
        "    \n",
        "    print(f'\\nTop {top_n} HS2 Categories:')\n",
        "    print((top_commodities / 1e9).round(2))  # In billions\n",
        "    \n",
        "    return country_data\n",
        "\n",
        "def analyze_commodity_detail(hs2_code, top_n=10):\n",
        "    \"\"\"Analyze trade details for a specific HS2 commodity category.\"\"\"\n",
        "    commodity_data = df[df['hs2'] == hs2_code]\n",
        "    \n",
        "    if len(commodity_data) == 0:\n",
        "        print(f'No data found for HS2 code {hs2_code}')\n",
        "        return\n",
        "    \n",
        "    print(f'\\nDetailed Analysis for HS2 Category {hs2_code}:')\n",
        "    print(f'Total records: {len(commodity_data):,}')\n",
        "    \n",
        "    # Trade summary\n",
        "    trade_summary = commodity_data.groupby('trade_type')['Value'].agg(['sum', 'count'])\n",
        "    print('\\nTrade Summary:')\n",
        "    print(trade_summary)\n",
        "    \n",
        "    # Top countries\n",
        "    top_countries = commodity_data.groupby(['Country', 'trade_type'])['Value'].sum().unstack(fill_value=0)\n",
        "    top_countries['Total'] = top_countries.sum(axis=1)\n",
        "    top_countries = top_countries.sort_values('Total', ascending=False).head(top_n)\n",
        "    \n",
        "    print(f'\\nTop {top_n} Countries:')\n",
        "    print((top_countries / 1e9).round(2))  # In billions\n",
        "    \n",
        "    return commodity_data\n",
        "\n",
        "# Example usage:\n",
        "print('Analysis functions defined. Example usage:')\n",
        "print('analyze_country_detail(213)  # Analyze specific country')\n",
        "print('analyze_commodity_detail(\"84\")  # Analyze specific HS2 category')"
    ]))
    
    # Summary and Insights
    cells.append(create_notebook_cell("markdown", [
        "## 8. Key Insights and Summary"
    ]))
    
    cells.append(create_notebook_cell("code", [
        "# Generate key insights\n",
        "total_trade = df['Value'].sum()\n",
        "export_share = df[df['trade_type'] == 'Export']['Value'].sum() / total_trade * 100\n",
        "import_share = df[df['trade_type'] == 'Import']['Value'].sum() / total_trade * 100\n",
        "\n",
        "top_partner = partner_display.index[0]\n",
        "top_partner_share = partner_display.iloc[0]['Total'] / (total_trade / 1e9) * 100\n",
        "\n",
        "top_commodity = hs2_display.index[0]\n",
        "top_commodity_share = hs2_display.iloc[0]['Total'] / (total_trade / 1e9) * 100\n",
        "\n",
        "print('KEY INSIGHTS:')\n",
        "print('=' * 50)\n",
        "print(f'📊 Total Trade Value: ¥{total_trade/1e12:.2f} trillion')\n",
        "print(f'📈 Export Share: {export_share:.1f}%')\n",
        "print(f'📉 Import Share: {import_share:.1f}%')\n",
        "print(f'🤝 Top Trading Partner: Country {top_partner} ({top_partner_share:.1f}% of total trade)')\n",
        "print(f'📦 Top Commodity Category: HS2-{top_commodity} ({top_commodity_share:.1f}% of total trade)')\n",
        "print(f'🌍 Number of Trading Partners: {df.Country.nunique()}')\n",
        "print(f'📅 Time Period Covered: {df.Year.min()}-{df.month.min().zfill(2)} to {df.Year.max()}-{df.month.max().zfill(2)}')\n",
        "\n",
        "# Trade balance assessment\n",
        "if export_share > import_share:\n",
        "    print(f'💰 Trade Status: SURPLUS (Exports exceed imports by {export_share - import_share:.1f}%)')\n",
        "else:\n",
        "    print(f'⚠️ Trade Status: DEFICIT (Imports exceed exports by {import_share - export_share:.1f}%)')\n",
        "\n",
        "print('\\n🔍 For detailed analysis of specific countries or commodities, use:')\n",
        "print('   analyze_country_detail(country_code)')\n",
        "print('   analyze_commodity_detail(hs2_code)')"
    ]))
    
    # Next Steps
    cells.append(create_notebook_cell("markdown", [
        "## 9. Next Steps and Further Analysis\n",
        "\n",
        "This notebook provides a comprehensive overview of the trade data. Here are some suggestions for deeper analysis:\n",
        "\n",
        "### 🔬 Advanced Analytics\n",
        "1. **Seasonal Analysis**: Compare trade patterns across different months\n",
        "2. **Product Complexity**: Analyze trade in high-tech vs. raw materials\n",
        "3. **Trade Intensity**: Calculate trade intensity ratios with major partners\n",
        "4. **Market Concentration**: Use Herfindahl-Hirschman Index for market concentration\n",
        "\n",
        "### 📈 Statistical Analysis\n",
        "1. **Correlation Analysis**: Find relationships between different trade variables\n",
        "2. **Outlier Detection**: Identify unusual trade transactions\n",
        "3. **Trend Analysis**: Fit trend lines and forecast future trade\n",
        "4. **Clustering**: Group countries or commodities by trade patterns\n",
        "\n",
        "### 🌐 External Data Integration\n",
        "1. **GDP Data**: Compare trade values with country GDP\n",
        "2. **Distance/Geography**: Analyze trade by geographic distance\n",
        "3. **Economic Indicators**: Correlate with global economic indicators\n",
        "4. **Exchange Rates**: Adjust values for currency fluctuations\n",
        "\n",
        "### 📊 Interactive Visualizations\n",
        "1. **Plotly/Dash**: Create interactive dashboards\n",
        "2. **Geographic Maps**: Plot trade flows on world maps\n",
        "3. **Network Analysis**: Visualize trade networks\n",
        "4. **Time Series Forecasting**: Predict future trade patterns\n",
        "\n",
        "### 💾 Data Processing\n",
        "1. **Data Validation**: Cross-check with official statistics\n",
        "2. **Data Cleaning**: Handle missing values and outliers\n",
        "3. **Data Enrichment**: Add country names, HS code descriptions\n",
        "4. **Performance Optimization**: Optimize queries for large datasets\n"
    ]))
    
    # Data Export Section
    cells.append(create_notebook_cell("markdown", [
        "## 10. Data Export to CSV"
    ]))
    
    cells.append(create_notebook_cell("code", [
        "\n",
        "# Create output directory if it doesn't exist\n",
        "import os\n",
        "output_dir = 'output_csv'\n",
        "os.makedirs(output_dir, exist_ok=True)\n",
        "\n",
        "print(\"Exporting data to CSV files...\")\n",
        "print(\"=\" * 50)\n",
        "\n",
        f"# 1. Export full raw dataset (warning: large file)\n",
        "print(\"1. Exporting full raw dataset...\")\n",
        f"df.to_csv(f'{{output_dir}}/japan_trade_{year}_full.csv', index=False)\n",
        "print(f\"   ✓ Saved: {{output_dir}}/japan_trade_{year}_full.csv ({{len(df):,}} records)\")\n",
        "\n",
        "# 2. Export monthly trade summary\n",
        "print(\"2. Exporting monthly trade summary...\")\n",
        "monthly_trade_export = monthly_trade.reset_index()\n",
        "monthly_trade_export.columns = ['Year_Month', 'Export_Trillion_Yen', 'Import_Trillion_Yen', 'Balance_Trillion_Yen']\n",
        f"monthly_trade_export.to_csv(f'{{output_dir}}/monthly_trade_summary_{year}.csv', index=False)\n",
        "print(f\"   ✓ Saved: {{output_dir}}/monthly_trade_summary_{year}.csv ({{len(monthly_trade_export)}} records)\")\n",
        "\n",
        "# 3. Export top trading partners\n",
        "print(\"3. Exporting top trading partners...\")\n",
        "partner_export = partner_display.reset_index()\n",
        "partner_export.columns = ['Country_Code', 'Export_Billion_Yen', 'Import_Billion_Yen', 'Total_Billion_Yen', 'Balance_Billion_Yen']\n",
        f"partner_export.to_csv(f'{{output_dir}}/top_trading_partners_{year}.csv', index=False)\n",
        "print(f\"   ✓ Saved: {{output_dir}}/top_trading_partners_{year}.csv ({{len(partner_export)}} records)\")\n",
        "\n",
        "# 4. Export top commodity categories\n",
        "print(\"4. Exporting top commodity categories...\")\n",
        "hs2_export = hs2_display.reset_index()\n",
        "hs2_export.columns = ['HS2_Code', 'Export_Billion_Yen', 'Import_Billion_Yen', 'Total_Billion_Yen', 'Balance_Billion_Yen']\n",
        f"hs2_export.to_csv(f'{{output_dir}}/top_commodities_hs2_{year}.csv', index=False)\n",
        "print(f\"   ✓ Saved: {{output_dir}}/top_commodities_hs2_{year}.csv ({{len(hs2_export)}} records)\")\n",
        "\n",
        "# 5. Export country concentration analysis\n",
        "print(\"5. Exporting country concentration analysis...\")\n",
        "country_concentration = country_stats.reset_index()\n",
        "country_concentration.columns = ['Country_Code', 'Total_Value_Yen', 'Transaction_Count', 'Average_Value_Yen', 'Cumulative_Value_Yen', 'Cumulative_Percentage']\n",
        f"country_concentration.to_csv(f'{{output_dir}}/country_concentration_{year}.csv', index=False)\n",
        "print(f\"   ✓ Saved: {{output_dir}}/country_concentration_{year}.csv ({{len(country_concentration)}} records)\")\n",
        "\n",
        "# 6. Export key insights summary\n",
        "print(\"6. Exporting key insights summary...\")\n",
        "insights_data = {\n",
        "    'Metric': [\n",
        "        'Total Trade Value (Trillion Yen)',\n",
        "        'Export Share (%)',\n",
        "        'Import Share (%)',\n",
        "        'Top Trading Partner (Country Code)',\n",
        "        'Top Trading Partner Share (%)',\n",
        "        'Top Commodity Category (HS2)',\n",
        "        'Top Commodity Share (%)',\n",
        "        'Number of Trading Partners',\n",
        "        'Trade Status',\n",
        "        'Trade Balance (Trillion Yen)'\n",
        "    ],\n",
        "    'Value': [\n",
        "        f\"{total_trade/1e12:.2f}\",\n",
        "        f\"{export_share:.1f}\",\n",
        "        f\"{import_share:.1f}\",\n",
        "        f\"{top_partner}\",\n",
        "        f\"{top_partner_share:.1f}\",\n",
        "        f\"{top_commodity}\",\n",
        "        f\"{top_commodity_share:.1f}\",\n",
        "        f\"{df.Country.nunique()}\",\n",
        "        \"DEFICIT\" if import_share > export_share else \"SURPLUS\",\n",
        "        f\"{(exports - imports)/1e12:.3f}\"\n",
        "    ]\n",
        "}\n",
        "insights_df = pd.DataFrame(insights_data)\n",
        f"insights_df.to_csv(f'{{output_dir}}/key_insights_{year}.csv', index=False)\n",
        "print(f\"   ✓ Saved: {{output_dir}}/key_insights_{year}.csv ({{len(insights_df)}} records)\")\n",
        "\n",
        "print(\"\\n\" + \"=\" * 50)\n",
        "print(\"📁 All CSV files exported to:\", os.path.abspath(output_dir))\n",
        "print(\"\\n📋 Files created:\")\n",
        "for file in sorted(os.listdir(output_dir)):\n",
        "    if file.endswith('.csv'):\n",
        "        file_path = os.path.join(output_dir, file)\n",
        "        file_size = os.path.getsize(file_path) / 1024 / 1024  # MB\n",
        "        print(f\"   • {file} ({file_size:.1f} MB)\")\n",
        "\n",
        "print(\"\\n💡 Usage recommendations:\")\n",
        f"print(\"   • Use 'japan_trade_{year}_full.csv' for detailed analysis\")\n",
        f"print(\"   • Use 'monthly_trade_summary_{year}.csv' for time series analysis\")\n",
        f"print(\"   • Use 'top_trading_partners_{year}.csv' for partner analysis\")\n",
        f"print(\"   • Use 'top_commodities_hs2_{year}.csv' for commodity analysis\")\n",
        f"print(\"   • Use 'key_insights_{year}.csv' for executive summary\")"
    ]))
    
    return cells


def create_notebook(db_path, output_path):
    """Create and save the Jupyter notebook."""
    cells = generate_notebook_content(db_path)
    
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.8.0",
                "mimetype": "text/x-python",
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "pygments_lexer": "ipython3",
                "nbconvert_exporter": "python",
                "file_extension": ".py"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2, ensure_ascii=False)
    
    print(f"Jupyter notebook created: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate a comprehensive Jupyter notebook for Japan trade statistics analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_trade_analysis_notebook.py input-data/ym_2020.db
  python generate_trade_analysis_notebook.py input-data/ym_2021.db trade_analysis_2021.ipynb
        """
    )
    
    parser.add_argument(
        'database',
        help='Path to the SQLite database file'
    )
    
    parser.add_argument(
        'output',
        nargs='?',
        help='Output notebook file name (optional, will auto-generate if not provided)'
    )
    
    args = parser.parse_args()
    
    # Validate database file
    if not Path(args.database).exists():
        print(f"Error: Database file '{args.database}' does not exist.")
        sys.exit(1)
    
    # Generate output filename if not provided
    if args.output is None:
        db_name = Path(args.database).stem
        args.output = f"trade_analysis_{db_name}.ipynb"
    
    # Create the notebook
    create_notebook(args.database, args.output)
    
    print(f"\n🎉 Notebook generated successfully!")
    print(f"📁 File: {args.output}")
    print(f"🚀 To open: jupyter notebook {args.output}")
    print(f"\n📋 The notebook includes:")
    print("   • Data loading and exploration")
    print("   • Trade balance analysis")
    print("   • Top trading partners")
    print("   • Commodity analysis")
    print("   • Time series analysis")
    print("   • Geographic patterns")
    print("   • Advanced analysis functions")
    print("   • Key insights and summary")
    print("   • CSV data export functionality")


if __name__ == "__main__":
    main()