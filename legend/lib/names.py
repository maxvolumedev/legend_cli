import re
import uuid


def normalize_name(name: str) -> str:
    """Normalize app name: lowercase and replace underscores with hyphens"""
    return name.lower().replace('_', '-')

def generate_short_name(name: str, max_len: int = 24) -> str:
    """Generate a meaningful short name from a longer name.
    
    Strategy:
    1. Split into words
    2. For common words (api, service, etc), use standard abbreviations
    3. For other words:
       - Keep first letter
       - Keep consonants after first letter (to maintain readability)
       - Keep numbers
    4. Join and truncate to max_len
    
    Examples:
        'customer-service-api' -> 'cstapi'
        'payment-processing-service' -> 'pmtprcsvc'
        'rta-customer-adapter' -> 'rtacstadp'
    """
    # Common word mappings by category
    abbreviations = {
        # Service types
        'service': 'svc',
        'api': 'api',
        'application': 'app',
        'adapter': 'adp',
        'integration': 'int',
        'interface': 'intf',
        'gateway': 'gw',
        'proxy': 'prx',
        'server': 'srv',
        'client': 'cli',
        'worker': 'wkr',
        'daemon': 'dmn',
        'scheduler': 'sch',
        'processor': 'prc',
        'handler': 'hdlr',
        'listener': 'lsnr',
        'monitor': 'mon',
        'controller': 'ctrl',
        'middleware': 'mw',
        
        # Business domains
        'customer': 'cst',
        'payment': 'pmt',
        'account': 'acc',
        'transaction': 'trx',
        'order': 'ord',
        'invoice': 'inv',
        'product': 'prod',
        'inventory': 'inv',
        'catalog': 'cat',
        'document': 'doc',
        'message': 'msg',
        'notification': 'notif',
        'analytics': 'anly',
        'reporting': 'rpt',
        'billing': 'bill',
        'shipping': 'ship',
        'tracking': 'trk',
        'marketing': 'mkt',
        'authentication': 'auth',
        'authorization': 'authz',
        
        # Operations
        'manager': 'mgr',
        'processing': 'prc',
        'generator': 'gen',
        'validator': 'val',
        'converter': 'conv',
        'transformer': 'trf',
        'calculator': 'calc',
        'formatter': 'fmt',
        'publisher': 'pub',
        'subscriber': 'sub',
        'synchronizer': 'sync',
        'orchestrator': 'orch',
        
        # Data related
        'database': 'db',
        'repository': 'repo',
        'storage': 'store',
        'cache': 'cache',
        'queue': 'q',
        'stream': 'strm',
        'event': 'evt',
        'config': 'cfg',
        'settings': 'set',
        'metadata': 'meta',
        
        # Environments
        'development': 'dev',
        'production': 'prod',
        'test': 'test',
        'staging': 'stg',
        'sandbox': 'sbx',
        'quality': 'qa',
        'acceptance': 'uat',
        'integration': 'int',
        'preview': 'prev',
        'performance': 'perf',
        
        # Common prefixes/suffixes
        'internal': 'int',
        'external': 'ext',
        'public': 'pub',
        'private': 'prv',
        'shared': 'shd',
        'common': 'cmn',
        'core': 'core',
        'legacy': 'leg',
        'utility': 'util',
        'helper': 'hlpr',
        'wrapper': 'wrap',
        'engine': 'eng',
        'system': 'sys',
    }
    
    # Split into words
    words = name.lower().replace('_', '-').split('-')
    result = []
    
    for word in words:
        # Check if we have a standard abbreviation
        if word in abbreviations:
            result.append(abbreviations[word])
        else:
            # Keep first letter
            shortened = word[0]
            
            # Keep consonants and numbers after first letter
            consonants = ''.join(c for c in word[1:] 
                                if c.isdigit() or (c.isalpha() and c not in 'aeiou'))
            shortened += consonants[:2]  # Limit to 2 consonants for consistency
            
            result.append(shortened)
    
    # Join and ensure we don't exceed max_len
    return ''.join(result)[:max_len]

def pad_with_uuid(name: str, max_len: int = 24) -> str:
    """Pad a string with part of a UUID to reach max_len.
    Only uses the minimum number of UUID characters needed.
    Example: 'myapp' -> 'myapp1a2b3' (not the full UUID)
    """
    if len(name) >= max_len:
        return name[:max_len]
    
    # Only use as many UUID chars as needed to reach max_len
    needed_length = max_len - len(name)
    uid = str(uuid.uuid4()).replace('-', '')[:needed_length]
    return name + uid

def get_storage_name(app_name: str, env: str) -> str:
    """Generate storage account name: shortened app name + env + optional uuid suffix, max 24 chars.
    Must be 3-24 characters, lowercase letters and numbers only.
    Will be padded with UUID to ensure global uniqueness.
    """
    short_name = generate_short_name(app_name, max_len=20)  # Leave room for env
    name = f"{short_name}{env}"
    # Remove any non-alphanumeric characters and convert to lowercase
    name = re.sub(r'[^a-z0-9]', '', name.lower())
    # Ensure minimum length of 3
    if len(name) < 3:
        name = name + 'x' * (3 - len(name))
    # Pad with UUID to ensure uniqueness
    return pad_with_uuid(name, 24)

def get_keyvault_name(app_name: str, env: str) -> str:
    """Generate key vault name: shortened app name + env + kv + optional uuid suffix, max 24 chars.
    Must be 3-24 characters, lowercase letters, numbers, and hyphens.
    Hyphens cannot be consecutive or at start/end.
    Will be padded with UUID to ensure global uniqueness.
    """
    short_name = generate_short_name(app_name, max_len=19)  # Leave room for env and 'kv'
    name = f"{short_name}{env}kv"
    # Remove any characters not allowed in key vault names
    name = re.sub(r'[^a-z0-9-]', '', name.lower())
    # Remove consecutive hyphens
    name = re.sub(r'-+', '-', name)
    # Remove leading/trailing hyphens
    name = name.strip('-')
    # Ensure minimum length of 3
    if len(name) < 3:
        name = name + 'x' * (3 - len(name))
    # Pad with UUID to ensure uniqueness
    return pad_with_uuid(name, 24)
