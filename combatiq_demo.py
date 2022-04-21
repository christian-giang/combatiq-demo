import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from math import pi
from datetime import datetime

try:
    import pickle5 as pickle
except ImportError:
    import pickle

# *********** DEFINITION OF FUNCTIONS **************



# Function for plotting fighters clusters by round 

def plot_clusters(round):

	fig = plt.figure(figsize=(3,3))
	ax = plt.subplot(polar="True")

	categories = ['Distance', 'Clinch', 'Ground','Grappling', 'Aggressiveness']
	n_cats = len(categories)

	df_fighter_tmp = df_fighter_fight[df_fighter_fight['Rd']==round]
	df_opp_tmp = df_opp[df_opp['Rd']==round]

	#st.dataframe(df_fighter_tmp)

	values = [df_fighter_tmp['ClusterDST'].values,df_fighter_tmp['ClusterCLC'].values,df_fighter_tmp['ClusterGRD'].values,df_fighter_tmp['ClusterGRAP'].values,df_fighter_tmp['ClusterAGGR'].values]
	values +=values[:1]

	values_opp = [df_opp_tmp['ClusterDST'].values,df_opp_tmp['ClusterCLC'].values,df_opp_tmp['ClusterGRD'].values,df_opp_tmp['ClusterGRAP'].values,df_opp_tmp['ClusterAGGR'].values]
	values_opp +=values_opp[:1]


	angles = [n/float(n_cats) * 2 * pi for n in range(n_cats)]
	angles +=angles[:1]

	plt.polar(angles,values, marker='s', color='crimson', label=df_fighter_tmp['FighterName'].values[0])
	plt.fill(angles, values, alpha=0.3 , color='crimson')
	plt.polar(angles,values_opp, marker='s' , color='dimgrey', label=df_opp_tmp['FighterName'].values[0])
	plt.fill(angles, values_opp, alpha=0.3, color='silver')
	plt.xticks(angles[:-1], categories)
	plt.title("ROUND " + str(round), loc='left', fontweight="bold")
	if round==2:
		plt.legend(bbox_to_anchor =(0.8, -0.15), ncol=1)

	ax.set_rlabel_position(0)



	plt.yticks([0,1,2], color='grey', size=10)

	return fig

# ***********************************************


# ********** SIDEBAR ELEMENTS *******************

st.sidebar.image("redciq-copy.png", width=100)
st.sidebar.markdown("###### 	This is a demo of the Combat IQ Fight Analyzer."
					" Currently, the analysis is limited to the five major weightclasses and fights with three rounds.")
#st.title("Combat IQ Fight Analyzer")


list_weightclasses = ['Featherweight','Lightweight','Welterweight','Middleweight','Heavyweight']

weightclass = st.sidebar.selectbox("Select a weightclass:", list_weightclasses)

#df = pd.read_pickle(weightclass + '_streamlit.pkl')			

#read the pickle file
picklefile = open(weightclass+'_streamlit.pkl', 'rb')
#unpickle the dataframe
df = pickle.load(picklefile)
#close file
picklefile.close()


list_fighters = np.sort(df['FighterName'].unique())
list_fighters = np.hstack(['*** Summary of data set ***',list_fighters])

fighter = st.sidebar.selectbox("Select a fighter:", list_fighters)

if fighter!= '*** Summary of data set ***':

	df_fighter = df[df['FighterName']==fighter]
	list_fights = np.sort(df_fighter['Date_formatted'].unique())
	list_fights = np.hstack(['*** Fighter\'s history ***',list_fights])
	sel_fight = st.sidebar.selectbox("Select a fight:", list_fights)
	


#*************************************************


#*************** MAIN PAGE ELEMENTS **************


if fighter == "*** Summary of data set ***":

	st.title(weightclass + " data set")
	#with st.expander("Show complete data table"):
	#	st.dataframe(df)
	col1a, col1b = st.columns(2)
	col1a.metric("Total fights", df['FightUrl'].nunique())
	col1b.metric("Total fighters", df['FighterName'].nunique())
	col1a.metric("Most fights", df['FighterName'].value_counts().index[0])
	col1b.metric("Most wins", df['Winner'].value_counts().index[0])

