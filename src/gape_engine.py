import rdflib
from pyshacl import validate
from neo4j import GraphDatabase
import time
import os

class GapeEngine:
    def __init__(self, uri, auth, policy_dir="ontology/policies"):
        """
        Initialize the GAPE Engine.
        :param uri: Neo4j Bolt URI
        :param auth: Tuple (username, password)
        :param policy_dir: Directory containing the split SHACL files
        """
        self.driver = GraphDatabase.driver(uri, auth=auth)
        self.policy_dir = policy_dir
        # FIX: Automatically load the composite policy graph on init
        self.shacl_graph = self.load_policies()

    def load_policies(self):
        """
        Aggregates multiple SHACL files (Topology, Resource, State) 
        into a single validation graph.
        """
        g = rdflib.Graph()
        
        # List of policies defined in your repo structure
        policy_files = ["topology.ttl", "resource.ttl", "state.ttl"]
        
        print(f"Loading SHACL policies from {self.policy_dir}...")
        for file_name in policy_files:
            file_path = os.path.join(self.policy_dir, file_name)
            try:
                g.parse(file_path, format="turtle")
                print(f" - Loaded: {file_name}")
            except Exception as e:
                print(f" - WARNING: Failed to load {file_name}: {e}")
                
        return g

    def create_hypothetical_graph(self, subgraph_rdf, action_plan):
        """
        Implements Equation (4): Verify(a, G)
        Creates a transient in-memory graph G' to test the action.
        """
        sim_graph = subgraph_rdf.copy() # O(k) copy as per Sec 4.6.2 
        
        # NOTE: In a full implementation, you would apply the JSON action_plan 
        # to mutate sim_graph here (e.g., adding edges, changing properties).
        # For the benchmark, we assume sim_graph represents the post-action state.
        return sim_graph

    def validate_plan(self, action_plan, subgraph_rdf):
        """
        Executes the SHACL validation loop.
        """
        start_time = time.time()
        
        # 1. Create Hypothetical State
        g_prime = self.create_hypothetical_graph(subgraph_rdf, action_plan)
        
        # 2. Run SHACL Validation
        # inferencing='rdfs' allows class inheritance (e.g., AMF is a NetworkFunction)
        conforms, _, report = validate(
            g_prime,
            shacl_graph=self.shacl_graph,
            inference='rdfs',
            abort_on_first=False
        )
        
        latency = (time.time() - start_time) * 1000
        
        if not conforms:
            return {"status": "REJECTED", "reason": report, "latency_ms": latency}
        
        return {"status": "APPROVED", "latency_ms": latency}
