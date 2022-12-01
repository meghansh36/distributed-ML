from typing import final, List
from nodes import Node

M: final = 3

PING_TIMEOOUT: final = 4

PING_DURATION: final = 5

CLEANUP_TIME: final = 20

TEST_FILES_PATH = "/home/bachina3/MP4/awesomedml/testfiles_more/"

DOWNLOAD_PATH = "/tmp/"

# INTRODUCER_DNS_HOST = '127.0.0.1'
INTRODUCER_DNS_HOST = "fa22-cs425-6901.cs.illinois.edu"
INTRODUCER_DNS_PORT = 8888

# USERNAME = 'meghansh'
USERNAME = "mgoel7"
PASSWORD = None

with open('/home/bachina3/MP3/awesomesdfs/password.txt') as f:
    line = f.readline()
    USERNAME = line.split(',')[0].strip()
    PASSWORD = line.split(',')[1].strip()
    f.close()


available_files_in_sdfs = ['135.jpeg', '199.jpeg', '151.jpeg', '24.jpeg', '10.jpeg', '149.jpeg', '144.jpeg', '119.jpeg', '100.jpeg', '124.jpeg', '101.jpeg', '176.jpeg', '163.jpeg', '155.jpeg', '159.jpeg', '177.jpeg', '152.jpeg', '19.jpeg', '3.jpeg', '169.jpeg', '25.jpeg', '28.jpeg', '130.jpeg', '127.jpeg', '110.jpeg', '196.jpeg', '185.jpeg', '109.jpeg', '168.jpeg', '131.jpeg', '172.jpeg', '195.jpeg', '113.jpeg', '26.jpeg', '106.jpeg', '164.jpeg', '21.jpeg', '173.jpeg', '12.jpeg', '181.jpeg', '198.jpeg', '15.jpeg', '126.jpeg', '148.jpeg', '17.jpeg', '123.jpeg', '174.jpeg', '186.jpeg', '111.jpeg', '147.jpeg', '136.jpeg', '153.jpeg', '189.jpeg', '121.jpeg', '141.jpeg', '140.jpeg', '115.jpeg', '137.jpeg', '188.jpeg', '162.jpeg', '192.jpeg', '187.jpeg', '107.jpeg', '14.jpeg', '125.jpeg', '157.jpeg', '122.jpeg', '166.jpeg', '183.jpeg', '145.jpeg', '193.jpeg', '108.jpeg', '154.jpeg', '2.jpeg', '143.jpeg', '171.jpeg', '22.jpeg', '105.jpeg', '156.jpeg', '129.jpeg', '161.jpeg', '18.jpeg', '179.jpeg', '11.jpeg', '117.jpeg', '27.jpeg', '138.jpeg', '118.jpeg', '134.jpeg', '139.jpeg', '1.jpeg', '178.jpeg', '23.jpeg', '114.jpeg', '128.jpeg', '158.jpeg', '102.jpeg', '170.jpeg', '146.jpeg', '200.jpeg', '175.jpeg', '150.jpeg', '13.jpeg', '184.jpeg', '182.jpeg', '194.jpeg', '197.jpeg', '191.jpeg', '142.jpeg', '165.jpeg', '160.jpeg', '132.jpeg', '133.jpeg', '104.jpeg', '167.jpeg', '180.jpeg', '20.jpeg', '103.jpeg', '16.jpeg', '190.jpeg', '120.jpeg', '29.jpeg', '112.jpeg', '116.jpeg']    

