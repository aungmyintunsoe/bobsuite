import time

def initialize_bob(api_key, project_id):
    if not api_key or not project_id:
        raise ValueError('API key and Project ID are required.')
    return {'api_key': api_key, 'project_id': project_id, 'session_start': time.time()}

def route_request(user_input, context):
    if any(w in user_input.lower() for w in ['bug', 'fix', 'error']):
        return 'qa_sentry'
    elif any(w in user_input.lower() for w in ['doc', 'readme']):
        return 'doc_engine'
    elif any(w in user_input.lower() for w in ['plan', 'feature']):
        return 'ideation'
    return 'doc_engine'

def format_bob_response(tool, result, duration_ms):
    return {'tool': tool, 'result': result, 'duration_ms': duration_ms}

def check_session_validity(context, max_age=3600):
    return time.time() - context.get('session_start', 0) < max_age
