#!/usr/bin/env python
# -*- coding: utf-8 -*-

# assign.py : Find an assignment of students to teams that minimizes the total 
#			  amount of work the course staff needs to do, subject to the constraint 
#			  that no team may have more than 3 students.
# Augustine Joseph, Mandar Sudhir Baxi, Zachariah Kyle Meador
# Course: CS-B551-Fall2017
'''
Problem description: 
Find an assignment of students to teams that minimizes the total 
amount of work the course staff needs to do, subject to the constraint that no team
may have more than 3 students.

State Space: 
Combination of different student teams. Each team will have maximum 3 students. 
No student is shared between team

Initial State : 
No student team formed

Successor function: 
--The successor function will create list of student teams possible with (N+1) 
students given current state has N students team groups formed.
--Team will have not have students who do not prefer to work with each other
--We have restricted total successor states to 15 in this algorithm.
--In selecting 15 records, algorithm checks and pick up records where there are minimum
number of teams and teams do not have members who do not want to work with each other   
Example: 
Suppose there are 4 students A, B, C, D and A and D do not prefer to work as team
Initial State: 
Successor function Pass 1: All possible team combination with A included
(A) (AB) (AC) (ABC) 
Successor function Pass 2 : All possible team combination with A & B included
(A B) (A BC) (A BD) (A BCD) (AB) (AC B) (AC BD) (ABC) (ACD B)
Successor function Pass 3 : All possible team combination with A ,B & C included
(A B C) (A B CD) (A BC) (A BD C) (A BCD) (AB C) (AB CD)	(AC B)	(AC BD) (ABC) 
Successor function Pass 4 : All possible team combination with A ,B, C & D included
(A B C D) (A B CD) (A BC D) (A BD C) (A BCD) (AB C D) (AB CD) (AC B D) (AC BD) 
 (ABC D) 
 
Goal state: 
Student team formed with minimum work needed for course staff

Cost function: 
Total time required for course staff to adress student concerns

Brief Description of How Search Algorithm works:
--Algorithm implemented is Similar to BFS implementation
--Suppose we have 4 students A B C D
--First form all combinations possible between these 4 students considering group of 3
--While generating combinations, program ensures that combination does not have students
who do not want to work with each other 
--Algorithm restricts maximum successor state to 15 at each level based on criteria that 
there are minimum number of total teams and no team has unprefered members.
    Depth level 1 - Valid team combination with Student A included 
    Depth level 2 - Valid team combination with student A & B included 
    Depth level 3 - Valid team combination with student A & B & C included and 
    Depth level 4 - Valid team combination with student A & B & C & D included and

--In the end, we will have list of combinations by which student teams can be formed with 
max team size of 3 and no student shared between teams
--Now, calculate cost associated with each of this combination and find team combination 
with minimum cost

Simplification/Design Decision:

--possible Successor states are restricted to 15 
--This algorithm ensures that output of successor function adhers to problem costrains 
of maximum team size =3 and student can not be shared between teams. This helps to 
reduce state space possibilities at each depth 

''' 
#########################################################################################
from itertools import combinations
import sys
import re
import random


#########################################################################################
#Global variables
#########################################################################################
#List of all Students
student_list = []
#Prfered team size for each student
prefered_team_size=[]
#Prefered team members for each student
prefered_team_member=[]
#Non Prefered team members for each student
non_prefered_team_member=[]

level_wise_possible_groups=[]
valid_groups=[]
formatted_valid_groups=[]
group_with_time=[]

#########################################################################################
# name: get_input
# input: na
# output:  string
# purpose: get user input
# 
#########################################################################################
def get_input():
    # check if there is exactly four argument
    if len(sys.argv) != 5:
        print("Insufficient arguments" )
        sys.exit()
    return(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])


