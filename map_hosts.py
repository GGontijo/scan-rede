class MapHosts:
    def __init__(self, known_hosts, arp_hosts) -> None:
        self.knowns_mac = []
        self.known_obj = known_hosts
        for i in known_hosts:
            self.knowns_mac.append(i['mac'])
        self.arps = arp_hosts

    def match(self):
        self.matches_check = list(set(self.knowns_mac) & set(self.arps))
        self.matches_names = []
        for i in self.known_obj:
            if i['mac'] in self.matches_check:
                self.matches_names.append(i['name'])

        return self.matches_names
