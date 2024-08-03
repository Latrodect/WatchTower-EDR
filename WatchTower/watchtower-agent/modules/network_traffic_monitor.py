import psutil
from scapy.all import sniff, IP
import requests
import datetime
from core.event_handler import EventHandler

class NetworkTrafficMonitor:
    def __init__(self, config) -> None:
        self.event_handler = EventHandler()
        self.server_url = config.get("server_url", "http://localhost:8000/data/store/")
        self.endpoint = ""
        self.threshold = config.get("network_threshold", 1000)
        self.connections = []

    def monitor_network(self):
        sniff(prn=self.monitor, store=0, filter="ip")

    def monitor(self, packet):
        self.endpoint = "traffic"
        if packet.haslaer(IP):
            ip_src = packet[IP].src
            ip_dst = packet[IP].dst
            timestamp = datetime.datetime.now().isoformat()
            data = {
                'timestamp': timestamp,
                'source_ip': ip_src,
                'destionation_ip': ip_dst,
                'packet_length': len(packet)
            }
            self.send_data_to_server(data)

    def log(self):
        self.endpoint = "connections"
        for conn in psutil.net_connections():
            connection_info = {
                'fd': conn.fd,
                'family': conn.family,
                'type': conn.type,
                'laddr': conn.laddr,
                'raddr': conn.raddr,
                'status': conn.status,
                'pid': conn.pid
            }
            self.connections.append(connection_info)

            if len(self.connections) > self.threshold:
                message = f'High number of connections detected: {len(self.connections)}'
                self.event_handler.log_event('High Network Connections', message)
                self.send_data_to_server({
                    'timestamp': datetime.datetime.now().isoformat(),
                    'connections': self.connections,
                    'message': message
                })
                self.connections.clear()

    def send_data_to_server(self, data):
        try:
            url = f'{self.server_url}/{self.endpoint}'
            response = requests.post(url, json=data)
            response.raise_for_status()
        except requests.RequestException as e:
            self.event_handler.log_event('Server Error', f'Failed to send data to server: {e}')