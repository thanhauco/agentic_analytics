import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import Optional, List
import numpy as np

class VizTools:
    """Tools for data visualization"""
    
    def __init__(self, style: str = "seaborn-v0_8", figsize: tuple = (10, 6)):
        plt.style.use(style)
        self.figsize = figsize
    
    def create_line_chart(self, df: pd.DataFrame, x_col: str, y_col: str, 
                         title: str = "Line Chart", save_path: Optional[str] = None):
        """Create a line chart"""
        fig, ax = plt.subplots(figsize=self.figsize)
        ax.plot(df[x_col], df[y_col], marker='o', linewidth=2)
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def create_bar_chart(self, df: pd.DataFrame, x_col: str, y_col: str,
                        title: str = "Bar Chart", save_path: Optional[str] = None):
        """Create a bar chart"""
        fig, ax = plt.subplots(figsize=self.figsize)
        ax.bar(df[x_col], df[y_col], color='steelblue', alpha=0.8)
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(title)
        ax.grid(True, alpha=0.3, axis='y')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def create_scatter_plot(self, df: pd.DataFrame, x_col: str, y_col: str,
                           hue_col: Optional[str] = None, title: str = "Scatter Plot",
                           save_path: Optional[str] = None):
        """Create a scatter plot"""
        fig, ax = plt.subplots(figsize=self.figsize)
        
        if hue_col:
            for category in df[hue_col].unique():
                mask = df[hue_col] == category
                ax.scatter(df[mask][x_col], df[mask][y_col], label=category, alpha=0.6)
            ax.legend()
        else:
            ax.scatter(df[x_col], df[y_col], alpha=0.6)
        
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def create_heatmap(self, df: pd.DataFrame, title: str = "Correlation Heatmap",
                      save_path: Optional[str] = None):
        """Create a correlation heatmap"""
        fig, ax = plt.subplots(figsize=self.figsize)
        sns.heatmap(df, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                   square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax)
        ax.set_title(title)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def create_distribution_plot(self, df: pd.DataFrame, column: str,
                                title: str = "Distribution Plot",
                                save_path: Optional[str] = None):
        """Create a distribution plot with histogram and KDE"""
        fig, ax = plt.subplots(figsize=self.figsize)
        ax.hist(df[column], bins=30, alpha=0.7, color='steelblue', edgecolor='black')
        ax.set_xlabel(column)
        ax.set_ylabel('Frequency')
        ax.set_title(title)
        ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
