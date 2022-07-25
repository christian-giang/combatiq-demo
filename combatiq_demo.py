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
	plt.title("ROUND " + str(round), loc='left', fontweight="bold", color="white")
	if round==2:
		plt.legend(bbox_to_anchor =(0.8, -0.15), ncol=1)

	ax.set_rlabel_position(0)

	ax.xaxis.label.set_color('white')
	ax.tick_params(axis='x', colors='white')
	ax.yaxis.label.set_color('white')
	ax.tick_params(axis='y', colors='white')

	plt.yticks([0,1,2], color='grey', size=10)
	fig.patch.set_alpha(0)


	return fig

# ***********************************************


# ********** PASSWORD CHECK *******************
pass_status = False
correct_pass = "c0mb4t!q2022"
if pass_status == False:
	text_input_container1 = st.empty()
	text_input_container2 = st.empty()
	text_input_container3 = st.empty()


	text_input_container1.image("redciq-copy.png", width=100)
	text_input_container2.markdown("If you want to  receive the access code, please fill out <a href='https://combatiq.io/register' style='text-align: left; '>this form</a>", unsafe_allow_html=True)	
	password = text_input_container3.text_input("Access code", type="password")

	if password == correct_pass:
		pass_status = True
		text_input_container1.empty()
		text_input_container2.empty()
		text_input_container3.empty()
	elif password =='':
		text_input_container4 = st.empty()
	else:
		st.error('The password entered is wrong.')


# ********** SIDEBAR ELEMENTS *******************
if pass_status == True:
	st.sidebar.image("redciq-copy.png", width=100)


	st.sidebar.markdown("###### By choosing one of the options below, you can explore the Combat IQ analysis tools."
						" Currently, past fight analysis is limited to the five major weightclasses and fights with three rounds.")

	choice_subpage = st.sidebar.radio(label="", options=('Fight predictions', 'Computer vision demo', 'Past fight analysis'))


	if choice_subpage == 'Fight predictions':
		subpage = 'pred'
	elif choice_subpage == 'Computer vision demo':
		subpage = 'cvdemo'
	else:
		subpage = 'styles'


	if subpage == 'styles':


		list_weightclasses = ['','Featherweight','Lightweight','Welterweight','Middleweight','Heavyweight']

		weightclass = st.sidebar.selectbox("Select a weightclass:", list_weightclasses)


		if weightclass!= '':

			# IF WITH PICKLE
			#df = pd.read_pickle(weightclass + '_streamlit.pkl')

			# IF WITH PICKLE5			
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

#*************** MAIN PAGE ELEMENTS **************

if pass_status == True:
	if subpage== 'pred':
		st.title('Fight predictions')
		# IF WITH PICKLE
		#df = pd.read_pickle(weightclass + '_streamlit.pkl')

		# IF WITH PICKLE5			
		#read the pickle file
		picklefile = open('20220730_predictions_bsv.pkl', 'rb')
		#unpickle the dataframe
		df_pred = pickle.load(picklefile).round(decimals=2)
		#close file
		
		picklefile.close()	
		st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)	

		# FPR THE MOMENT ODDS ARE NOT USED

		# genre = st.radio(label="Odds settings", options=('American odds', 'Decimal odds', 'Fractional odds'))


		# if genre == 'Fractional odds':
		# 	suffix = 'frac'
		# elif genre == 'Decimal odds':
		# 	suffix = 'dec'
		# else:
		# 	suffix = 'american'

		# odds_fighter1 = 'Fighter1_'+suffix
		# odds_fighter2 = 'Fighter2_'+suffix

		odds_fighter1 = 'Fighter1_proba'
		odds_fighter2 = 'Fighter2_proba'

		st.empty()
		st.info("Confidence values of winning predictions for " + df_pred.iloc[0,3] + " on " +  df_pred.iloc[0,4] + ". Fighters with limited data records are highlighted wiht an asterisk (*).")

		for index, row in df_pred.iterrows(): 

			transaction = row['TxID']
			bsv_link = 'https://whatsonchain.com/tx/' + transaction

			if row['Fighter1_nrecords'] < 3:
				display_name1 = row['RC'] + ' (*)'
			else:
				display_name1 = row['RC']

			if row['Fighter2_nrecords'] < 3:
				display_name2 = row['BC'] + ' (*)'
			else:
				display_name2 = row['BC']	

			
			col1, col2, col3 = st.columns(3)
			col1.markdown("<p style='text-align: center;'>"+display_name1+"</p>", unsafe_allow_html=True)
			col2.markdown("<p style='text-align: center;'>"+display_name2+"</p>", unsafe_allow_html=True)

			if row[odds_fighter1] > row[odds_fighter2]:
				col1.markdown("<p style='text-align: center; color:green;'>"+str(row[odds_fighter1])+"</p>", unsafe_allow_html=True)
				col2.markdown("<p style='text-align: center; color:red;'>"+str(row[odds_fighter2])+"</p>", unsafe_allow_html=True)
			else:
				col1.markdown("<p style='text-align: center; color:red;'>"+str(row[odds_fighter1])+"</p>", unsafe_allow_html=True)
				col2.markdown("<p style='text-align: center; color:green;'>"+str(row[odds_fighter2])+"</p>", unsafe_allow_html=True)

			col3.markdown("<p style='text-align: center; font-style:italic;'>"+row['Division']+"</p>", unsafe_allow_html=True)	
			col3.markdown("<p style='text-align: center;'> <a align='center' href='"+ bsv_link +"'>BSV record </a></p>", unsafe_allow_html=True)	
			col3.markdown("<p style='text-align: center;'> <br /> </p>", unsafe_allow_html=True)	

	elif subpage == 'cvdemo':
		st.video('https://www.youtube.com/watch?v=GwbuM0I9tzE')

	else:
		if weightclass!= '':
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
					fig.patch.set_alpha(0)

					ax.plot(df_fighter_chronological['Date_formatted'],df_fighter_chronological['Won'], marker='s', color='crimson')
					ax.xaxis.label.set_color('white')
					ax.tick_params(axis='x', colors='white')
					ax.yaxis.label.set_color('white')
					ax.tick_params(axis='y', colors='white')
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
					ax.xaxis.label.set_color('white')
					ax.tick_params(axis='x', colors='white')
					ax.yaxis.label.set_color('white')
					ax.tick_params(axis='y', colors='white')

					plt.xlabel("Round")
					plt.ylabel(sel_metric)
					plt.legend([fighter, df_opp['FighterName'].unique()[0]],bbox_to_anchor =(1.0, 1.2))
					fig.patch.set_alpha(0)
					
					
					col2b.pyplot(fig)
		else:
			st.markdown("#### Please select a weightclass from the dropdown menu on the left")

