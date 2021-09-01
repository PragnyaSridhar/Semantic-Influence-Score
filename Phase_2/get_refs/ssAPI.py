import requests
import pandas as pd
from datetime import *
import time as Time
import os
import sys
import json

end_index = 0
start_index = 0

def get_references(csv_path,using='ID',save_name='',st_index=0,end_index = 0):
    # df = pd.read_csv(csv_path)
    with open(csv_path,'r') as f:
        files = f.read().splitlines()
    

    # global end_index
    if(end_index==0):
        end_index = len(files)
    files = files[st_index:end_index]
    

    # global start_index

    print('Total remaining=',end_index-st_index,'\n\n\n')

    if(using=='ID'):
        url_pre = 'https://api.semanticscholar.org/v1/paper/'
        # ids = list(df['ddId']) #DPK: change col name here
        ids = files

    # elif(using=='MAG'):
    #     url_pre =  'https://api.semanticscholar.org/v1/paper/MAG:'
    elif(using=='s2url'):
        url_pre='https://api.semanticscholar.org/v1/paper/CorpusID:'
        # ids = list(df['s2_url'])
        ids = files

    # try:
    #     with open('refID_'+str(end_index)+'.txt','r',encoding="utf-8") as f:
    #         ret_refID = f.read().split('\n\n\n')
    #     with open('refNames_'+str(end_index)+'.txt','r',encoding="utf-8") as f:
    #         ret_refNames = f.read().split('\n\n\n')
    # except:
    #     ret_refID = []
    #     ret_refNames = []


    ret_refID = []
    ret_refNames = []

    time_lim = datetime.now()+timedelta(minutes = 5)
    count = 0
    if(st_index!=0):
        with open(save_name,'r') as f:
            d = json.loads(f.read())
    else:
        d = dict()
    for ID in ids:
        # ID2 = ID.split(':')[-1]
        ID2 = ID
        if(count==100):
            # with open('refID_'+str(end_index)+'.txt','w+',encoding="utf-8") as f:
            #     f.write('\n\n\n'.join(ret_refID))
            # with open('refNames_'+str(end_index)+'.txt','w+',encoding="utf-8") as f:
            #     f.write('\n\n\n'.join(ret_refNames))
            # df['Ref IDs'] = ret_refID
            # df['Ref Names'] = ret_refNames

            # if (save_name!=''):
            #     df.to_csv(savename,index=False)
            count=0
            d1 = json.dumps(d)
            with open(save_name,'w+') as f:
                f.write(d1)
            print('Saved obtained refs')

            if(datetime.now()<time_lim):
                count = 0
                sleeptime = (time_lim - datetime.now()).seconds
                print('Sleeping for ',sleeptime)
                Time.sleep(sleeptime)
                print('; Resumed ...')
                time_lim = datetime.now()+timedelta(minutes = 5)
                

        count+=1

        url = url_pre+ID2.strip()

        response = requests.get(url)
        err=0

        if(response.status_code!=200):
            print(response.status_code)
            time_i = 1
            while(response.status_code!=200):
                if(response.status_code==404):
                    print(ids.index(ID),url)
                    err = 1
                    break

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

        if(err):
            refID = ''
            refNames = ''
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
            
            d[ID2] = {'refID':refID,'refNames':refNames}
            # refID = ' #;# '.join(refID)
            # refNames = ' #;# '.join(refNames)
        
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

    # d = json.dumps(d)
    with open(save_name,'w+') as f:
        f.write(json.dumps(d))



args = sys.argv[1:]

if(len(args)!=2):
    print('Start and End Indices')
else:
    st_index = args[0]
    en_index = args[1]
    # print('POOL A...')
    # get_references('poolA_s2urls.csv',using='s2url',save_name='basepaperID_PoolA.csv',index=1700)

    print('Running between ', st_index, en_index)
    get_references('l0_papers_ids.txt',using='ID',save_name = 'l0_ref_json.txt',st_index=int(st_index),end_index=int(en_index)) 

    # print('POOL C...')
    # get_references('poolC_s2urls.csv',using='s2url',save_name='basepaperID_PoolC.csv',index=1000)

    # print('Done')