# H1: final = Node('127.0.0.1', 8001, USERNAME, PASSWORD, 'H1')
# H2: final = Node('127.0.0.1', 8002, USERNAME, PASSWORD, 'H2')
# H3: final = Node('127.0.0.1', 8003, USERNAME, PASSWORD, 'H3')
# H4: final = Node('127.0.0.1', 8004, USERNAME, PASSWORD, 'H4')
# H5: final = Node('127.0.0.1', 8005, USERNAME, PASSWORD, 'H5')
# H6: final = Node('127.0.0.1', 8006, USERNAME, PASSWORD, 'H6')
# H7: final = Node('127.0.0.1', 8007, USERNAME, PASSWORD, 'H7')
# H8: final = Node('127.0.0.1', 8008, USERNAME, PASSWORD, 'H8')
# H9: final = Node('127.0.0.1', 8009, USERNAME, PASSWORD, 'H9')
# H10: final = Node('127.0.0.1', 8010, USERNAME, PASSWORD, 'H10')

# Global nodes configuration
# ADD new nodes here...
H1: final = Node('fa22-cs425-6901.cs.illinois.edu', 8000,USERNAME, PASSWORD, 'H1')
H2: final = Node('fa22-cs425-6902.cs.illinois.edu', 8000,USERNAME, PASSWORD, 'H2')
H3: final = Node('fa22-cs425-6903.cs.illinois.edu', 8000,USERNAME, PASSWORD, 'H3')
H4: final = Node('fa22-cs425-6904.cs.illinois.edu', 8000,USERNAME, PASSWORD, 'H4')
H5: final = Node('fa22-cs425-6905.cs.illinois.edu', 8000,USERNAME, PASSWORD, 'H5')
H6: final = Node('fa22-cs425-6906.cs.illinois.edu', 8000,USERNAME, PASSWORD, 'H6')
H7: final = Node('fa22-cs425-6907.cs.illinois.edu', 8000,USERNAME, PASSWORD, 'H7')
H8: final = Node('fa22-cs425-6908.cs.illinois.edu', 8000,USERNAME, PASSWORD, 'H8')
H9: final = Node('fa22-cs425-6909.cs.illinois.edu', 8000,USERNAME, PASSWORD, 'H9')
H10: final = Node('fa22-cs425-6910.cs.illinois.edu', 8000,USERNAME, PASSWORD, 'H10')

# Current Ring topology
# Edit the ring as needed
GLOBAL_RING_TOPOLOGY: dict = {

    H1: [H2, H10, H5],

    H2: [H3, H1, H6],

    H3: [H4, H2, H7],

    H4: [H5, H3, H8],

    H5: [H6, H4, H9],

    H6: [H7, H5, H10],

    H7: [H8, H6, H1],

    H8: [H9, H7, H2],

    H9: [H10, H8, H3],

    H10: [H1, H9, H4]

}


class Config:
    """
    Config class which takes current hostname, port, introducer and testing flags from cmdline args. 
    """

    def __init__(self, hostname: str, port: int, testing: bool) -> None:

        self.node: Node = Config.get_node(hostname, port)
        self.ping_nodes: List[Node] = GLOBAL_RING_TOPOLOGY[self.node]
        self.introducerDNSNode = Node(INTRODUCER_DNS_HOST, INTRODUCER_DNS_PORT, USERNAME, PASSWORD)
        # self.introducerNode = None
        # self.introducerFlag = False
        # self.introducerNode = Node(introducer.split(
        #     ":")[0], int(introducer.split(":")[1]))

        # if (self.node.unique_name == self.introducerNode.unique_name):
        #     self.introducerFlag = True
        # else:
        #     self.introducerFlag = False

        self.testing = testing

    

    @staticmethod
    def get_node(hostname: str, port: int) -> Node:
        """Return class Node which matches hostname and port"""
        member = None
        for node in GLOBAL_RING_TOPOLOGY.keys():
            if node.host == hostname and node.port == port:
                member = node
                break

        return member

    @staticmethod
    def get_node_from_unique_name(unique_name: str) -> Node:
        """Return class Node which matches unique name"""
        member = None
        for node in GLOBAL_RING_TOPOLOGY.keys():
            if node.unique_name == unique_name:
                member = node
                break

        return member

    @staticmethod
    def get_node_from_id(id: str):
        for node in GLOBAL_RING_TOPOLOGY.keys():
            if node.name == id:
                return node
        
        return None
