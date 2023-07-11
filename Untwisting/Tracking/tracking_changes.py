
import numpy as np
import pandas as pd

#be sure to change the volumes
for csv_num in range(43,128):
    #try:
        #be sure to change file path
        csv_num = str(csv_num)
        file = r'Z:\\Cell_Tracking_Project\\Vab-1\\Tracking\\Pos2\\SPIMB\\Reg_Sample\\For_Tracking\\RegB\\Decon_reg_'+csv_num+'\\Decon_reg_'+csv_num+'_results\\integrated_annotation\\annotations.csv'
        df = pd.read_csv(file,header=None)
        df_np = df.to_numpy() 
        
        #annotation name
        r2_index = np.argwhere('P2'==df_np[:,0])
        #r3_index = np.argwhere('A13'== df_np[:,0])
    
        df_np[r2_index,0] = 'IL2DR'
        #temp = df_np[r2_index,0]
        #df_np[r2_index,0] = df_np[r3_index,0]
        #df_np[r3_index,0] = temp
        
        pd.DataFrame(df_np).to_csv(r'Z:\\Cell_Tracking_Project\\Vab-1\\Tracking\\Pos2\\SPIMB\\Reg_Sample\\For_Tracking\\RegB\\Decon_reg_'+csv_num+'\\Decon_reg_'+csv_num+'_results\\integrated_annotation\\annotations.csv',header=None, index=None)
    
    #except:
        #pass

  
