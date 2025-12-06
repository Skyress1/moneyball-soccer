"""
Oyuncu karşılaştırma ve radar chart modülü
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import pi

def create_radar_chart(player_data, player_name, position):
    """Create a radar chart for player statistics"""
    
    # Position-specific attributes
    if position == 'FW':
        categories = ['Goals', 'Assists', 'xG', 'Shots', 'Dribbles', 'Progressive']
        values = [
            player_data['Gls_per90'],
            player_data['Ast_per90'],
            player_data['xG_per90'],
            player_data['Sh_per90'],
            player_data['Succ_Drib'] / (player_data['Min'] / 90) if player_data['Min'] > 0 else 0,
            (player_data['PrgC'] + player_data['PrgP']) / (player_data['Min'] / 90) if player_data['Min'] > 0 else 0
        ]
    elif position == 'MF':
        categories = ['Goals', 'Assists', 'Passing', 'Progressive', 'Tackles', 'Interceptions']
        values = [
            player_data['Gls_per90'],
            player_data['Ast_per90'],
            player_data['Cmp%'] / 10,
            (player_data['PrgC'] + player_data['PrgP']) / (player_data['Min'] / 90) if player_data['Min'] > 0 else 0,
            player_data['Tkl'] / (player_data['Min'] / 90) if player_data['Min'] > 0 else 0,
            player_data['Int'] / (player_data['Min'] / 90) if player_data['Min'] > 0 else 0
        ]
    elif position == 'DF':
        categories = ['Tackles', 'Interceptions', 'Blocks', 'Aerials', 'Passing', 'Progressive']
        values = [
            player_data['Tkl'] / (player_data['Min'] / 90) if player_data['Min'] > 0 else 0,
            player_data['Int'] / (player_data['Min'] / 90) if player_data['Min'] > 0 else 0,
            player_data['Blocks'] / (player_data['Min'] / 90) if player_data['Min'] > 0 else 0,
            player_data['AerWon'] / (player_data['Min'] / 90) if player_data['Min'] > 0 else 0,
            player_data['Cmp%'] / 10,
            player_data['PrgP'] / (player_data['Min'] / 90) if player_data['Min'] > 0 else 0
        ]
    else:  # GK
        categories = ['Passing', 'Progressive', 'Consistency', 'Distribution', 'Positioning', 'Sweeping']
        values = [
            player_data['Cmp%'] / 10,
            player_data['PrgP'] / (player_data['Min'] / 90) if player_data['Min'] > 0 else 0,
            player_data['MP'] / 38 * 10,
            player_data['TotDist'] / (player_data['Min']) if player_data['Min'] > 0 else 0,
            5.0,  # Placeholder
            player_data['Def_Pen'] / (player_data['Min'] / 90) if player_data['Min'] > 0 else 0
        ]
    
    # Normalize values to 0-10 scale
    max_values = {
        'Goals': 1.0, 'Assists': 0.8, 'xG': 1.0, 'Shots': 5.0, 'Dribbles': 3.0,
        'Progressive': 10.0, 'Passing': 10.0, 'Tackles': 5.0, 'Interceptions': 4.0,
        'Blocks': 3.0, 'Aerials': 5.0, 'Consistency': 10.0, 'Distribution': 0.1,
        'Positioning': 10.0, 'Sweeping': 1.0
    }
    
    normalized_values = []
    for cat, val in zip(categories, values):
        if cat in max_values and max_values[cat] > 0:
            normalized = min(10, (val / max_values[cat]) * 10)
        else:
            normalized = min(10, val)
        normalized_values.append(normalized)
    
    # Number of variables
    num_vars = len(categories)
    
    # Compute angle for each axis
    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
    normalized_values += normalized_values[:1]
    angles += angles[:1]
    
    # Initialize the plot
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
    
    # Draw one axis per variable and add labels
    plt.xticks(angles[:-1], categories, size=12, weight='bold')
    
    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([2, 4, 6, 8, 10], ["2", "4", "6", "8", "10"], color="grey", size=10)
    plt.ylim(0, 10)
    
    # Plot data
    ax.plot(angles, normalized_values, linewidth=2, linestyle='solid', color='#667eea')
    ax.fill(angles, normalized_values, alpha=0.25, color='#667eea')
    
    # Add title
    plt.title(f"{player_name}\n{position} - Performance Radar", 
              size=16, weight='bold', pad=20)
    
    # Add grid
    ax.grid(True, linestyle='--', alpha=0.7)
    
    return fig

def compare_players(player1_data, player2_data, player1_name, player2_name, position):
    """Create a comparison radar chart for two players"""
    
    # Position-specific attributes
    if position == 'FW':
        categories = ['Goals', 'Assists', 'xG', 'Shots', 'Dribbles', 'Progressive']
        values1 = [
            player1_data['Gls_per90'],
            player1_data['Ast_per90'],
            player1_data['xG_per90'],
            player1_data['Sh_per90'],
            player1_data['Succ_Drib'] / (player1_data['Min'] / 90) if player1_data['Min'] > 0 else 0,
            (player1_data['PrgC'] + player1_data['PrgP']) / (player1_data['Min'] / 90) if player1_data['Min'] > 0 else 0
        ]
        values2 = [
            player2_data['Gls_per90'],
            player2_data['Ast_per90'],
            player2_data['xG_per90'],
            player2_data['Sh_per90'],
            player2_data['Succ_Drib'] / (player2_data['Min'] / 90) if player2_data['Min'] > 0 else 0,
            (player2_data['PrgC'] + player2_data['PrgP']) / (player2_data['Min'] / 90) if player2_data['Min'] > 0 else 0
        ]
    elif position == 'MF':
        categories = ['Goals', 'Assists', 'Passing', 'Progressive', 'Tackles', 'Interceptions']
        values1 = [
            player1_data['Gls_per90'],
            player1_data['Ast_per90'],
            player1_data['Cmp%'] / 10,
            (player1_data['PrgC'] + player1_data['PrgP']) / (player1_data['Min'] / 90) if player1_data['Min'] > 0 else 0,
            player1_data['Tkl'] / (player1_data['Min'] / 90) if player1_data['Min'] > 0 else 0,
            player1_data['Int'] / (player1_data['Min'] / 90) if player1_data['Min'] > 0 else 0
        ]
        values2 = [
            player2_data['Gls_per90'],
            player2_data['Ast_per90'],
            player2_data['Cmp%'] / 10,
            (player2_data['PrgC'] + player2_data['PrgP']) / (player2_data['Min'] / 90) if player2_data['Min'] > 0 else 0,
            player2_data['Tkl'] / (player2_data['Min'] / 90) if player2_data['Min'] > 0 else 0,
            player2_data['Int'] / (player2_data['Min'] / 90) if player2_data['Min'] > 0 else 0
        ]
    elif position == 'DF':
        categories = ['Tackles', 'Interceptions', 'Blocks', 'Aerials', 'Passing', 'Progressive']
        values1 = [
            player1_data['Tkl'] / (player1_data['Min'] / 90) if player1_data['Min'] > 0 else 0,
            player1_data['Int'] / (player1_data['Min'] / 90) if player1_data['Min'] > 0 else 0,
            player1_data['Blocks'] / (player1_data['Min'] / 90) if player1_data['Min'] > 0 else 0,
            player1_data['AerWon'] / (player1_data['Min'] / 90) if player1_data['Min'] > 0 else 0,
            player1_data['Cmp%'] / 10,
            player1_data['PrgP'] / (player1_data['Min'] / 90) if player1_data['Min'] > 0 else 0
        ]
        values2 = [
            player2_data['Tkl'] / (player2_data['Min'] / 90) if player2_data['Min'] > 0 else 0,
            player2_data['Int'] / (player2_data['Min'] / 90) if player2_data['Min'] > 0 else 0,
            player2_data['Blocks'] / (player2_data['Min'] / 90) if player2_data['Min'] > 0 else 0,
            player2_data['AerWon'] / (player2_data['Min'] / 90) if player2_data['Min'] > 0 else 0,
            player2_data['Cmp%'] / 10,
            player2_data['PrgP'] / (player2_data['Min'] / 90) if player2_data['Min'] > 0 else 0
        ]
    else:  # GK
        categories = ['Passing', 'Progressive', 'Consistency', 'Distribution', 'Positioning', 'Sweeping']
        values1 = [
            player1_data['Cmp%'] / 10,
            player1_data['PrgP'] / (player1_data['Min'] / 90) if player1_data['Min'] > 0 else 0,
            player1_data['MP'] / 38 * 10,
            player1_data['TotDist'] / (player1_data['Min']) if player1_data['Min'] > 0 else 0,
            5.0,
            player1_data['Def_Pen'] / (player1_data['Min'] / 90) if player1_data['Min'] > 0 else 0
        ]
        values2 = [
            player2_data['Cmp%'] / 10,
            player2_data['PrgP'] / (player2_data['Min'] / 90) if player2_data['Min'] > 0 else 0,
            player2_data['MP'] / 38 * 10,
            player2_data['TotDist'] / (player2_data['Min']) if player2_data['Min'] > 0 else 0,
            5.0,
            player2_data['Def_Pen'] / (player2_data['Min'] / 90) if player2_data['Min'] > 0 else 0
        ]
    
    # Normalize values
    max_values = {
        'Goals': 1.0, 'Assists': 0.8, 'xG': 1.0, 'Shots': 5.0, 'Dribbles': 3.0,
        'Progressive': 10.0, 'Passing': 10.0, 'Tackles': 5.0, 'Interceptions': 4.0,
        'Blocks': 3.0, 'Aerials': 5.0, 'Consistency': 10.0, 'Distribution': 0.1,
        'Positioning': 10.0, 'Sweeping': 1.0
    }
    
    normalized_values1 = []
    normalized_values2 = []
    
    for cat, val1, val2 in zip(categories, values1, values2):
        if cat in max_values and max_values[cat] > 0:
            norm1 = min(10, (val1 / max_values[cat]) * 10)
            norm2 = min(10, (val2 / max_values[cat]) * 10)
        else:
            norm1 = min(10, val1)
            norm2 = min(10, val2)
        normalized_values1.append(norm1)
        normalized_values2.append(norm2)
    
    # Number of variables
    num_vars = len(categories)
    
    # Compute angle for each axis
    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
    normalized_values1 += normalized_values1[:1]
    normalized_values2 += normalized_values2[:1]
    angles += angles[:1]
    
    # Initialize the plot
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    # Draw one axis per variable and add labels
    plt.xticks(angles[:-1], categories, size=13, weight='bold')
    
    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([2, 4, 6, 8, 10], ["2", "4", "6", "8", "10"], color="grey", size=10)
    plt.ylim(0, 10)
    
    # Plot data for both players
    ax.plot(angles, normalized_values1, linewidth=2.5, linestyle='solid', 
            color='#667eea', label=player1_name)
    ax.fill(angles, normalized_values1, alpha=0.25, color='#667eea')
    
    ax.plot(angles, normalized_values2, linewidth=2.5, linestyle='solid', 
            color='#e74c3c', label=player2_name)
    ax.fill(angles, normalized_values2, alpha=0.25, color='#e74c3c')
    
    # Add title and legend
    plt.title(f"Player Comparison\n{player1_name} vs {player2_name}", 
              size=18, weight='bold', pad=20)
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=12)
    
    # Add grid
    ax.grid(True, linestyle='--', alpha=0.7)
    
    return fig