#########################################################################################
# name: form_lists(list_possible_groups,student_list,total_student_count)
# input: all possible combinatons of student group of different sizes, student name list 
#        student count
# output: Level wise list with student group combinatios. Groip will not have students
#         who don't perefer to be in team
#Total groups at each pass are restricted to 15. 
#For example we have student A B C D . A and D do not want to work with each other
#Level 1 - List group combination in which A is present - A AB AC ABC 
#Level 2 - List of group combination in which B is present but not A - B BC BD BCD
#Therefore combination of List 1 & List 2 will give all possible groups with A & B
#Level 3 - List of group combination in which C is present but not A & B - C CD
#Level 4 - List of group combination in which D is present but not A , B & C - D
#Total number of level will be equal to total student count 
#########################################################################################
def form_lists(list_possible_groups,student_list,total_student_count):
   for i in range(total_student_count):
    level=[]
    #As we move to next level, we have to ignore all previous student name since their 
    #possible combinations are already covered in previous level list
    ignore_list=[]
    #Create ignore list for each level For example for level 3 ignore list will be 
    #A, B in above example
    for j in range(i):
        ignore_list.append(student_list[j])
    #Check for each student group combination if group contains student name, if yes
    #add that group in list for that level. Also, ignore all groups with whcih are
    #already covered in previous levels using ignore list
    for sub_group in list_possible_groups :
        for std_name in sub_group:
            nonpref_list=[]
            idx= student_list.index(std_name)
            nonpref_list=non_prefered_team_member[idx]
            if (std_name in ignore_list) :
                break;
            if ((std_name == student_list[i]) ):
                unpref_list=(list(set(sub_group)&set(nonpref_list)))
                if (len(unpref_list)==0) :
                    level.append(sub_group)
    level_wise_possible_groups.append(level)
   
   #Create combinations for students  who do not want to work with each other
   ignore_group=[]
   for std in range(total_student_count):
      ignore_row=[]
      if(non_prefered_team_member[std] != "_") :
           ignore_row.append(student_list[std])
           ignore_row.extend(non_prefered_team_member[std])
           ignore_row = [ x for x in ignore_row if x is not "," ]
           ignore_group.append(ignore_row)

   #Check if any team formed has students who do not want to work with each other    
   chcek_unpref_grp=[]
   for grp in level_wise_possible_groups:
       unpref_row=[]
       for std in grp:
          flag=0
          for ignore_combination in ignore_group :
            common= (list(set(std)&set(ignore_combination)))
            unpref_count=len(common)
            if unpref_count >1 :
                flag=1
          if(flag==0) :             
              unpref_row.append(std)
   #Restrict successot states to 15
 
       max_limit=15
       if (max_limit < len(unpref_row)) :
           unpref_row=random.sample(unpref_row,max_limit)   
       chcek_unpref_grp.append(unpref_row) 
    
   return (chcek_unpref_grp)
   
#########################################################################################
# name: successor_form_valid_group(initial_group_list,total_student_count)
# input: Initial list of groups which contains first student mandatory in every group
#       Example: A AB AC AD ABC ABD ACD and total_student_count
# output: List of valid group combinations with all student with no group having students
#         who don't perefer to be in team
#After every pass, valid list of groups are formed with next student in list getting 
#madatorily added
#Total groups at each pass are restricted to 15. 
#While selecting 15 successors, algorithm checks combination has minimum teams formed
#Example : 
#A B C D are students. A has preferecne not to work with D
#Pass 0 : Initial List (A mandatory) -     (A) (AB) (AC) (ABC) 
#Pass 1 : Initial List (A,B mandatory)-    (A B) (A BC) (A BD) (A BCD) (AB) (AC B) 
#                                          (AC BD) (ABC) 
#Pass 2 : Initial List (A,B,C mandatory)-  (A B C) (A B CD) (A BC) (A BD C) (A BCD)	
#                                          (AB C) (AB CD)	(AC B)	(AC BD) (ABC) 
#Pass 3 : Initial List (A,B,C,D mandatory)-(A B C D) (A B CD) (A BC D) (A BD C) (A BCD) 
#                                          (AB C D) (AB CD) (AC B D) (AC BD) (ABC D) 
#########################################################################################
def successor_form_valid_group(initial_group_list,total_student_count):
#Iterate for n-1 times where n is number of student
 for i in range(total_student_count-1) :
     valid_list=[]
      #Get each element in current valid list
     for ini_grp in initial_group_list :
          #Check if this element can be appended with each element in next level group
          #combination
          #Example in pass 1, A from valid list will be checked with every element in 
          #level 2 (B, BC , BD, BCD) . Later AB which will be checked and so on...
         for append_grp in level_wise_possible_groups[i+1] :
             grp_list=[]
              #If  student group getting appended and initial list group  has NO student 
              #common, append that group to valid list (check_coomon==1)
              #Check if student group getting appended and initial list grouphas any 
              #student common. If yes, we should not append that group (check_common=2)
              #If intial list group has student madatory student requured already
              #add this group in valid list as it is (check_coomon==0)
             check_common=checkcommon(ini_grp,append_grp,student_list[i+1])
             if check_common == 1 :
                 grp_list.append(ini_grp)
                 grp_list.append(append_grp)
                 valid_list.append(grp_list)
             elif check_common ==0 :
                 grp_list.append(ini_grp)
                 valid_list.append(grp_list)
      
 #List mmay contain duplicate entries. Removing those duplicate entries        
     unique_valid_list=[]
     for j in valid_list:
      if j not in unique_valid_list:
         unique_valid_list.append(j)
     
     #Count number of teams in combination and append it with group as additional info
     min_team_list=[]    
     for team in unique_valid_list:
         min_team_row=[]
         team_1=str(team)
         cnt=team_1.count("(")
         min_team_row.append(team)
         min_team_row.append(cnt)
         min_team_list.append(min_team_row)
     #Get top 100 recoreds from valid combnations order by total team count ascending
     sort_limit=100
     if (sort_limit < len(min_team_list)) :
         min_team_list=sorted(min_team_list,key=lambda x: (x[1]))
         min_team_list=min_team_list[:sort_limit]
     for row in min_team_list:
         del row[1]
    
     #Pick random 15 records  from this subset (with minimun no of total team)      
     max_limit=12
     if (max_limit < len(min_team_list)) :
        unique_valid_list=random.sample(min_team_list,max_limit)
     #Initialise list for next pass         
     initial_group_list=unique_valid_list    
     
 return(unique_valid_list)

