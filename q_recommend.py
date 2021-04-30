import math 
import os,csv
r_path='/home/tsuruta/workspace/cf/latestsmall'
recommend_user='611'#推薦対象のユーザ

def other_loadMovieLens(path='./latestsmall'):#その他ジャンルのデータセット読み込み(ここではAction以外)

	movies={}
	genrelist=[]
	with open(path+'/movies.csv',encoding='ISO-8859-1') as f:
		for line in f:
			reader=csv.reader(f)
			for row in reader:
				id=row[0]
				title=row[1]
				genre=row[2]
				genre=row[2]
				if 'Action' not in genre:
					movies[id]=title
					genrelist.append(id)
	#print(movies)
	dataset={}
	with open(path+'/ratings.csv',encoding='ISO-8859-1') as f:
		for line in f:
			reader=csv.reader(f)  
			for row in reader:
				user=row[0]
				movieid=row[1]
				rating=row[2]
				ts=row[3]
				if movieid in genrelist:
					dataset.setdefault(user,{})
					dataset[user][movies[movieid]]=float(rating)
	return dataset


def specfic_loadMovieLens(path='./latestsmall'):#特定のジャンルのデータセット読み込み(ここではAction)


	movies={}
	genrelist=[]
	with open(path+'/movies.csv',encoding='ISO-8859-1') as f:
		for line in f:
			reader=csv.reader(f)
			for row in reader:
				id=row[0]
				title=row[1]
				genre=row[2]
				genre=row[2]
				if 'Action' in genre:
					movies[id]=title
					genrelist.append(id)
	dataset={}
	with open(path+'/ratings.csv',encoding='ISO-8859-1') as f:
		for line in f:
			reader=csv.reader(f)  
			for row in reader:
				user=row[0]
				movieid=row[1]
				rating=row[2]
				ts=row[3]
				if movieid in genrelist:
					dataset.setdefault(user,{})
					dataset[user][movies[movieid]]=float(rating)
	return dataset


def get_similarity_p(person1,person2): #その他ジャンルでのユーザ同士のピアソン相関を求める

	si={}
	for item in dataset[person1]:
		if item in dataset[person2]:
			si[item]=1

	n=len(si)
	if n<3: #共通でみた映画が3未満の場合は類似度を0とする
		return 0

	sum1=sum(dataset[person1][it] for it in si)
	sum2=sum(dataset[person2][it] for it in si)

	sum1Sq=sum([pow(dataset[person1][it],2) for it in si])
	sum2Sq=sum([pow(dataset[person2][it],2) for it in si])
	pSum=sum([dataset[person1][it]*dataset[person2][it] for it in si])
	num=pSum-(sum1*sum2/n)
	den=math.sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
	if den==0:
		return 0

	return num/den


def most_similar_users(person,number_of_users):

	similar_person_list=[]
	scores=[[get_similarity_p(person,other_person),other_person] for other_person in dataset if other_person != person]
	scores.sort()
	scores.reverse()
	for i in range(number_of_users):
		similar_person_list.append(scores[i][1])
	return similar_person_list


def s_get_similarity_p(person1,person2): #似たユーザ同士でのピアソン相関
	si={}
	for item in specific_dataset[person1]:
		if item in specific_dataset[person2]:
			si[item]=1
	n=len(si)
	if n<2: #共通でみた映画がない場合は類似度を0とする
		return 0

	sum1=sum(specific_dataset[person1][it] for it in si)
	sum2=sum(specific_dataset[person2][it] for it in si)

	sum1Sq=sum([pow(specific_dataset[person1][it],2) for it in si])
	sum2Sq=sum([pow(specific_dataset[person2][it],2) for it in si])
	pSum=sum([specific_dataset[person1][it]*specific_dataset[person2][it] for it in si])
	num=pSum-(sum1*sum2/n)
	den=math.sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
	if den==0:
		return 0

	return num/den

def s_most_similar_users(person,number_of_users):

	scores=[[s_get_similarity_p(person,other_person),other_person] for other_person in specific_dataset if other_person != person]
	scores.sort()
	scores.reverse()
	return scores[0:number_of_users]


dataset=other_loadMovieLens()#特定のジャンル以外のデータセット
specific_dataset=specfic_loadMovieLens()#特定のジャンルのデータセット
all_person=specific_dataset.keys()#特定のジャンル内のすべてのユーザのリスト


similar_person_list=most_similar_users(recommend_user,20)#特定ジャンル以外の中でrecommend_userに似たユーザリスト上位20
similar_person_list.append(recommend_user)
different_set=list(set(all_person)-set(similar_person_list))#特定のジャンル内での上記の似た上位20のユーザ以外のユーザ

for name in different_set:
	del specific_dataset[name]#特定のジャンル内のデータセットからそれらを除く


s_similar_person_list=s_most_similar_users(recommend_user,20)#特定のジャンル内での抽出されたユーザの類似度


specific_user=min(s_similar_person_list)#特定のジャンル内で似ていないユーザ


specific_user_number=specific_user[1]
s_persons_data=specific_dataset[specific_user_number]

max_val = max(s_persons_data.values())
final_dict = [key for key in s_persons_data if s_persons_data[key] == max_val]#特定のジャンル内で似ていないユーザが高く評価した映画名のリスト
print(final_dict)
