class MapHosts:
    def __init__(self, known_hosts, arp_hosts) -> None:
        self.knowns = []
        for i in known_hosts:
            self.knowns.append(i['mac'])
        self.arps = arp_hosts

    def match(self):
        self.matches = list(set(self.knowns) & set(self.arps))
        print(self.matches)
        return self.matches
