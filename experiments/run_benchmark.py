import json
import sys
import os

# Ensure we can import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.gape_engine import GapeEngine

def run_suite():
    print("----------------------------------------------------------------")
    print("  GAPE Framework: Reproducibility Benchmark (Paper Table 1)")
    print("----------------------------------------------------------------")
    
    # Load Scenarios
    try:
        with open('experiments/scenarios.json', 'r') as f:
            scenarios = json.load(f)
    except FileNotFoundError:
        print("Error: experiments/scenarios.json not found.")
        return

    # Initialize Engine (Using Mock DB connection for reproducibility without live Neo4j)
    # Note: In a real run, this connects to the live NKG. 
    # For the public repo, we rely on the SHACL graph loaded from files.
    engine = GapeEngine(uri="bolt://localhost:7687", auth=("neo4j", "password"))
    
    results = {"APPROVED": 0, "REJECTED": 0}
    
    print(f"Loaded {len(scenarios)} test scenarios.\n")

    for case in scenarios:
        print(f"Running Scenario: {case['id']} ({case['type']})")
        print(f"  Intent: {case['intent']}")
        
        # Execute Validation
        result = engine.validate_plan(case['plan'], case['mock_subgraph'])
        
        status = result['status']
        results[status] += 1
        
        print(f"  Result: [{status}]")
        if status == 'REJECTED':
            print(f"  Reason: {result['reason'][:100]}...") # Truncated for display
        print(f"  Latency: {result['latency_ms']:.2f} ms\n")

    print("----------------------------------------------------------------")
    print("SUMMARY")
    print(f"Total Scenarios: {len(scenarios)}")
    print(f"Violations Intercepted: {results['REJECTED']}")
    print(f"Safe Actions Allowed:   {results['APPROVED']}")
    print("----------------------------------------------------------------")

if __name__ == "__main__":
    run_suite()