#########################################################################################
# name: checkcommon(ini_grp,append_grp,student_name)
# input: Inital group list, Next level valid group list, mandatory student name for current 
#level
# output: Whether there is common student in initial list group and next level list group
#If  student group getting appended and initial list group  has NO student common, 
#append that group to valid list (check_coomon==1)
#if student group getting appended and initial list grouphas any student common
#we should not append that group (check_common=2)
#If intial list group has student madatory student requured already
#add this group in valid list as it is (check_coomon==0) 
#########################################################################################
def checkcommon(ini_grp,append_grp,student_name):

#Flaten inital group lis and append group list. Extract name within single quote and 
#form list of extracted anmes
   ini_grp=str(ini_grp).replace('(','').replace(')','')
   ini_grp=re.findall(r"['\"](.*?)['\"]", ini_grp)
   append_grp=str(append_grp).replace('(','').replace(')','')
   append_grp=re.findall(r"['\"](.*?)['\"]", append_grp)
   
   for i in ini_grp:
       #initial list group has already mandatory student
       if (i==student_name ) :
           return 0
       else:
           for j in append_grp:
               #Initial list group and next level lis group has student in common
               if(j== i) :
                   return 2
   return 1

#########################################################################################
# name: format_group_list(valid_groups)
# input: Valid group list
# output: Cleaner and formmated valid group list
#Example:  [[[('A', 'C', 'D'), ('B',)]]]] transformed to [['A','C','D'],['B']] 
#########################################################################################
def format_group_list(valid_groups):
    for i in valid_groups: 
        grp_list=[]
        grp=str(i).replace('[','').replace(']','')
        grp=grp.split("),")
        for j in grp:
            j=re.findall(r"['\"](.*?)['\"]", j)
            grp_list.append(j)
       
        formatted_valid_groups.append(grp_list)
    return( formatted_valid_groups)

#########################################################################################
# name: check_prefered_size(subgrp_size, idx)
# input: Actual group length, index of student
# output: 0 if length is matching or in case of no prefernce; other wise 1
#########################################################################################
def check_prefered_size(size,idx):
    #Get prefered group size 
    prefred_size=prefered_team_size[idx]
    #If prefered size is zero , it means no preference , return 0
    if(int(prefred_size)== 0):
        return 0
    #If prefered size is matching ,  return 0
    elif (size== int(prefred_size)) :
      return 0
    else :
      return 1

#########################################################################################
# name: check_prefered_grp(student,sub_group,idx)
# input: Name of student, group assigned to student, index
# output: count of prefered members absent for student in group
#########################################################################################
def check_prefered_grp(student,sub_group,idx):
    pref_member_absent=0
    pref_member_list=[]
    #Get Prefered member name for stuents
    pref_member_list= prefered_team_member[idx]
    pref_member_list=pref_member_list.replace(","," ")
    pref_member_list=pref_member_list.split(" ")
   
    for pref_student in pref_member_list:
        
        if pref_student == '_' :
            #No preference specified by student
            pref_member_absent= 0
            return pref_member_absent
        else :
            flag=1
            for student in sub_group:
                #Prefered member is present in list
                if (student == pref_student ) :
                    flag=0
            if(flag==1) :
                #If flag is one after iterating over entire list 
                #indicated prefered member is absent
                pref_member_absent=pref_member_absent+1

    return pref_member_absent

#########################################################################################
# name: check_unprefered_grp(student,sub_group,idx)
# input: Name of student, group assigned to student, index
# output: count of non prefered members present for student in group
#########################################################################################
def check_unprefered_grp(student,sub_group,idx):
    unpref_member_present=0
    unpref_memmber_list=[]
    #Get Prefered member name for stuents
    unpref_memmber_list= non_prefered_team_member[idx]
    unpref_memmber_list=unpref_memmber_list.replace(","," ")
    unpref_memmber_list=unpref_memmber_list.split(" ")
       
    for unpref_member in unpref_memmber_list:
        if  unpref_member == '_' :
            unpref_member_present= 0
            return unpref_member_present
        else :
            for student in sub_group:
                if (student == unpref_member ) :
                    unpref_member_present=unpref_member_present+1
   
    return unpref_member_present

