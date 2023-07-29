"""
Created on Dec 20, 2012

@author: cris
"""

import sys
import numpy
import random
import math
from PoI import PoI
from VPoI import VPoI
from Session import Session
from User import User
from datetime import datetime
from datetime import timedelta


# set of poi objects
pois = dict()
vpois = dict()
vpoi_list = None
sessions = dict()
users = dict()
poi_features = dict()
session_features = dict()
categs = dict ()
frequencies = {}
frequencies_bigrams = {}

# un poi ha le sue categorie, ma non abbiamo la frequenza del poi in una categoria
top_cat_pisa = set(["chiesedipisa", "palazzidipisa", "pontidipisa", "museidipisa", "portedipisa" ,"torridipisa", "teatridipisa", "stazioniferroviariedipisa", "ciclidiaffreschidellatoscana", "cappelledipisa"])
#top_cat_firenze = set(["palazzidifirenze", "chiesedifirenze", "stradedifirenze", "torridifirenze", "piazzedifirenze", "museidifirenze", "teatridifirenze", "villedifirenze", "architetturedifirenze", "cappelledifirenze"])
#top_cat_rome = set(["romar.xcampitelli", "chiesetitolaridiroma", "architetturescomparsediroma", "zoneurbanistichediroma", "templiantichidiroma", "disposizionifonichediorganiacanne", "romar.iitrevi", "lineaa(metropolitanadiroma)", "basilichediroma", "palazzidiroma"])



def load_categ_pois(categ_pois):
	global categs
	for line in categ_pois:
		line_split = line.strip().split(" ")
		poi_id = line_split[1].strip()
		'''
		if 'FIPO' in poi_id:
			poi_id = int(poi_id.replace('FIPOIHPC1', ''))
		else:
			poi_id = int(poi_id.replace('F', ''))
		'''
		categ = line_split[0].strip()
		if poi_id not in categs:
			categs[poi_id] = [] 
		categs[poi_id].append(categ)

def load_info_pois(pois_info):
	global pois
	for line_poi in pois_info:
		line_split = line_poi.strip().split("|")
		poi_id = line_split[0].strip()
		'''
		if 'FIPO' in poi_id:
			poi_id = int(poi_id.replace('FIPOIHPC1', ''))
		else:
			poi_id = int(poi_id.replace('F', ''))
		'''
		poi_city = line_split[1].strip()
		poi_title = line_split[2].strip()
		poi_geo = [float(line_split[4].strip()), float(line_split[5].strip())]
		if poi_id in categs:
			poi_categs = list(categs[poi_id])
		else:
			poi_categs = []
		
		pois[poi_id] = PoI(poi_id, poi_city, poi_title, poi_geo, poi_categs)
		
	print 'Step 1 - Loaded list of PoIs'
	print "PoIs " , len(pois)
	   
def load_trajectories(trajectories, exclude_single_poi = True):
	global pois, vpois, sessions, users
	i = 0
	for line in trajectories:
		line_splitted = line.strip().split("\t")
		
		if len(line_splitted) <= 2 and exclude_single_poi:
			continue
		
		skip_session = False
		for point in line_splitted[1:]:
			point_info = point.strip().split(";")
			poi_id = point_info[0]
			#poi_id = int(point_info[0])
			if poi_id not in pois:
				skip_session = True
				break
		if skip_session:
			continue
			
		#session
		s = Session(i)
		session_pois = []	  
		  
		#vpoi
		for point in line_splitted[1:]:
			point_info = point.strip().split(";")
			poi_id = point_info[0]
			#poi_id = int(point_info[0])
			poi_num_photos = point_info[1]
			poi_begin = point_info[2]
			poi_end = point_info[3]
					   
			vpoi = VPoI(poi_id, poi_num_photos, poi_begin, poi_end)
			if poi_id not in vpois:
				vpois[poi_id] = [vpoi]
			else:
				vpois[poi_id].append(vpoi)
			session_pois.append(vpoi)
		
		#user
		user_id = line_splitted[0].strip()

		if user_id not in users:
			users[user_id] = User(user_id)
		#---
			
		s.set_pois(session_pois)
		sessions[i] = s
