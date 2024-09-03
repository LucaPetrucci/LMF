# IP and PORT of the LMF within the docker network
LMF_IP = "lmf_net.org"
LMF_API_PORT = "4321"
LMF_PORT = 9090



### CORE NETOWRK USED ##
#CN_Used= "OAI"
CN_Used = "free5gc"

match CN_Used:
    case "OAI": # IP/PORT FOR OAI core network
        AMF_IP = "192.168.170.132"
        AMF_PORT = 8080
    case "free5gc":     # IP/PORT FOR free5gc
        AMF_IP = "10.100.200.50"
        AMF_PORT = 8000




# identifiuer of lmf network function
nfID = "97bfff10-1add-4a3f-b8d6-6b08a3718129"

# the maximum age of the estimation in minutes
MaxAgeOfEstimation= 5 

# information of the cell where the UE is connected
mcc = "001"
mnc = "01"
tac = "000001"

gNB_bitLength= 32
gNBValue = "00000E00"
trpID= 0


#Config information for the Location Alogorthms
# origin lat and lon are the coordinates of the origin of the cartesian system (0,0,0)
origin_lat = 0
origin_lon = 0
gNBPos= [{'x': 0,'y': 0},             
         {'x': 0,'y':300},
         {'x': 300,'y':0},
         {'x': 300,'y':300}]


