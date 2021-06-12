import requests
import pandas as pd
from datetime import *
import time as Time
import csv
import sys
import os
import telegram_send


end_index = 0
start_index = 0

def get_references(csv_path,using='ID',save_name='temp.csv',start_index=0,end_index=0):
    df = pd.read_csv(csv_path)   

    if(end_index==0):
        end_index = len(df)


    print('Total remaining=',end_index-start_index,'\n\n\n')

    if(using=='ID'):
        url_pre = 'https://api.semanticscholar.org/v1/paper/'
        ids = list(df['ddId']) #DPK: change col name here

    # elif(using=='MAG'):
    #     url_pre =  'https://api.semanticscholar.org/v1/paper/MAG:'
    elif(using=='s2url'):
        url_pre='https://api.semanticscholar.org/v1/paper/CorpusID:'
        ids = list(df['s2_url'])

    paper_names = list(df['title'])

    # try:
    #     with open('refID_'+str(end_index)+'.txt','r',encoding="utf-8") as f:
    #         ret_refID = f.read().split('\n\n\n')
    #     with open('refNames_'+str(end_index)+'.txt','r',encoding="utf-8") as f:
    #         ret_refNames = f.read().split('\n\n\n')
    # except:
    # ret_refID = []
    # ret_refNames = []

    time_lim = datetime.now()+timedelta(minutes = 5)
    count = start_index

    for index in range(start_index,end_index):
        ID = ids[index] 
        ID2 = ID.split(':')[-1]
        count+=1


        if(count%100==0):
            # with open('refID_'+str(end_index)+'.txt','w+',encoding="utf-8") as f:
            #     f.write('\n\n\n'.join(ret_refID))
            # with open('refNames_'+str(end_index)+'.txt','w+',encoding="utf-8") as f:
            #     f.write('\n\n\n'.join(ret_refNames))
            # df['Ref IDs'] = ret_refID
            # df['Ref Names'] = ret_refNames

            # if (save_name!=''):
            #     df.to_csv(savename,index=False)
            # print('Saved obtained refs')
            print(count)

            if(datetime.now()<time_lim):
                # count = 0
                sleeptime = (time_lim - datetime.now()).seconds
                print('Sleeping for ',sleeptime,end='\t')
                Time.sleep(sleeptime)
                print('; Resumed ...')
                time_lim = datetime.now()+timedelta(minutes = 5)
                


        url = url_pre+ID2.strip()

        response = requests.get(url)
        err=0

        if(response.status_code!=200):
            if(response.status_code==404):
                print(response.status_code, 'error on',index)
                continue
            else:
                print(response.status_code)
                print('Completed ',count)
                return
            # time_i = 1
            # while(response.status_code!=200):
            #     if(response.status_code==404):
            #         print(ids.index(ID),url)
            #         err = 1
            #         break

                # if(time_i==1):
                    # telegram_send.send(messages=["Fix me on M1"])
                    # print('\n\n\nRun from index')
                    # try:
                    #     with open('refID_'+str(end_index)+'.txt','r',encoding="utf-8") as f:
                    #         data_id = f.read().split('\n\n\n')
                    #     with open('refNames_'+str(end_index)+'.txt','r',encoding="utf-8") as f:
                    #         data_names = f.read().split('\n\n\n')
                    # except:
                    #     print('Files dont exists')
                    #     data_id = []
                    #     data_names = []
                    # print(start_index+len(data_id),start_index+len(data_names))
                    # os.system('python3 check_len.py')
                    # return 
                    
                # print('Retrying...',response.status_code,';\tSleeping for ',300*time_i)
                # Time.sleep(300*time_i)
                # time_i+=1
                # reponse = requests.get(url)

        # if(err):
        #     refID = ''
        #     refNames = ''
        else:
            c = response.status_code
            response = response.json()

            try:
                ref_list = response['references']
            except:
                # telegram_send.send(messages=["Error "+str(c)])
                print('Error ',str(c))
                

            refID = []
            refNames = []
            for i in range(len(ref_list)):
                refID.append(ref_list[i]['paperId'])
                refNames.append(ref_list[i]['title'])
            
            refID = ' #;# '.join(refID)
            refNames = ' #;# '.join(refNames)
            basepaper_ID = response.get('paperId','')
            fields_of_study = response.get('fieldsOfStudy','')
            influential_citation_count = response.get('influentialCitationCount',str(-1))
            cited_by = response.get('numCitedBy',str(-1))
            citing = response.get('numCiting',str(-1))
            venue = response.get('venue','')
            year = response.get('year','')
            authors = response.get('authors','')

            topics = [x['topic'] for x in response.get('topics',[])]

            with open(save_name,'a+') as f:
                writer = csv.writer(f)
                writer.writerow([index,ID2,basepaper_ID,paper_names[index],fields_of_study,influential_citation_count,
                cited_by,citing,venue,year,authors,topics,refID,refNames]) 
        
        # ret_refID.append(refID)
        # ret_refNames.append(refNames)

    # with open('refID_'+str(end_index)+'.txt','w+',encoding="utf-8") as f:
    #     f.write('\n\n\n'.join(ret_refID))
    # with open('refNames_'+str(end_index)+'.txt','w+',encoding="utf-8") as f:
    #     f.write('\n\n\n'.join(ret_refNames))

    # df['Ref IDs'] = ret_refID
    # df['Ref Names'] = ret_refNames

    # if(save_name!=''):
    #     df.to_csv(save_name,index=False)

    # print('\n\nYou are done! Please upload','refID_'+str(end_index)+'.txt and ','refNames_'+str(end_index)+'.txt before proceeding.')
    # return df, ret_refID, ret_refNames



args = sys.argv[1:]

if(len(args)!=2):
    print('Start Index and End Index')
else:
    start_index = int(args[0])
    end_index = int(args[1])
    # print('POOL A...')
    # get_references('poolA_s2urls.csv',using='s2url',save_name='basepaperID_PoolA.csv',index=1700)

    print('Running between ', start_index, end_index)
    save_name = 'basepapers.csv'
    if(save_name not in os.listdir('/')):
        with open(save_name,'a+') as f:
            writer = csv.writer(f)
            writer.writerow(['index','Corpus ID','S2 ID','name','fields_of_study','influential_citation_count',
                    'cited_by','citing','venue','year','authors','topics','refID','refNames']) 
            print('Wrote header') 
    get_references(csv_path='papers_of_interest.csv',using='s2url',save_name=save_name,start_index=start_index,end_index=end_index) 

    telegram_token = '1437027031:AAFZ3AiVsGrxNQcWYGrMemHLX4IGqosthjk'
    chat_id = '1422492198'
    path_config = telegram_send.get_config_path()
    with open(path_config, 'w') as f:
        f.write(f'[telegram]\ntoken = {telegram_token}\nchat_id = {chat_id}')
    telegram_send.send(messages=['Check M1'])
    # print('POOL C...')
    # get_references('poolC_s2urls.csv',using='s2url',save_name='basepaperID_PoolC.csv',index=1000)

    # print('Done')