#########################################################################################
# name: calculate_time(formatted_valid_groups,k,n,m)
# input: Valid group list,k,n m
# output: Group list with corresponding time required
#########################################################################################
def calculate_time(formatted_valid_groups,k,m,n):
    group_metrics=[]
    for group in formatted_valid_groups:
        grp=[]
        prefered_size_missmatch=0
        prefered_member_mismatch=0
        unprefered_member_mismatch=0
        #Get total number of groups
        total_group=len(group)
        #Iterate through each sub group of student for each group
        for sub_group in group:
            subgrp_len= len(sub_group)
            #If SUb  group has more than two students, iterate through each student
            if subgrp_len > 1:
                for student in sub_group :
                    #Gent index of student in original student list.
                    #This is required to get all preferences for this student
                    idx= student_list.index(student)
                    
                    #Check prefered group size for student
                    size_mismatch=check_prefered_size(subgrp_len, idx)
                    if(size_mismatch==1) :
                        prefered_size_missmatch+=1
                    
                    #Check prefered group member alloted for student
                    pref_member_absent=check_prefered_grp(student,sub_group,idx)
                    prefered_member_mismatch=prefered_member_mismatch+pref_member_absent
                    
                    #Check prefered group member alloted for student
                    unpref_member_present=check_unprefered_grp(student,sub_group,idx)
                    unprefered_member_mismatch=unprefered_member_mismatch+unpref_member_present
            else :
                #It is single student group
                #Gent index of student in original student list.
                #This is required to get all preferences for this student
                idx= student_list.index(sub_group[0])
                
                #Check prefered group size for student
                size_mismatch=check_prefered_size(1, idx)
                if(size_mismatch==1) :
                    prefered_size_missmatch+=1

                #Check prefered group member alloted for student
                pref_member_absent=check_prefered_grp(sub_group,sub_group,idx)
                prefered_member_mismatch=prefered_member_mismatch+pref_member_absent
                
                #Check prefered group member alloted for student
                unpref_member_present=check_unprefered_grp(sub_group,sub_group,idx)
                unprefered_member_mismatch=unprefered_member_mismatch+unpref_member_present
       
        time=total_group*int(k)+prefered_size_missmatch+prefered_member_mismatch*int(n)+unprefered_member_mismatch*int(m)
        
        grp.append(group)
        grp.append(time)
        group_metrics.append(grp)
    return(group_metrics)



#########################################################################################
# name: team_assignment(input_file,k,m,n)
# input: input file name, k, n, m
# output: Optimal group composition with total time
#########################################################################################
def team_assignment(input_file,k,m,n):

#Read input file line by line
 with open(input_file,'r') as f:
    for line in f:
        #First word will be student name. Store in in array
        student_list.append(line.split(None, 1)[0])
        #Second word will be prefered team size 
        prefered_team_size.append(line.split()[1])
        #Third word will be prefered team members 
        prefered_team_member.append(line.split()[2])
        #FOurth word will be non prefered team members 
        non_prefered_team_member.append(line.split()[3])

 #Get count of total students    
 total_student_count=len(student_list)
 #Defind Max group size
 max_group_size=3
 list_possible_groups=[]
 #Get all possible combinatons of student group of different sizes ranging from 1 to 3
 #These may be valid or invalid (Same student repeated in group)
 for grp_size in range(max_group_size):
    list_possible_groups.extend(combinations(student_list, grp_size + 1))

 #Form level wise list with student group combinatios
 level_wise=form_lists(list_possible_groups,student_list,total_student_count)
 
 #Initialise level 0 group list
 initial_group_list=level_wise[0]
 
 #Form List of valid group combinations with all student
 valid_groups=successor_form_valid_group(initial_group_list,total_student_count)
 
 #Remove unanted square bracket and other punctualtion markd from final group lsit
 formatted_valid_groups=format_group_list (valid_groups) 

 #Calculate time for each group
 group_with_time=calculate_time(formatted_valid_groups,k,m,n)
 #Sort list accoriding to time. First record will be of smallest time record
 group_with_time=sorted(group_with_time,key=lambda x: x[1])

 #Retrun group with shorted time
 return(group_with_time[0][0],group_with_time[0][1])

#########################################################################################
# name: main:
#########################################################################################

def main():
    #Read and get command line arguments
    input_file,k,m,n = get_input()
    #Get optimal group
    group, total_time = team_assignment(input_file,k,m,n)
    #Print optimal group composition with total time
    for i in group:
        print (str(i).replace('[','').replace(']','').replace(",",'').replace("'",''))
    print(total_time)

if __name__ == "__main__":
    main()
   