#		if i == 14:
#			print 'Session 14', sessions[i]
#			print 'pois' , [poi.get_id() for poi in s.get_pois()]
		user_sessions = users[user_id].get_sessions()
		user_sessions.append(s)
		i += 1	   
	
	print 'Step 2 - Loaded trajectories'
	print 'VPoIs ', len(vpois)
	print 'Sessions ', len(sessions)
	print 'Users ', len(users)
	print '------------------------'
	
def load_frequencies():
	global	 frequencies, frequencies_bigrams
	
	for session in sessions.itervalues():
		session_pois = session.get_pois()
		#print[poi.get_id() for poi in session_pois]
		for i, poi in enumerate(session_pois[:-1]):
			poi_id = poi.get_id()
			
			if poi_id not in frequencies:
				frequencies[poi_id] = {}
			current_poi = frequencies[poi_id]
		  
			next_poi_id = session_pois[i+1].get_id()
			
			if next_poi_id in current_poi:
				current_poi[next_poi_id] += 1
			else:
				current_poi[next_poi_id] = 1
				
	
				
		if len(session_pois) > 2:
			for i, poi in enumerate(session_pois[:-2]):
				tupl = (poi.get_id(), session_pois[i+1].get_id())
				
				if tupl not in frequencies_bigrams:
					frequencies_bigrams[tupl] = {}
				current_tupl = frequencies_bigrams[tupl]
				
				next_poi_id = session_pois[i+2].get_id()
				
				if next_poi_id in current_tupl:
					current_tupl[next_poi_id] += 1
				else:
					current_tupl[next_poi_id] = 1
					
	total = dict()
	for k, v in frequencies.iteritems():
		total[k] = 0 
		for k1, v1 in v.iteritems():
			total[k] += v1 
		
	print total
			
	for k, v in frequencies.iteritems():
		for k1, v1 in v.iteritems():
			v[k1] = float(v1) / total[k]
					
	total_bigrams = dict()
	for k, v in frequencies_bigrams.iteritems():
		total_bigrams[k] = 0 
		for k1, v1 in v.iteritems():
			total_bigrams[k] += v1 
			
	for k, v in frequencies_bigrams.iteritems():
		for k1, v1 in v.iteritems():
			 v[k1] = float(v1) / total_bigrams[k]
				
	print 'Freq',frequencies
	print 'Big' , frequencies_bigrams
	return [frequencies, frequencies_bigrams]

