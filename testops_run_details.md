(venv) pritish@ymax-hw-0005 TestOps % python3.11 rd_froth_testops.py 
2025-08-20 13:18:25,699 - __main__ - INFO - Loading sentence transformer model...
2025-08-20 13:18:25,720 - sentence_transformers.SentenceTransformer - INFO - Use pytorch device_name: mps
2025-08-20 13:18:25,720 - sentence_transformers.SentenceTransformer - INFO - Load pretrained SentenceTransformer: all-MiniLM-L6-v2
2025-08-20 13:18:29,451 - chromadb.telemetry.product.posthog - INFO - Anonymized telemetry enabled. See                     https://docs.trychroma.com/telemetry for more information.
2025-08-20 13:18:30,039 - __main__ - INFO - Vector database initialized successfully
🚀 Test Case Generator - Froth TestOps
==================================================

📝 Test 1: User should be able to login with email and password
----------------------------------------
2025-08-20 13:18:30,039 - __main__ - INFO - Request 07742f77-cb71-43d2-ac28-5a2193f8850c: Generating test cases for user user_1
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:01<00:00,  1.57s/it]
2025-08-20 13:18:31,625 - __main__ - INFO - Request 07742f77-cb71-43d2-ac28-5a2193f8850c: Calling OpenAI API
huggingface/tokenizers: The current process just got forked, after parallelism has already been used. Disabling parallelism to avoid deadlocks...
To disable this warning, you can either:
	- Avoid using `tokenizers` before the fork if possible
	- Explicitly set the environment variable TOKENIZERS_PARALLELISM=(true | false)
huggingface/tokenizers: The current process just got forked, after parallelism has already been used. Disabling parallelism to avoid deadlocks...
To disable this warning, you can either:
	- Avoid using `tokenizers` before the fork if possible
	- Explicitly set the environment variable TOKENIZERS_PARALLELISM=(true | false)
