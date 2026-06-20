import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
from datetime import time, datetime
import numpy as np
import plotly.express as px

mgapts = pd.read_csv("./megaptstable.csv")
ptsdiff = pd.read_csv("./ptsdiff.csv")


col1, col2 = st.columns(2)
with col1:
    st.subheader('Standings')
    st.image('./standings.png')
    
with col2:
    st.subheader('FRAUD-O-METER')
    st.image('./fraudnice.png')

st.subheader('Top 10 Player Weeks')
mgaptssrt = mgapts.sort_values(by='pts', ascending=False)
st.write(mgaptssrt.head(10))

st.subheader('See how your favourite player did.')
#player_name = st.text_input("Enter Player Name...", 'Carter Hart').strip()
player_names = sorted(mgapts['name'].dropna().unique().tolist())
player_name = st.selectbox("Enter Player Name...", options=player_names)

plr1, plr2 = st.columns(2)
with plr1:
    if player_name:
        player_stats = mgapts[mgapts['name'].str.upper() == player_name.upper()][['team', 'week', 'pts']].sort_values(by='week')
    else:    
        player_stats = []
    st.write(player_stats)
with plr2:
    if player_name:
        # rank_finder = mgapts.copy()
        # rankfinder = rank_finder.groupby(['name', 'position'], as_index=False)['pts'].sum().sort_values('pts', ascending=False)
        # rankfinder['rank'] = rank_finder['pts'].rank(ascending=False, method='min')
        # #rankfinder = mgapts.groupby(['name'], as_index=False)['pts'].sum().sort_values('pts', ascending=False)
        # rank = rankfinder[rankfinder['name'].str.upper() == player_name.upper()]

        # positionrank = mgapts.copy()
        # position_rank = positionrank.groupby(['name', 'position'], as_index=False)['pts'].sum().sort_values('pts', ascending=False)
        # row = position_rank.loc[position_rank['name'].str.lower() == player_name.lower()]
        # position = row['position'].iloc[0]
        # posrankfind = position_rank.copy()
        # position_rank_finder = posrankfind[posrankfind['position'] == position]
        # position_rank_finder['pos_rank'] = position_rank_finder['pts'].rank(ascending=False, method='min')
        # pos_rank = position_rank_finder[position_rank_finder['name'].str.upper() == player_name.upper()]

        # player_ranks = (mgapts.groupby(['name', 'position'], as_index=False)['pts'].sum().sort_values('pts', ascending=False).copy())
        # player_ranks['rank'] = player_ranks['pts'].rank(ascending=False,method='min').astype(int)

        player_ranks = (
            mgapts.groupby(['name', 'position'], as_index=False)['pts']
            .sum()
            .sort_values('pts', ascending=False)
            .copy()
        )
        player_ranks['overall_rank'] = player_ranks['pts'].rank(
            ascending=False,
            method='min'
        ).astype(int)

        result = player_ranks[
            player_ranks['name'].str.lower() == player_name.lower()
        ]

        player_name2 = result.iloc[0]['name']
        player_position = result.iloc[0]['position']
        player_pts = result.iloc[0]['pts']
        overall_rank = result.iloc[0]['overall_rank']

        position_table = (
            player_ranks[player_ranks['position'] == player_position]
            .sort_values('pts', ascending=False)
            .copy()
        )

        position_table['position_rank'] = position_table['pts'].rank(
            ascending=False,
            method='min'
        ).astype(int)

        player_position_row = position_table[
            position_table['name'].str.lower() == player_name.lower()
        ]
        
        position_rank = player_position_row.iloc[0]['position_rank']



        st.write(f'Total Points: {player_pts}')
        st.write(f"Overall Rank: {overall_rank}")
        st.write(f"Position Rank: {position_rank}")
    else:
        st.write('please select a player.')


# group by players, sum pts, find top 3 F, top 2 D, top G, Team of the Year
st.subheader('Team of the Year')

#bestplayers = mgapts.groupby("name", as_index=False)['pts'].sum().sort_values(ascending=False)
# bestplayers = (
#     mgapts.groupby('name', as_index=False)
#     .agg({'pts': 'sum', 'team': 'first', 'position': 'first'})
#     .sort_values('pts', ascending=False)
# )
bestplayers = (
    mgapts.groupby(['name', 'team', 'position'], as_index=False)['pts']
    .sum()
    .sort_values('pts', ascending=False)
)