def compute_poi_features(userid, poi, current_session):
	global vpois, sessions, users
	poi_features = dict()
	'''
	-title, tags?? 
	-list of categories, number of categories
	-gps coords
	-num photos - per user id and total - don;t know if it makes sense calculating per userid 
			- it will not be user in the test phase, or not?
	-visit time per current poi (media, sigma squared, max, min, total)
	-wiki it, en, number of clicks
	-photos (avg , total, max, min) - for all and/or userid
	-starting probability
	-ending probability
	-middle probability
	-spatial density - number of pois/max number of pois
	-number of user who visited the poi / number of users
	-number of sessions containing poi / total number of sessions
	-number of photos of poi / total number of photos 
	'''
	# 1 - title
	#poi_features['title'] = poi.get_title()
	
	# 2 - list of categories - or number of categs?
	poi_features['categories'] = len(poi.get_categ())
	
	# 10 features
	poi_features.update(((x, 0) for x in top_cat_pisa))
	for cat in poi.get_categ():
		if cat in top_cat_pisa:
			poi_features[cat] = 1
	
	# 3 - list of coordinates[lat, long]
	#poi_features['coords'] = poi.get_geo()
	
	# 4 - number of pois in the proximity!!! TODO
	
	# STATS PER POI PER USER ID
	photos_poi_per_userid = 0
	visit_time_userid = 0
	user_counter = 0
	photos_per_user = 0
	for session in userid.get_sessions():
		for vpoi_obj in session.get_pois():
			if vpoi_obj.get_id() == poi.get_id():
				user_counter += 1 
	# 4 - number of photos per userid
				photos_poi_per_userid += vpoi_obj.get_num_photos()
	# 5 - total visit time of a poi per user (sum of time of the same poi in all sessions of the user)
	#   - the difference is in millis
				visit_time_userid += (vpoi_obj.get_stop() - vpoi_obj.get_start())
	# 27 - total number of photos for a user
			photos_per_user += vpoi_obj.get_num_photos()
	# 15 - avg number of photos of the current PoI per userid - does this make sense, it gives 2, user counter is bs
	if photos_poi_per_userid > 0:
		photos_poi_per_userid_avg = float(photos_poi_per_userid) / user_counter
	else:
		photos_poi_per_userid_avg = 0
	
	poi_features['photos_poi_userid_avg'] = photos_poi_per_userid_avg
	poi_features['photos_poi_userid_total'] = photos_poi_per_userid
	poi_features['photos_per_user'] = photos_per_user
	# 28 - ratio of photos of poi in user photos
	poi_features['poi_ratio_in_user_photos'] = float(photos_poi_per_userid) / photos_per_user
	poi_features['visit_time_userid'] = visit_time_userid
			
	#STATS PER POI PER ALL APPEARENCES IN SESSIONS  
	photos_total = 0
	photos_min = 10000 # how much should the number be 
	photos_max = 0
	visit_counter = 0
	visit_max = 0
	visit_min = float('inf') # equivalent of a 6 hours interval
	visit_total = 0 
	for vpoi_id, vpoi_list in vpois.iteritems():
		if vpoi_id == poi.get_id():
			visit_counter = len(vpoi_list)
			for vpoi_obj in vpoi_list:
		#6 - number of photos of poi per total in sessions
				photos_total += vpoi_obj.get_num_photos()
		#17 - max number of photos
				if vpoi_obj.get_num_photos() > photos_max:
					photos_max = vpoi_obj.get_num_photos()
		#18 - min number of photos
				if vpoi_obj.get_num_photos() < photos_min:
					photos_min = vpoi_obj.get_num_photos()
		#7 - visit time min
				if  (vpoi_obj.get_stop() - vpoi_obj.get_start()) < visit_min :
					visit_min = vpoi_obj.get_stop() - vpoi_obj.get_start()
		#8 - visit time max
				if  (vpoi_obj.get_stop() - vpoi_obj.get_start()) > visit_max :
					visit_max = vpoi_obj.get_stop() - vpoi_obj.get_start()
		#9 - visit time cumulative
				visit_total += vpoi_obj.get_stop() - vpoi_obj.get_start()
	#16 - average number of photos per poi in all sessions
	if photos_total > 0 and visit_counter > 0:
		photos_avg = float(photos_total) / visit_counter
	else:
		photos_avg = 0
	
	#26 total visits
	poi_features['visits'] = visit_counter
	poi_features['photos_total'] = photos_total
	poi_features['photos_avg'] = photos_avg
	poi_features['photos_min'] = photos_min
	poi_features['photos_max'] = photos_max
	poi_features['visit_min'] = visit_min
	poi_features['visit_max'] = visit_max
	poi_features['visit_total'] = visit_total
	
	#10 - media - arithmetic, sigma squared
	# check for sum 0 -  0 division
	if visit_total > 0 and visit_counter > 0:
		mean = float(visit_total)/visit_counter
	else:
		mean = 0
	poi_features['visit_mean'] = mean
	
	#11 - standard deviation 
	sigmasq = 0 
	if visit_counter > 0:
		dif_sum = 0
		for vpoi_id, vpoi_list in vpois.iteritems():
			if vpoi_id == poi.get_id():
				for vpoi_obj in vpoi_list:
					dif_sum += ((vpoi_obj.get_stop() - vpoi_obj.get_start()) - mean)**2
		if dif_sum > 0:
			sigmasq = (float(dif_sum) / visit_counter)**.5
	poi_features['visit_std_dev'] = sigmasq
	
	#12 wiki it {0,1}
	#13 wiki en {0,1}
	#14 number of clicks - for both?
	
	#22 spatial density - need bounding box info 
		
	#23 number of users who visited the poi / number of users
	users_visiting_poi = 0
	visited = 0
	for user_id, user in users.iteritems():
		for session in user.get_sessions():
			for vpoi in session.get_pois():
				if vpoi.get_id() == poi.get_id():
					visited = 1
					break
			if visited ==1:
				break
			else:
				continue
		if visited == 1:
			users_visiting_poi +=1
		visited = 0
	ratio_users_visiting_poi = float(users_visiting_poi) / len(users)  
	poi_features['ratio_users_visiting_poi'] = ratio_users_visiting_poi
	
	#24 number of sessions containing poi / total number of sessions
	sessions_with_poi = 0
	for session_id, session in sessions.iteritems():
		for vpoi in session.get_pois():
			if vpoi.get_id() == poi.get_id():
				sessions_with_poi += 1
				break
	ratio_sessions_with_poi = float(sessions_with_poi) / len(sessions)
	poi_features['ratio_sessions_with_poi'] = ratio_sessions_with_poi
	
	#25 num photos of PoI / number of photos
	total_num_photos =0
	for vpoi_list in vpois.itervalues():
		total_num_photos += sum(vpoi_obj.get_num_photos() for vpoi_obj in vpoi_list)
	ratio_photos_of_poi = float(photos_total) / total_num_photos
	poi_features['ratio_photos_of_poi'] = ratio_photos_of_poi
	
	start_counter = 0 
	stop_counter = 0
	for session in sessions.itervalues():
		if session.get_pois()[0].get_id() == poi.get_id():
			start_counter += 1
		if session.get_pois()[-1].get_id() == poi.get_id():
			stop_counter += 1
			
	#19 starting probability
	if start_counter > 0:		
		start_probability = float(start_counter) / sessions_with_poi
	else:
		start_probability = 0
	poi_features['start_probability'] = start_probability
		
	#20 stopping probability	 
	if stop_counter > 0:		
		stop_probability = float(stop_counter) / sessions_with_poi
	else:
		stop_probability = 0
	poi_features['stop_probability'] = stop_probability
	
	#21 middle probability - consider cases where traj have single pois !!!
	poi_features['middle_probability'] = 1 - start_probability - stop_probability
	
	#26 Distance between poi and last poi in session | TO DO
	#need to look for info in the pois dict
	last_poi_in_session = pois[current_session.get_pois()[-1].get_id()]
	
	dif_lat = poi.get_geo()[0] - last_poi_in_session.get_geo()[0]
	dif_len = poi.get_geo()[1] - last_poi_in_session.get_geo()[1]
	
	poi_features['distance_from_last_poi_lat'] = dif_lat
	poi_features['distance_from_last_poi_len'] = dif_len
	poi_features['distance_from_last_poi_euclidean'] = math.sqrt(dif_lat**2 + dif_len**2)
	
	#27 Distance between poi and first poi in session | TO DO
	first_poi_in_session = pois[current_session.get_pois()[0].get_id()]
	
	diff_lat = poi.get_geo()[0] - first_poi_in_session.get_geo()[0]
	diff_len = poi.get_geo()[0] - first_poi_in_session.get_geo()[0]
	
	poi_features['distance_from_first_poi_lat'] = diff_lat
	poi_features['distance_from_first_poi_len'] = diff_len
	poi_features['distance_from_first_poi_euclidean'] = math.sqrt(diff_lat**2 + diff_len**2)
	
	# 28 frequencies
	pair = [False, 0]
	last_poi = current_session.get_pois()[-1].get_id()
	if last_poi in frequencies:
		for k,v in frequencies[last_poi].iteritems():
			if k == poi.get_id():
				pair = [True, v]
			
	poi_features['freq'] = pair[1]

	# 29 frequncies_bigrams
	bigram = [False, 0]
	if len(current_session.get_pois()) > 2:
		tupl = (current_session.get_pois()[-2].get_id(), current_session.get_pois()[-1].get_id())
		if tupl in frequencies_bigrams:
			for k,v in frequencies_bigrams[tupl].iteritems():
				if k == poi.get_id():
					bigram = [True,v]
	poi_features['freq_bigram'] = bigram[1]
	
	
	# entropy
	last_session_poi = current_session.get_pois()[-1].get_id()
	out_dict = frequencies[last_session_poi]
	entropy = 0
	sum_freq = sum([v for v in out_dict.itervalues()])
	for k,v in out_dict.iteritems():
		vprob = float(v) / sum_freq
		entropy += vprob*math.log10(vprob)
	
	poi_features['entropy'] = -entropy	
		
	
	#print 'Number of POI features ', len(poi_features)
	#print poi_features 
