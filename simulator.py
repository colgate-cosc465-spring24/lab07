#!/usr/bin/env python3

"""
Simulates Internet routing
"""

from argparse import ArgumentParser
import json

class AutonomousSystem:
    def __init__(self, number, prefix):
        self._number = number
        self._prefix = prefix
        self._customers = []
        self._providers = []
        self._peers = []
        self._routes = {self._prefix : Advertisement(self._prefix)}

    @property
    def number(self):
        """Get AS's number"""
        return self._number

    @property
    def prefix(self):
        """Get AS's own prefix"""
        return self._prefix

    @property
    def routes(self):
        """"Get AS's table of routes"""
        return self._routes

    def add_customer(self, customer):
        """Add a customer AS"""
        self._customers.append(customer)

    def add_provider(self, provider):
        """Add a provider AS"""
        self._providers.append(provider)

    def add_peer(self, peer):
        """Add a peer AS"""
        self._peers.append(peer)

    def originate_advertisement(self):
        """Send an advertisement for the AS's own prefix"""
        # TODO

    def forward_advertisement(self, ad):
        """Forward an advertisement to all relevant neighbors"""
        ad = ad.copy() # Create a copy to avoid reference-related problems
        # TODO

    def recv_advertisement(self, ad):
        """Receive an advertisement from a neighbor"""
        ad = ad.copy() # Create a copy to avoid reference-related problems 
        # TODO

    def __str__(self):
        return ("AS {} ({}): cust=[{}]; prov=[{}]; peer=[{}]".format( 
                self._number, self._prefix, 
                ','.join([str(AS.number) for AS in self._customers]),
                ','.join([str(AS.number) for AS in self._providers]),
                ','.join([str(AS.number) for AS in self._peers])))

class Advertisement:
    def __init__(self, prefix, path=[]):
        self._prefix = prefix
        self._path = path

    @property
    def prefix(self):
        return self._prefix

    @property
    def path_head(self):
        """Gets the nexthop AS"""
        if len(self._path) > 0:
            return self._path[0]
        else:
            return None

    @property
    def path_length(self):
        """Get the length of the path"""
        return len(self._path)

    def path_contains(self, AS):
        """Checks if AS already exists in the path"""
        return AS in self._path

    
    def add_to_path(self, AS):
        """Add an AS to the path"""
        self._path.insert(0, AS)

    def copy(self):
        """Creates a copy of this path"""
        return Advertisement(self._prefix, self._path.copy())

    def __str__(self):
        return ("{}: {}".format(self._prefix, 
                " -> ".join([str(AS.number) for AS in self._path])))

def load_topology(filepath):
    """Load a network topology and return a dictionary of AS objects"""
    # Load JSON
    with open(filepath) as topo_file:
        topo = json.load(topo_file)
  
    # Create ASes 
    ASes = {}
    for AS in topo["ases"]:
        AS = AutonomousSystem(AS["number"], AS["prefix"])
        ASes[AS.number] = AS

    # Create relationships
    for relationship in topo["relationships"]:
        if "customer" in relationship:
            customer = ASes[relationship["customer"]]
            provider = ASes[relationship["provider"]]
            customer.add_provider(provider)
            provider.add_customer(customer)
        else:
            peerA = ASes[relationship["peerA"]]
            peerB = ASes[relationship["peerB"]]
            peerA.add_peer(peerB)
            peerB.add_peer(peerA)

    return ASes 

def main():
    # Parse arguments
    arg_parser = ArgumentParser(description='Internet routing simulator')
    arg_parser.add_argument('topology', action='store',
            help='JSON file containing topology')
    settings = arg_parser.parse_args()

    # Load topology
    ASes = load_topology(settings.topology)
    print("***** Topology *****")
    for AS in ASes.values():
        print(AS)

    # Propagate routes
    for AS in ASes.values():
        AS.originate_advertisement()

    # Display routes
    print("***** Routes *****")
    for AS in ASes.values():
        print("AS %d" % AS.number)
        for route in AS.routes.values():
            print("\t{}".format(route))

if __name__ == '__main__':
    main()