2025-08-20 13:18:35,316 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 17.88it/s]
2025-08-20 13:18:35,417 - __main__ - INFO - Stored requirement in vector DB with ID: 07742f77-cb71-43d2-ac28-5a2193f8850c
✅ Status: success
🔍 Source: openai
💰 Cached: False
🪙 Tokens: 710 ($0.0012)
📋 Test Cases Preview:
{
    "test_cases": [
        {
            "id": 1,
            "title": "Valid login with correct email and password",
            "description": "User tries to login with valid email and password",...

📝 Test 2: System should validate user input for registration form
----------------------------------------
2025-08-20 13:18:35,417 - __main__ - INFO - Request 157de1b9-e4d0-4aaf-98c3-a8ad1a3c172a: Generating test cases for user user_2
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  2.81it/s]
2025-08-20 13:18:35,775 - __main__ - INFO - Request 157de1b9-e4d0-4aaf-98c3-a8ad1a3c172a: Calling OpenAI API
2025-08-20 13:18:46,877 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 20.09it/s]
2025-08-20 13:18:46,945 - __main__ - INFO - Stored requirement in vector DB with ID: 157de1b9-e4d0-4aaf-98c3-a8ad1a3c172a
✅ Status: success
🔍 Source: openai
💰 Cached: False
🪙 Tokens: 713 ($0.0012)
📋 Test Cases Preview:
{
    "test_cases": [
        {
            "id": 1,
            "title": "Valid user registration",
            "description": "Verify user input validation for a successful registration",
          ...

📝 Test 3: User should be able to reset their password via email
----------------------------------------
2025-08-20 13:18:46,945 - __main__ - INFO - Request 174d4411-9d9c-47bf-825f-7d45024b984e: Generating test cases for user user_3
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  3.17it/s]
2025-08-20 13:18:47,262 - __main__ - INFO - Request 174d4411-9d9c-47bf-825f-7d45024b984e: Vector similarity hit (score: 0.811)
✅ Status: success
🔍 Source: vector_similarity
💰 Cached: False
🎯 Similarity Score: 0.811
📋 Test Cases Preview:
{
    "test_cases": [
        {
            "id": 1,
            "title": "Valid login with correct email and password",
            "description": "User tries to login with valid email and password",...

📝 Test 4: Application should handle file upload with size limits
----------------------------------------
2025-08-20 13:18:47,263 - __main__ - INFO - Request 32adea7e-f201-4ac4-a782-cd8bf3be6596: Generating test cases for user user_4
Batches: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 178.67it/s]
2025-08-20 13:18:47,270 - __main__ - INFO - Request 32adea7e-f201-4ac4-a782-cd8bf3be6596: Calling OpenAI API
2025-08-20 13:18:49,921 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 20.69it/s]
2025-08-20 13:18:49,980 - __main__ - INFO - Stored requirement in vector DB with ID: 32adea7e-f201-4ac4-a782-cd8bf3be6596
✅ Status: success
🔍 Source: openai
💰 Cached: False
🪙 Tokens: 633 ($0.0010)
📋 Test Cases Preview:
{
    "test_cases": [
        {
            "id": 1,
            "title": "Upload file within size limit",
            "description": "Verify that the application allows uploading a file within the sp...

📝 Test 5: User login functionality with email and password validation
----------------------------------------
2025-08-20 13:18:49,981 - __main__ - INFO - Request 0fda9ef9-1890-4f53-bea4-d26b5452240b: Generating test cases for user user_5
Batches: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 116.27it/s]
2025-08-20 13:18:49,991 - __main__ - INFO - Request 0fda9ef9-1890-4f53-bea4-d26b5452240b: Vector similarity hit (score: 0.779)
✅ Status: success
🔍 Source: vector_similarity
💰 Cached: False
🎯 Similarity Score: 0.779
📋 Test Cases Preview:
{
    "test_cases": [
        {
            "id": 1,
            "title": "Valid login with correct email and password",
            "description": "User tries to login with valid email and password",...

📊 User Statistics:
==============================
user_1: 710/10000 tokens used today
user_2: 713/10000 tokens used today

📜 Recent Audit Logs:
=========================
User: user_3, Source: vector_db, Tokens: 0, Time: 317ms
User: user_4, Source: openai, Tokens: 633, Time: 2717ms
User: user_5, Source: vector_db, Tokens: 0, Time: 10ms
(venv) pritish@ymax-hw-0005 TestOps % 
(venv) pritish@ymax-hw-0005 TestOps % python3.11 rd_froth_testops.py
2025-08-20 13:20:51,748 - __main__ - INFO - Loading sentence transformer model...
2025-08-20 13:20:51,761 - sentence_transformers.SentenceTransformer - INFO - Use pytorch device_name: mps
2025-08-20 13:20:51,761 - sentence_transformers.SentenceTransformer - INFO - Load pretrained SentenceTransformer: all-MiniLM-L6-v2
2025-08-20 13:20:58,713 - chromadb.telemetry.product.posthog - INFO - Anonymized telemetry enabled. See                     https://docs.trychroma.com/telemetry for more information.
2025-08-20 13:20:58,779 - __main__ - INFO - Vector database initialized successfully
🚀 Test Case Generator - Froth TestOps
==================================================

📝 Test 1: User should be able to login with email and password
----------------------------------------
2025-08-20 13:20:58,780 - __main__ - INFO - Request 812b175f-d111-45e0-a02f-2d52a40d0ba1: Generating test cases for user user_1
2025-08-20 13:20:58,780 - __main__ - INFO - Request 812b175f-d111-45e0-a02f-2d52a40d0ba1: Cache hit
✅ Status: success
🔍 Source: cache
💰 Cached: True
🪙 Tokens: 710 ($0.0000)
📋 Test Cases Preview:
{
    "test_cases": [
        {
            "id": 1,
            "title": "Valid login with correct email and password",
            "description": "User tries to login with valid email and password",...

📝 Test 2: System should validate user input for registration form
----------------------------------------
2025-08-20 13:20:58,781 - __main__ - INFO - Request 4ea7b394-736c-41f2-a2ca-0cddc73e9138: Generating test cases for user user_2
2025-08-20 13:20:58,781 - __main__ - INFO - Request 4ea7b394-736c-41f2-a2ca-0cddc73e9138: Cache hit
✅ Status: success
🔍 Source: cache
💰 Cached: True
🪙 Tokens: 713 ($0.0000)
📋 Test Cases Preview:
{
    "test_cases": [
        {
            "id": 1,
            "title": "Valid user registration",
            "description": "Verify user input validation for a successful registration",
          ...

📝 Test 3: User should be able to reset their password via email
----------------------------------------
2025-08-20 13:20:58,781 - __main__ - INFO - Request 88f32ef7-28a4-4024-8c43-c0f75cef88c7: Generating test cases for user user_3
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  6.42it/s]
2025-08-20 13:20:58,969 - __main__ - INFO - Request 88f32ef7-28a4-4024-8c43-c0f75cef88c7: Vector similarity hit (score: 0.811)
✅ Status: success
🔍 Source: vector_similarity
💰 Cached: False
🎯 Similarity Score: 0.811
📋 Test Cases Preview:
{
    "test_cases": [
        {
            "id": 1,
            "title": "Valid login with correct email and password",
            "description": "User tries to login with valid email and password",...

📝 Test 4: Application should handle file upload with size limits
----------------------------------------
2025-08-20 13:20:58,969 - __main__ - INFO - Request af1cc346-a3b2-466f-aee7-993abf8f1a3a: Generating test cases for user user_4
2025-08-20 13:20:58,970 - __main__ - INFO - Request af1cc346-a3b2-466f-aee7-993abf8f1a3a: Cache hit
✅ Status: success
🔍 Source: cache
💰 Cached: True
🪙 Tokens: 633 ($0.0000)
📋 Test Cases Preview:
{
    "test_cases": [
        {
            "id": 1,
            "title": "Upload file within size limit",
            "description": "Verify that the application allows uploading a file within the sp...

📝 Test 5: User login functionality with email and password validation
----------------------------------------
2025-08-20 13:20:58,970 - __main__ - INFO - Request 2c43e5f6-16cb-4d36-8bb1-a852f46365a5: Generating test cases for user user_5
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 39.05it/s]
2025-08-20 13:20:58,997 - __main__ - INFO - Request 2c43e5f6-16cb-4d36-8bb1-a852f46365a5: Vector similarity hit (score: 0.779)
✅ Status: success
🔍 Source: vector_similarity
💰 Cached: False
🎯 Similarity Score: 0.779
📋 Test Cases Preview:
{
    "test_cases": [
        {
            "id": 1,
            "title": "Valid login with correct email and password",
            "description": "User tries to login with valid email and password",...

📊 User Statistics:
==============================
user_1: 710/10000 tokens used today
user_2: 713/10000 tokens used today

📜 Recent Audit Logs:
=========================
User: user_3, Source: vector_db, Tokens: 0, Time: 188ms
User: user_4, Source: cache, Tokens: 633, Time: 0ms
User: user_5, Source: vector_db, Tokens: 0, Time: 27ms
(venv) pritish@ymax-hw-0005 TestOps % .
.: not enough arguments