#	for i in poi_features.iteritems():
#		if isinstance(i[1], list):
#			print 'is list', i[0]
	
#	print 'The list is ', [f.get_id() for f in current_session.get_pois()]  
#	print 'The PoI is', poi.get_id()
#	print poi_features['freq']
#	print poi_features['freq_bigram']
#	
	return poi_features

	
def compute_session_features(userid, session):
	session_features = dict()
	'''
	-session length (in pois)
	-session time (total)
	-actual visit time (avg, global, max, min - check if same sequence of pois is repeated)
	-actual transfer time ( -II-)
	-number of sessions of the user / max number of sessions made by a user
	-info about sessions per (current???) user (max, min, avg, total)
	-photos per poi in session (avg, global, min, max)
	-space walked (measured in bounding boxes) (avg, min, max, total)
	-bounding box distance between first and last poi of the session - long, lat, euclidean
	-categories pois per session - diversity of the session
	'''
	#'''
	# 1 session length 
	session_features['session_length'] = len(session.get_pois())
	
	# 2 session time
	session_features['sesion_time'] = session.get_pois()[-1].get_stop() - session.get_pois()[0].get_start()
	
	
	# 3 actual visit time
	actual_visit_time = 0
	for vpoi in session.get_pois():
		actual_visit_time += vpoi.get_stop() - vpoi.get_start()
	session_features['actual_visit_time'] = actual_visit_time
	
	# identify same sequence in other traj and calculate min, max, avg ???
	
	# 4 actual transfer time
	actual_transfer_time = 0
	
	session_pois = session.get_pois()
	
	for i in range(1, len(session.get_pois())):
		actual_transfer_time += session_pois[i].get_start() - session_pois[i-1].get_stop()
	session_features['actual_transfer_time'] = actual_transfer_time
	
	# identify same sequence in other traj and calculate min, max, avg ???
	
	# 5 number of sessions of the user / max number of sessions made by a user
	max_num_user_sessions = 0
	for user in users.itervalues():
		if len(user.get_sessions()) > max_num_user_sessions:
			max_num_user_sessions = len(user.get_sessions())
	#print 'max number of sessions', max_num_user_sessions
	session_features['user_sessions_ration'] = float(len(userid.get_sessions())) / max_num_user_sessions
	
	# 6 info about sessions per (current???) user (max, min, avg, total)
	user_session_length_max = 0
	user_session_length_min = 1000
	user_session_length_sum = 0
	
	for ses in userid.get_sessions():
		user_session_length_sum += len(ses.get_pois())
		if len(ses.get_pois()) > user_session_length_max:
			user_session_length_max = len(ses.get_pois())
		if len(ses.get_pois()) < user_session_length_min:
			user_session_length_min = len(ses.get_pois())
			
	session_features['user_session_length_max'] = user_session_length_max
	session_features['user_session_length_min'] = user_session_length_min
	session_features['user_session_length_avg'] = float(user_session_length_sum) / len(userid.get_sessions())
	session_features['user_session_length_total'] = user_session_length_sum
	
	# 7 photos per poi in session (avg, global, min, max)
	
	photos_poi_in_session_max = 0
	photos_poi_in_session_min = 10000
	photos_poi_in_session_sum = 0
	for poi in session_pois:
		photos_poi_in_session_sum += poi.get_num_photos()
		if poi.get_num_photos() > photos_poi_in_session_max :
			photos_poi_in_session_max = poi.get_num_photos()
		if poi.get_num_photos() < photos_poi_in_session_min :
			photos_poi_in_session_min = poi.get_num_photos()
	
	session_features['photos_poi_in_session_max'] = photos_poi_in_session_max
	session_features['photos_poi_in_session_min'] = photos_poi_in_session_min
	session_features['photos_poi_in_session_avg'] = float(photos_poi_in_session_sum) / len(session_pois)
	session_features['photos_poi_in_session_total'] = photos_poi_in_session_sum
	
	# 8 space walked (measured in bounding boxes) (avg, min, max, total)
	
	# 9 bounding box distance between first and last poi of the session - long, lat, euclidean
	
	# 10 categories pois per session - diversity of the session
	categs_per_session = 0
	categ_set = set()
	for vpoi in session_pois:
		for poi_id, poi_categ in pois.iteritems():
			if vpoi.get_id() == poi_categ.get_id():
				categs_per_session += len(poi_categ.get_categ())
				for category in poi_categ.get_categ():
					categ_set.add(category)
	session_features['categs_per_session'] = categs_per_session
	session_features['uniq_categs_per_session'] = len(categ_set)
		
	# categ in respect to the user!!! - per poi or per session TODO
	
	
	
	#3 distanze su pois in session 
	
	if len(session_pois) >1:
		lat_distance_max = lat_distance_min = pois[session_pois[1].get_id()].get_geo()[0] - pois[session_pois[0].get_id()].get_geo()[0]
		lat_distance_total = 0
		lon_distance_max = lon_distance_min = pois[session_pois[1].get_id()].get_geo()[1] - pois[session_pois[0].get_id()].get_geo()[1]
		lon_distance_total = 0
		euclid_max = euclid_min = math.sqrt(lat_distance_max**2 + lon_distance_max**2)
		euclid_total = 0
		for i, p in enumerate(session_pois[:-1]):
			lat_dif = pois[session_pois[i+1].get_id()].get_geo()[0] - pois[p.get_id()].get_geo()[0]
			if lat_dif > lat_distance_max:
				lat_distance_max = lat_dif
			if lat_dif < lat_distance_min:
				lat_distance_min = lat_dif
			lat_distance_total += lat_dif
				
			lon_dif = pois[session_pois[i+1].get_id()].get_geo()[1] - pois[p.get_id()].get_geo()[1]
			if lon_dif > lon_distance_max:
				lon_distance_max = lon_dif
			if lon_dif < lon_distance_min:
				lon_distance_min = lon_dif
			lon_distance_total += lon_dif
			
			euclid_dif = math.sqrt(lat_dif**2 + lon_dif**2)
			if euclid_dif > euclid_max:
				euclid_max = euclid_dif
			if euclid_dif < euclid_min:
				euclid_min = euclid_dif
			euclid_total += euclid_dif
		
		session_features['lat_distance_avg'] = avg_lat = float(lat_distance_total) / len(session_pois)
		session_features['lat_distance_min'] = lat_distance_min
		session_features['lat_distance_max'] = lat_distance_max
		session_features['lat_distance_total'] = lat_distance_total
		 
		session_features['lon_distance_avg'] = avg_lon = float(lon_distance_total) / len(session_pois)
		session_features['lon_distance_min'] = lon_distance_min
		session_features['lon_distance_max'] = lon_distance_max
		session_features['lon_distance_total'] = lon_distance_total
		
		session_features['euclidean_distance_avg'] = float(euclid_total) / len(session_pois)
		 
		session_features['euclidean_distance_min'] = euclid_min
		session_features['euclidean_distance_max'] = euclid_max
		session_features['euclidean_distance_total'] = euclid_total
		
	  
	else:
		
		session_features['lat_distance_avg'] = 0
		session_features['lat_distance_min'] = 0
		session_features['lat_distance_max'] = 0
		session_features['lat_distance_total'] = 0
		 
		session_features['lon_distance_avg'] = 0
		session_features['lon_distance_min'] = 0
		session_features['lon_distance_max'] = 0
		session_features['lon_distance_total'] = 0
		
		session_features['euclidean_distance_avg'] = 0
		 
		session_features['euclidean_distance_min'] = 0
		session_features['euclidean_distance_max'] = 0
		session_features['euclidean_distance_total'] = 0
		
  
	#print 'Number of SESSION features ', len(session_features)
	#print session_features
