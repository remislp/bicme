import scipy.io as sio

mat = sio.loadmat('../Data/Experimental/AChRealData.mat')

#print(mat_contents)

for key, value in mat.items() :
    print (key)
    
print('concentration: ', mat['concs'])
print('tcrit: ', mat['tcrit'])
print('tres; ', mat['tres'])
print('use_Chs:', mat['useChs'])
print('number of bursts = ', len(mat['bursts']) )
print('bursts shape', mat['bursts'].shape)
#print('resolved_data:', mat['resolved_data'])

print('************************')
mat1 = sio.loadmat('../Tests/Data/NormData.mat')
for key, value in mat1.items() :
    print (key)
print('data: ', mat1['data'])
    

    