bestF = bestplayers[bestplayers['position'] == 'F']
styledF = bestF[:3]
styledF = styledF.style.set_properties(
    **{'background-color': 'black', 'color': 'red'}
    )
st.write('Forwards')
st.write(styledF)

bestD = bestplayers[bestplayers['position'] == 'D']
styledD = bestD[:2]
styledD = styledD.style.set_properties(
    **{'background-color': 'black', 'color': 'blue'}
    )
st.write('Defensemen')
st.write(styledD)

bestG = bestplayers[bestplayers['position'] == 'G']
styledG = bestG[:1]
styledG = styledG.style.set_properties(
    **{'background-color': 'black', 'color': 'green'}
    )
st.write('Goalie')
st.write(styledG)


         
st.subheader('Here\'s how the season went.')
# fig = px.scatter(
#     mgapts,
#     x='week',
#     y='pts',
#     color='team',   # optional, but useful (allow user to switch between colour = team or colour = position)
#     hover_data=['team', 'name', 'week', 'position', 'pts'],
#     title='Player Points by Week'
# )

# fig.update_traces(mode='markers')
# fig.update_layout(
#     xaxis_title='Week',
#     yaxis_title='Points',
#     yaxis_range=[-15, 110]
# )


plot_df = mgapts.copy()

teams = sorted(mgapts['team'].dropna().unique().tolist())

selected_teams = st.multiselect(
    'Select team(s)',
    options=teams,
    default=teams
)

positions = st.multiselect(
    'Select positions',
    ['F','D','G'],
    default=['F','D','G']
)

colour_change = st.selectbox(
    'do you want different colour plot points based on Team or Position?',
    ('position', 'team')
)



filtered_df = mgapts[mgapts['team'].isin(selected_teams)].copy()

# np.random.seed(42)
# filtered_df['week_jitter'] = filtered_df['week'] + np.random.uniform(-0.2, 0.2, size=len(filtered_df))
filtered_df ['pts_bucket'] = plot_df['pts'].round(0)

filtered_df ['offset_num'] = filtered_df .groupby(['week', 'pts_bucket']).cumcount()
filtered_df ['count_same'] = filtered_df .groupby(['week', 'pts_bucket'])['pts'].transform('count')

filtered_df ['week_jitter'] = (
    filtered_df['week']
    + (filtered_df ['offset_num'] - (filtered_df ['count_same'] - 1) / 2) * 0.08
)

final_filter = filtered_df[filtered_df['position'].isin(positions)].copy()

position_colours = position_colors = {
    'D': '#1f77b4',   # blue
    'F': '#d62728',   # red
    'G': '#2ca02c',   # green
}

fig = px.scatter(
    final_filter,
    x='week_jitter',
    y='pts',
    color=colour_change,
    color_discrete_map=position_colours,
    hover_data={'week_jitter': False, 'pts_bucket': False, 'offset_num': False, 'count_same': False, 'team': True, 'name': True, 'week': True, 'position': True, 'pts': True},
    title='Player Points by Week (expand graph for better view)'
)

fig.update_traces(mode='markers')
fig.update_layout(
    xaxis_title='Week',
    yaxis_title='Points',
    yaxis_range=[-20, 110]
)

fig.update_xaxes(
    tickmode='linear',
    dtick=1
)

fig.update_layout(
    height=700
)

st.plotly_chart(fig, use_container_width=True)




st.subheader('Cumulative Point Differential')

teams2 = [col for col in ptsdiff.columns if col != 'Week']

selected_teams2 = st.multiselect(
    'Select team(s)',
    options=teams2,
    default=teams2
)

if not selected_teams2:
    st.warning('Please select at least one team.')
    st.stop()

fig = px.line(
    ptsdiff,
    x='Week',
    y=selected_teams2,
    line_shape='spline',
    title='Cumulative Point Differential by Week'
)

fig.update_layout(
    height=700,
    xaxis_title='Week',
    yaxis_title='Cumulative Point Differential',
    yaxis_range=[-1000, 1000]
)