#	for i in session_features.iteritems():
#		if isinstance(i[1], list):
#			print 'is list', i[0]
	return session_features


def generate_negative_pois(session, next_poi, n):
	global vpoi_list, frequencies
	
	if not vpoi_list:
		vpoi_list = vpois.keys()
	
	result = set()	
	exclude = set(poi.get_id() for poi in session.get_pois())
	exclude.add(next_poi.get_id())
	neg_candidates = set()
	stop = n-4 # 4 negative candidates in proximity the rest are random
	
	if n > 0 :
		last_poi_in_session = session.get_pois()[-1].get_id()
		#print 'last poi in session', last_poi_in_session
		neg_candidates.update(frequencies[last_poi_in_session].keys())
		#print neg_candidates
		if len(neg_candidates) <= n-4: # 4 negative candidates in proximity the rest are random
			stop = len(neg_candidates)
		for id in neg_candidates:
			if id not in exclude:
				result.add(id)
				if len(result) >= stop:
					break
 		
	negative_pois = random.sample(vpoi_list, n * 2) if n > -1 else vpoi_list
	for poi_id in negative_pois:
		if poi_id not in exclude and poi_id not in neg_candidates:
			result.add(poi_id)
			if n > -1 and len(result) >= n:
				break
#	print 'Last in session ' , session.get_pois()[-1].get_id()
#	print 'Negative pois ' , result
#	print '----------'
	return result


  