else:

	if sel_fight == '*** Fighter\'s history ***':
	
		st.markdown("## Fight history of " + fighter)	

		n_fights = df_fighter['FightUrl'].nunique()
		n_wins = int(df_fighter['Won'].sum()/3)

		col1a, col1b, col1c = st.columns(3)
		col1a.metric("Total Fights", n_fights)
		col1b.metric("Wins", n_wins)
		col1c.metric("Losses", n_fights-n_wins)


		df_fighter_chronological = df_fighter[df_fighter['Rd']==1].sort_values('Date_formatted')
		
		#with st.expander("Show complete data table"):
		#	st.dataframe(df_fighter_chronological)

		fig, ax = plt.subplots(figsize=(10, 2))
		ax.grid(color='black', ls = '-.', lw = 0.25)
		ax.set_yticks([0,1])
		ax.set_yticklabels(['Lost','Won'])
		ax.set_ylim([-0.25,1.25])

		ax.plot(df_fighter_chronological['Date_formatted'],df_fighter_chronological['Won'], marker='s', color='crimson')

		st.pyplot(fig)

	else:


		#st.markdown("### Analyze a specific fight")	

		df_fighter_fight = df_fighter[df_fighter['Date_formatted']==sel_fight]
		fighturl = df_fighter_fight['FightUrl'].unique()
		#st.write(fighturl[0])
		df_opp = df[(df['FightUrl']==fighturl[0])&(df['FighterName']!=fighter)]

		if df_fighter_fight['Winner'].unique()[0] == fighter:
			st.success("__Result__: " + fighter + " wins against " + df_opp['FighterName'].unique()[0] 
				+ " on " + sel_fight.isoformat() + " (" + df_fighter_fight['Event'].unique()[0] + ")")
		else:
			st.error("__Result__: " + fighter + " loses against " + df_opp['FighterName'].unique()[0] 
				+ " on " + sel_fight.isoformat() + " (" + df_fighter_fight['Event'].unique()[0] + ")")


		st.markdown("#### Style analysis by round")

		with st.expander("More about the style analysis"):
			st.info("These plots depict the styles of both opponents accross the three rounds of a fight." +
				" Styles are classfified using to the following five dimensions: Ground fight, clinch fight, distance fight, aggressiveness and grappling." +
				" Both fighters were rated in each round with respect to these five dimensions." +
				" The ratings were obtained by running machine learning methods (specifically clustering algorithms) on the entire data set including all fighters and metrics." +
				" The metrics comprised both standard features (such as number of strikes etc.) as well as features engineered using domain expertise and Combat IQ's propietary formulas." +
				" The output of the clustering method is the classification of each fighter to the different levels of the five dimensions (from 1 = poor to 3 = strong).")


		figRd1 = plot_clusters(1)
		figRd2 = plot_clusters(2)
		figRd3 = plot_clusters(3)

		col3a, col3b, col3c = st.columns(3)
		col3a.pyplot(figRd1)
		col3b.pyplot(figRd2)
		col3c.pyplot(figRd3)


		st.markdown("#### Fight metrics by round")
		
		#st.dataframe(df_opp)
		#st.dataframe(df_fighter_fight)
		col2a, col2b = st.columns(2)

		with col2a:
			sel_metric = st.selectbox("Select a metric:", ['Strikes', 'SigStrikes',
			       'Takedowns', 'Knockdowns', 'Reversals', 'Ctrl', 'StrikesAttmptd',
			       'SigStrikesAttmptd', 'TakedownsAttmptd', 'SIgStrikes_Head',
			       'SIgStrikes_Body', 'SIgStrikes_Legs', 'SIgStrikes_HeadAttmptd',
			       'SIgStrikes_BodyAttmptd', 'SIgStrikes_LegsAttmptd', 'DTN_SigStrikes',
			       'CLNCH_SigStrikes', 'GND_SigStrikes', 'DTN_SigStrikesAttmptd',
			       'CLNCH_SigStrikesAttmptd', 'GND_SigStrikesAttmptd'])

			with st.expander("More about the fight metrics"):
				st.info("This tool can be used to visualize and compare a specific fight metric for both opponents." +
						" As of now, all standard metrics (such as number of strikes etc.) are available." +
						" In order to protect Combat IQ's intellectual property, the engineered features are currently not displayed.")

		metrics_fighter = df_fighter_fight[sel_metric]
		metrics_opp = df_opp[sel_metric]
		fig, ax = plt.subplots()
		ax.plot([1,2,3], metrics_fighter, marker='s' ,color='crimson')
		ax.plot([1,2,3], metrics_opp, marker='s', color='dimgrey')
		ax.grid(color='black', ls = '-.', lw = 0.25)
		ax.set_xticks([1,2,3])

		plt.xlabel("Round")
		plt.ylabel(sel_metric)
		plt.legend([fighter, df_opp['FighterName'].unique()[0]],bbox_to_anchor =(1.0, 1.2))

		
		col2b.pyplot(fig)