st.plotly_chart(fig, use_container_width=True)


# playermoves = mgapts.groupby(['name', 'team'], as_index=False)['pts'].sum()
# playermoves = playermoves

# mltinames = mgapts.groupby('name')['team'].nunique()
# multi_team_names = mltinames[mltinames > 1].index

# multiteam_df = mgapts[mgapts['name'].isin(multi_team_names)]
# st.write(multiteam_df.sort_values(by='name'))
# movers = multiteam_df.groupby(['team', 'name','position'], as_index=False)['pts'].sum().sort_values('name')
# good_movers = movers[movers['pts'] >= 30]
# good_movers2 = good_movers.groupby('name').nunique()

grouped = mgapts.groupby(['name', 'team'], as_index=False)['pts'].sum()

three_team_30_names = (           
    grouped[grouped['pts'].ge(30)]
    .groupby('name')['team']
    .nunique()
    .loc[lambda s: s.gt(2)]
    .index
    .tolist()
)
#st.write(three_team_30_names)
#st.write(mgapts[mgapts['name'].isin(three_team_30_names)].sort_values('name'))

two_team_100_names = (           
    grouped[grouped['pts'].ge(100)]
    .groupby('name')['team']
    .nunique()
    .loc[lambda s: s.gt(1)]
    .index
    .tolist()
)
#st.write(two_team_100_names)
#st.write(mgapts[mgapts['name'].isin(two_team_100_names)].sort_values('name'))

st.subheader("Miscellaneous Stats")

with st.expander('Players with at least 30 points for 3 different teams'):
    three30 = mgapts[mgapts['name'].isin(three_team_30_names)].sort_values('name')
    three3 = three30.groupby(['team', 'name'], as_index=False)['pts'].sum().sort_values(by='name')
    three3 = three3[three3['pts'] >= 30]
    st.write(three3)

with st.expander('Players with at least 100 points for 2 different teams'):
    two100 = mgapts[mgapts['name'].isin(two_team_100_names)].sort_values('name')
    two1 = two100.groupby(['team', 'name'], as_index=False)['pts'].sum().sort_values(by='name')
    two1 = two1[two1['pts'] >= 100]
    st.write(two1)

# First half: weeks 1–10
first_half = (
    mgapts[mgapts['week'].between(1, 10)]
    .groupby('name', as_index=False)['pts']
    .sum()
    .rename(columns={'pts': 'first_half_pts'})
)

# Second half: weeks 11–20
second_half = (
    mgapts[mgapts['week'].between(11, 20)]
    .groupby('name', as_index=False)['pts']
    .sum()
    .rename(columns={'pts': 'second_half_pts'})
)

# Merge and compute difference
player_half_diff = first_half.merge(second_half, on='name', how='outer')

player_half_diff['pts_diff'] = player_half_diff['second_half_pts'] - player_half_diff['first_half_pts']

# Fill NaN for players who only appeared in one half
player_half_diff['first_half_pts'] = player_half_diff['first_half_pts'].fillna(0)
player_half_diff['second_half_pts'] = player_half_diff['second_half_pts'].fillna(0)

# Sort by pts_diff so best second-half improvers are at the top
player_half_diff = player_half_diff.sort_values('pts_diff', ascending=False)


with st.expander('Players that had us in the first half'):
    st.write(player_half_diff.sort_values('pts_diff').head(10))

st.write('*note: points that players got while not on someone\'s team are not counted.  Also injuries and stuff.')

with st.expander('You had to let these players cook'):
    st.write(player_half_diff.head(10))


teams_per_player = (
    mgapts.groupby('name', as_index=False)['team']
    .nunique()
    .rename(columns={'team': 'num_teams'})
)

top_7_players = (
    teams_per_player
    .sort_values('num_teams', ascending=False)
    .head(7)
    ['name']
    .tolist()
)

with st.expander('These players got tossed around'):
    st.write('Played for at least 5 teams (Johansson played for 6).')
    tossed = mgapts[mgapts['name'].isin(top_7_players)]
    tossed = tossed.groupby(['team','name'], as_index=False)['pts'].sum().sort_values(by='name',ascending=False)
    st.write(tossed)