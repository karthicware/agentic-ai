#!/usr/bin/env python3
"""
Test script for the knowledge agent integration
"""

import os
import sys
from dotenv import load_dotenv

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

load_dotenv()

def test_knowledge_module():
    """Test the knowledge module initialization and basic functionality"""
    try:
        from modules.knowledge_module import KnowledgeModule
        
        print("🔵 Testing Knowledge Module...")
        
        # Initialize the knowledge module
        knowledge_module = KnowledgeModule()
        print("✅ Knowledge module initialized successfully")
        
        # Test query decomposition
        test_query = "What are meal ordering procedures and stock count processes?"
        decomposed = knowledge_module.decompose_query(test_query)
        print(f"✅ Query decomposition test: {decomposed}")
        
        # Test vector store search (this will work if ChromaDB is set up)
        try:
            search_result = knowledge_module.search_vector_store("meal ordering", n_results=2)
            print(f"✅ Vector store search test: Found {len(search_result)} documents")
        except Exception as e:
            print(f"⚠️  Vector store search test: {str(e)} (This is expected if ChromaDB is not set up)")
        
        print("✅ Knowledge module test completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Knowledge module test failed: {str(e)}")
        return False

def test_agent_integration():
    """Test that the knowledge agent is properly integrated into the agent system"""
    try:
        from app.agent_builder import build_root_agent
        from app.agent_instructions import get_agent_instructions
        
        print("🔵 Testing Agent Integration...")
        
        # Test that knowledge agent instructions exist
        knowledge_instructions = get_agent_instructions("knowledge_agent")
        print("✅ Knowledge agent instructions loaded successfully")
        
        # Test that the root agent can be built (this will include the knowledge agent)
        root_agent = build_root_agent()
        print("✅ Root agent built successfully with knowledge agent integration")
        
        # Check if knowledge agent is in the main_multi_tool_agent sub-agents
        main_agent = None
        for sub_agent in root_agent.sub_agents:
            if sub_agent.name == "main_multi_tool_agent":
                main_agent = sub_agent
                break
        
        if main_agent:
            knowledge_agent_found = any(agent.name == "knowledge_agent" for agent in main_agent.sub_agents)
            if knowledge_agent_found:
                print("✅ Knowledge agent found in main_multi_tool_agent sub-agents")
            else:
                print("❌ Knowledge agent not found in main_multi_tool_agent sub-agents")
                return False
        else:
            print("❌ main_multi_tool_agent not found in root agent")
            return False
        
        print("✅ Agent integration test completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Agent integration test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Knowledge Agent Integration Tests...\n")
    
    # Test 1: Knowledge Module
    test1_passed = test_knowledge_module()
    print()
    
    # Test 2: Agent Integration
    test2_passed = test_agent_integration()
    print()
    
    # Summary
    if test1_passed and test2_passed:
        print("🎉 All tests passed! Knowledge agent is properly integrated.")
        print("\n📋 Next steps:")
        print("1. Ensure your .env file has the required Azure OpenAI credentials")
        print("2. Make sure your ChromaDB vector store is set up in ./chroma-db")
        print("3. Test the knowledge agent with queries like:")
        print("   - 'What are the meal ordering procedures?'")
        print("   - 'Tell me about stock count processes'")
        print("   - 'Explain catering management policies'")
    else:
        print("❌ Some tests failed. Please check the error messages above.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 