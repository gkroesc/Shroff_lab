
import numpy as np
import pandas as pd

Path = 'X:\\shrofflab\\efn-2\\120222_efn-2\\Pos1\\SPIMB\\Reg_Sample\\For_Tracking\\RegB'

start_tp = 44

end_tp = 57

existing_annotation = 'DB6'

new_annotation = 'D6'

p1_end_tp = end_tp + 1

#be sure to change the volumes
for csv_num in range(start_tp, p1_end_tp):
    #try:
        #be sure to change file path
        csv_num = str(csv_num)
        file = Path + r'\\Decon_reg_'+csv_num+'\\Decon_reg_'+csv_num+'_results\\integrated_annotation\\annotations.csv'
        df = pd.read_csv(file,header=None)
        df_np = df.to_numpy() 
        
        #annotation name
        r2_index = np.argwhere(existing_annotation==df_np[:,0])
        #r3_index = np.argwhere('A13'== df_np[:,0])
    
        df_np[r2_index,0] = new_annotation
        #temp = df_np[r2_index,0]
        #df_np[r2_index,0] = df_np[r3_index,0]
        #df_np[r3_index,0] = temp
        
        pd.DataFrame(df_np).to_csv(Path + r'\\Decon_reg_'+csv_num+'\\Decon_reg_'+csv_num+'_results\\integrated_annotation\\annotations.csv',header=None, index=None)
    
    #except:
        #pass
print("Done")
  

  
