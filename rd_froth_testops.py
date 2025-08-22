#!/usr/bin/env python3
"""
Complete Test Case Generator - Froth Test Ops
Features:
1. OpenAI Python SDK integration
2. Token management with limits
3. Comprehensive audit logging
4. Smart caching for repetitive prompts
5. Vector DB with sentence transformers for similarity matching
6. Fallback to local generation when similar test cases exist

Dependencies:
pip install openai tiktoken sentence-transformers chromadb pandas numpy python-dotenv
"""

import os
import json
import hashlib
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import pandas as pd
import numpy as np
from dataclasses import dataclass, asdict
import logging
from pathlib import Path

# External libraries
import openai
import tiktoken
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('testcase_generator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class TokenUsage:
    """Token usage tracking"""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost_usd: float = 0.0

@dataclass
class UserQuota:
    """User quota management"""
    user_id: str
    daily_limit: int = 10000
    monthly_limit: int = 300000
    daily_used: int = 0
    monthly_used: int = 0
    last_reset_date: str = None

@dataclass
class AuditLog:
    """Audit log structure"""
    request_id: str
    user_id: str
    timestamp: str
    endpoint: str
    request_hash: str
    response_status: str
    token_usage: TokenUsage
    processing_time_ms: int
    was_cached: bool = False
    similarity_score: float = 0.0
    source: str = "openai"  # openai, cache, vector_db

class TestCaseGenerator:
    """
    Complete test case generator with OpenAI integration, caching, and vector similarity
    """
    
    def __init__(self, openai_api_key: str = None, data_dir: str = "./data"):
        """Initialize the test case generator"""
        
        # Setup directories
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # OpenAI setup
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            logger.warning("OpenAI API key not provided. Vector DB mode only.")
        else:
            openai.api_key = self.openai_api_key
            self.openai_client = openai.OpenAI(api_key=self.openai_api_key)
        
        # Token encoding for cost calculation
        try:
            self.encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        except:
            self.encoding = tiktoken.get_encoding("cl100k_base")
        
        # Initialize sentence transformer for similarity
        logger.info("Loading sentence transformer model...")
        self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize vector database
        self._init_vector_db()
        
        # Load or initialize data stores
        self._load_data_stores()
        
        # Pricing per 1K tokens (approximate)
        self.pricing = {
            "gpt-3.5-turbo": {"input": 0.001, "output": 0.002},
            "gpt-4": {"input": 0.03, "output": 0.06}
        }
    
    def _init_vector_db(self):
        """Initialize ChromaDB for vector storage"""
        try:
            self.chroma_client = chromadb.PersistentClient(
                path=str(self.data_dir / "chroma_db")
            )
            self.collection = self.chroma_client.get_or_create_collection(
                name="test_cases",
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("Vector database initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize vector DB: {e}")
            self.chroma_client = None
            self.collection = None
    
    def _load_data_stores(self):
        """Load or initialize data stores"""
        # Cache store
        self.cache_file = self.data_dir / "cache.json"
        self.cache = {}
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    self.cache = json.load(f)
            except:
                self.cache = {}
        
        # User quotas
        self.quota_file = self.data_dir / "quotas.json"
        self.quotas = {}
        if self.quota_file.exists():
            try:
                with open(self.quota_file, 'r') as f:
                    quota_data = json.load(f)
                    self.quotas = {k: UserQuota(**v) for k, v in quota_data.items()}
            except:
                self.quotas = {}
        
        # Audit logs
        self.audit_file = self.data_dir / "audit_logs.jsonl"
        if not self.audit_file.exists():
            self.audit_file.touch()
    
    def _save_data_stores(self):
        """Save data stores to disk"""
        # Save cache
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=2)
        
        # Save quotas
        quota_dict = {k: asdict(v) for k, v in self.quotas.items()}
        with open(self.quota_file, 'w') as f:
            json.dump(quota_dict, f, indent=2)
    
    def _generate_hash(self, text: str, params: Dict = None) -> str:
        """Generate hash for caching"""
        cache_data = {"text": text.strip().lower()}
        if params:
            cache_data.update(params)
        cache_string = json.dumps(cache_data, sort_keys=True)
        return hashlib.sha256(cache_string.encode()).hexdigest()
    
    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count"""
        return len(self.encoding.encode(text))
    
    def _calculate_cost(self, token_usage: TokenUsage, model: str) -> float:
        """Calculate cost based on token usage"""
        if model not in self.pricing:
            return 0.0
        
        pricing = self.pricing[model]
        input_cost = (token_usage.prompt_tokens / 1000) * pricing["input"]
        output_cost = (token_usage.completion_tokens / 1000) * pricing["output"]
        return input_cost + output_cost
    
    def _check_user_quota(self, user_id: str, estimated_tokens: int) -> bool:
        """Check if user has sufficient quota"""
        if user_id not in self.quotas:
            self.quotas[user_id] = UserQuota(user_id=user_id)
        
        quota = self.quotas[user_id]
        today = datetime.now().date().isoformat()
        
        # Reset daily quota if needed
        if quota.last_reset_date != today:
            quota.daily_used = 0
            quota.last_reset_date = today
        
        # Check limits
        if quota.daily_used + estimated_tokens > quota.daily_limit:
            return False
        if quota.monthly_used + estimated_tokens > quota.monthly_limit:
            return False
        
        return True
    
    def _update_user_quota(self, user_id: str, tokens_used: int):
        """Update user quota after successful request"""
        if user_id in self.quotas:
            self.quotas[user_id].daily_used += tokens_used
            self.quotas[user_id].monthly_used += tokens_used
            self._save_data_stores()
    
    def _log_audit(self, audit_log: AuditLog):
        """Log audit information"""
        with open(self.audit_file, 'a') as f:
            f.write(json.dumps(asdict(audit_log)) + '\n')
    
    def _find_similar_requirements(self, requirement: str, threshold: float = 0.8) -> Optional[Dict]:
        """Find similar requirements using vector similarity"""
        if not self.collection:
            return None
        
        try:
            # Generate embedding for the requirement
            embedding = self.sentence_model.encode([requirement]).tolist()[0]
            
            # Query similar documents
            results = self.collection.query(
                query_embeddings=[embedding],
                n_results=1
            )
            
            if results['documents'] and len(results['documents'][0]) > 0:
                similarity_score = 1 - results['distances'][0][0]  # Convert distance to similarity
                
                if similarity_score >= threshold:
                    return {
                        'requirement': results['documents'][0][0],
                        'test_cases': results['metadatas'][0][0]['test_cases'],
                        'similarity_score': similarity_score,
                        'id': results['ids'][0][0]
                    }
        except Exception as e:
            logger.error(f"Vector similarity search failed: {e}")
        
        return None
    
    def _store_in_vector_db(self, requirement: str, test_cases: str, request_id: str):
        """Store requirement and test cases in vector database"""
        if not self.collection:
            return
        
        try:
            embedding = self.sentence_model.encode([requirement]).tolist()[0]
            
            self.collection.add(
                embeddings=[embedding],
                documents=[requirement],
                metadatas=[{
                    'test_cases': test_cases,
                    'created_at': datetime.now().isoformat(),
                    'request_id': request_id
                }],
                ids=[request_id]
            )
            logger.info(f"Stored requirement in vector DB with ID: {request_id}")
        except Exception as e:
            logger.error(f"Failed to store in vector DB: {e}")
    
    def _call_openai_api(self, requirement: str, model: str = "gpt-3.5-turbo") -> Dict:
        """Make OpenAI API call"""
        if not self.openai_api_key:
            raise ValueError("OpenAI API key not available")
        
        prompt = f"""
        Generate comprehensive test cases for the following software requirement:

        Requirement: {requirement}

        Please provide test cases in the following JSON format:
        {{
            "test_cases": [
                {{
                    "id": 1,
                    "title": "Test case title",
                    "description": "Brief description",
                    "preconditions": "Prerequisites for the test",
                    "steps": [
                        "Step 1: Action to perform",
                        "Step 2: Next action",
                        "Step 3: Final action"
                    ],
                    "expected_result": "Expected outcome",
                    "priority": "High/Medium/Low",
                    "type": "Functional/UI/Integration/etc"
                }}
            ],
            "edge_cases": [
                {{
                    "scenario": "Edge case scenario",
                    "test_approach": "How to test this scenario"
                }}
            ]
        }}

        Focus on:
        1. Positive test cases (happy path)
        2. Negative test cases (error conditions)
        3. Edge cases and boundary conditions
        4. User experience considerations
        """

        try:
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a senior QA engineer specializing in comprehensive test case generation. Always respond with valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            return {
                'content': response.choices[0].message.content,
                'token_usage': TokenUsage(
                    prompt_tokens=response.usage.prompt_tokens,
                    completion_tokens=response.usage.completion_tokens,
                    total_tokens=response.usage.total_tokens
                ),
                'model': model
            }
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            raise
    
    def _generate_local_test_cases(self, requirement: str, similar_data: Dict) -> str:
        """Generate test cases based on similar existing data"""
        base_test_cases = similar_data['test_cases']
        
        # Simple template-based generation (can be enhanced)
        modified_cases = base_test_cases.replace(
            similar_data['requirement'].lower(),
            requirement.lower()
        )
        
        return modified_cases
    
    def generate_test_cases(self, requirement: str, user_id: str = "default_user", 
                          model: str = "gpt-3.5-turbo", use_vector_similarity: bool = True,
                          similarity_threshold: float = 0.8) -> Dict:
        """
        Main method to generate test cases with caching and vector similarity
        """
        request_id = str(uuid.uuid4())
        start_time = datetime.now()
        
        logger.info(f"Request {request_id}: Generating test cases for user {user_id}")
        
        # Generate cache key
        cache_params = {"model": model, "version": "1.0"}
        cache_key = self._generate_hash(requirement, cache_params)
        
        # Estimate tokens
        estimated_tokens = self._estimate_tokens(requirement) + 500  # Buffer for response
        
        # Check user quota
        if not self._check_user_quota(user_id, estimated_tokens):
            raise ValueError("User quota exceeded for today/month")
        
        # Check cache first
        if cache_key in self.cache:
            logger.info(f"Request {request_id}: Cache hit")
            cached_data = self.cache[cache_key]
            
            # Create audit log for cached response
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            audit_log = AuditLog(
                request_id=request_id,
                user_id=user_id,
                timestamp=datetime.now().isoformat(),
                endpoint="generate_test_cases",
                request_hash=cache_key,
                response_status="success",
                token_usage=TokenUsage(
                    prompt_tokens=cached_data.get('prompt_tokens', 0),
                    completion_tokens=cached_data.get('completion_tokens', 0),
                    total_tokens=cached_data.get('total_tokens', 0)
                ),
                processing_time_ms=int(processing_time),
                was_cached=True,
                source="cache"
            )
            self._log_audit(audit_log)
            
            return {
                'status': 'success',
                'test_cases': cached_data['test_cases'],
                'source': 'cache',
                'request_id': request_id,
                'cached': True,
                'token_usage': {
                    'prompt_tokens': cached_data.get('prompt_tokens', 0),
                    'completion_tokens': cached_data.get('completion_tokens', 0),
                    'total_tokens': cached_data.get('total_tokens', 0)
                }
            }
        
        # Check vector similarity if enabled
        if use_vector_similarity:
            similar_data = self._find_similar_requirements(requirement, similarity_threshold)
            if similar_data:
                logger.info(f"Request {request_id}: Vector similarity hit (score: {similar_data['similarity_score']:.3f})")
                
                # Generate test cases based on similar data
                test_cases = self._generate_local_test_cases(requirement, similar_data)
                
                # Create audit log
                processing_time = (datetime.now() - start_time).total_seconds() * 1000
                audit_log = AuditLog(
                    request_id=request_id,
                    user_id=user_id,
                    timestamp=datetime.now().isoformat(),
                    endpoint="generate_test_cases",
                    request_hash=cache_key,
                    response_status="success",
                    token_usage=TokenUsage(prompt_tokens=0, completion_tokens=0, total_tokens=0),
                    processing_time_ms=int(processing_time),
                    was_cached=False,
                    similarity_score=similar_data['similarity_score'],
                    source="vector_db"
                )
                self._log_audit(audit_log)
                
                return {
                    'status': 'success',
                    'test_cases': test_cases,
                    'source': 'vector_similarity',
                    'similarity_score': similar_data['similarity_score'],
                    'request_id': request_id,
                    'cached': False,
                    'similar_requirement': similar_data['requirement']
                }
        
        # Call OpenAI API if no cache/similarity hit
        if self.openai_api_key:
            logger.info(f"Request {request_id}: Calling OpenAI API")
            
            try:
                api_response = self._call_openai_api(requirement, model)
                test_cases = api_response['content']
                token_usage = api_response['token_usage']
                
                # Calculate cost
                cost = self._calculate_cost(token_usage, model)
                token_usage.cost_usd = cost
                
                # Update user quota
                self._update_user_quota(user_id, token_usage.total_tokens)
                
                # Cache the response
                self.cache[cache_key] = {
                    'test_cases': test_cases,
                    'prompt_tokens': token_usage.prompt_tokens,
                    'completion_tokens': token_usage.completion_tokens,
                    'total_tokens': token_usage.total_tokens,
                    'created_at': datetime.now().isoformat(),
                    'model': model
                }
                self._save_data_stores()
                
                # Store in vector database
                self._store_in_vector_db(requirement, test_cases, request_id)
                
                # Create audit log
                processing_time = (datetime.now() - start_time).total_seconds() * 1000
                audit_log = AuditLog(
                    request_id=request_id,
                    user_id=user_id,
                    timestamp=datetime.now().isoformat(),
                    endpoint="generate_test_cases",
                    request_hash=cache_key,
                    response_status="success",
                    token_usage=token_usage,
                    processing_time_ms=int(processing_time),
                    was_cached=False,
                    source="openai"
                )
                self._log_audit(audit_log)
                
                return {
                    'status': 'success',
                    'test_cases': test_cases,
                    'source': 'openai',
                    'request_id': request_id,
                    'cached': False,
                    'token_usage': asdict(token_usage),
                    'cost_usd': cost
                }
                
            except Exception as e:
                # Log failed request
                processing_time = (datetime.now() - start_time).total_seconds() * 1000
                audit_log = AuditLog(
                    request_id=request_id,
                    user_id=user_id,
                    timestamp=datetime.now().isoformat(),
                    endpoint="generate_test_cases",
                    request_hash=cache_key,
                    response_status="failed",
                    token_usage=TokenUsage(prompt_tokens=0, completion_tokens=0, total_tokens=0),
                    processing_time_ms=int(processing_time),
                    was_cached=False,
                    source="openai_failed"
                )
                self._log_audit(audit_log)
                
                raise Exception(f"Failed to generate test cases: {str(e)}")
        else:
            raise ValueError("No OpenAI API key available and no similar requirements found")
    
    def get_user_stats(self, user_id: str) -> Dict:
        """Get user statistics"""
        if user_id not in self.quotas:
            return {"error": "User not found"}
        
        quota = self.quotas[user_id]
        return {
            "user_id": user_id,
            "daily_quota": {
                "limit": quota.daily_limit,
                "used": quota.daily_used,
                "remaining": quota.daily_limit - quota.daily_used
            },
            "monthly_quota": {
                "limit": quota.monthly_limit,
                "used": quota.monthly_used,
                "remaining": quota.monthly_limit - quota.monthly_used
            }
        }
    
    def get_audit_summary(self, user_id: str = None, days: int = 7) -> List[Dict]:
        """Get audit log summary"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        logs = []
        try:
            with open(self.audit_file, 'r') as f:
                for line in f:
                    try:
                        log = json.loads(line.strip())
                        log_date = datetime.fromisoformat(log['timestamp'])
                        
                        if log_date >= cutoff_date:
                            if user_id is None or log['user_id'] == user_id:
                                logs.append(log)
                    except:
                        continue
        except FileNotFoundError:
            pass
        
        return logs
    
    def cleanup_cache(self, days_old: int = 30):
        """Clean up old cache entries"""
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        cleaned_count = 0
        for key, value in list(self.cache.items()):
            try:
                created_date = datetime.fromisoformat(value['created_at'])
                if created_date < cutoff_date:
                    del self.cache[key]
                    cleaned_count += 1
            except:
                # Remove entries without proper timestamp
                del self.cache[key]
                cleaned_count += 1
        
        if cleaned_count > 0:
            self._save_data_stores()
            logger.info(f"Cleaned up {cleaned_count} old cache entries")
        
        return cleaned_count


# Example usage and testing
def main():
    """Example usage of the TestCaseGenerator"""
    
    # Initialize generator (set your OpenAI API key in .env file or pass it directly)
    generator = TestCaseGenerator()
    
    # Example requirements
    test_requirements = [
        "User should be able to login with email and password",
        "System should validate user input for registration form",
        "User should be able to reset their password via email",
        "Application should handle file upload with size limits",
        "User login functionality with email and password validation"  # Similar to first one
    ]
    
    print("🚀 Test Case Generator - Froth TestOps")
    print("=" * 50)
    
    for i, requirement in enumerate(test_requirements, 1):
        print(f"\n📝 Test {i}: {requirement}")
        print("-" * 40)
        
        try:
            result = generator.generate_test_cases(
                requirement=requirement,
                user_id=f"user_{i}",
                similarity_threshold=0.7
            )
            
            print(f"✅ Status: {result['status']}")
            print(f"🔍 Source: {result['source']}")
            print(f"💰 Cached: {result.get('cached', False)}")
            
            if 'similarity_score' in result:
                print(f"🎯 Similarity Score: {result['similarity_score']:.3f}")
            
            if 'token_usage' in result:
                usage = result['token_usage']
                print(f"🪙 Tokens: {usage.get('total_tokens', 0)} (${result.get('cost_usd', 0):.4f})")
            
            # Print first few lines of test cases
            test_cases = result['test_cases']
            if len(test_cases) > 200:
                print(f"📋 Test Cases Preview:\n{test_cases[:200]}...")
            else:
                print(f"📋 Test Cases:\n{test_cases}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    # Show user statistics
    print("\n📊 User Statistics:")
    print("=" * 30)
    for user_id in ["user_1", "user_2"]:
        stats = generator.get_user_stats(user_id)
        if 'error' not in stats:
            daily = stats['daily_quota']
            print(f"{user_id}: {daily['used']}/{daily['limit']} tokens used today")
    
    # Show audit summary
    print("\n📜 Recent Audit Logs:")
    print("=" * 25)
    audit_logs = generator.get_audit_summary(days=1)
    for log in audit_logs[-3:]:  # Show last 3 logs
        print(f"User: {log['user_id']}, Source: {log['source']}, "
              f"Tokens: {log['token_usage']['total_tokens']}, "
              f"Time: {log['processing_time_ms']}ms")


if __name__ == "__main__":
    main()
