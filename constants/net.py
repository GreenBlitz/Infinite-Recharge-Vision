from tools.system import is_on_roborio_network

__is_on_roborio_network = is_on_roborio_network()

TCP_STREAM_IP = '10.45.90.8' if __is_on_roborio_network else '127.0.0.1'
TCP_STREAM_PORT = 5809
