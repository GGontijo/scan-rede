class MapHosts:
    def __init__(self, known_hosts, arp_hosts) -> None:
        self.knowns = []
        for k, v in known_hosts:
            self.knowns.append(v)
        self.arps = arp_hosts

    def match(self):
        self.matches = list(set(self.knowns) & set(self.arps))
        print(self.matches)
        return self.matches
