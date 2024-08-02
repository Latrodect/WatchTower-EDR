import platform
import datetime
import requests
import logging

from core.event_handler import EventHandler

if platform.system() == "Windows":
    import win32evtlog

class EventLogMonitor:
    def __init__(self, config):
        self.config = config
        self.event_handler = EventHandler()
        self.server_url = config.get("server_url", "http://localhost:8000/store/event")
        self.os_type = platform.system()

    def monitor(self):
        if self.os_type == "Windows":
            self.monitor_windows_event_log()
        elif self.os_type == "Linux":
            self.monitor_linux_syslog()
        else:
            self.event_handler.log_event('Unsupported OS', f'OS type {self.os_type} is not supported')

    def monitor_windows_event_log(self):
        server = 'localhost'
        logtype = 'System'
        hand = win32evtlog.OpenEventLog(server, logtype)
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

        events = win32evtlog.ReadEventLog(hand, flags, 0)
        for event in events:
            data = {
                'timestamp': datetime.datetime.now().isoformat(),
                'event_category': event.EventCategory,
                'time_generator': str(event.TimeGenerated),
                'source_name': event.SourceName,
                'event_id': event.EventID,
                'event_type': event.EventType,
                'event_data': event.StringInserts
            }
            self.send_data_to_server(data)

    def monitor_linux_syslog(self):
        try:
            with open('/var/log/syslog', 'r') as f:
                for line in f:
                    if 'error' in line.lower() or 'fail' in line.lower():
                        data = {
                            'timestamp': datetime.datetime.now().isoformat(),
                            'log': line.strip()
                        }
                        self.send_data_to_server(data)
        except FileNotFoundError:
            self.event_handler.log_event('File Not Found', '/var/log/syslog does not exist')

    def send_data_to_server(self, data):
        try:
            response = requests.post(self.server_url, json=data)
            response.raise_for_status()
        except requests.RequestException as e:
            self.event_handler.log_event('Server Error', f'Failed to send data to server: {e}')
