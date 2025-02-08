import re
from typing import List, Dict

def analyze_naming_conventions(line: str, line_num: int) -> List[Dict]:
    """Check Java naming conventions"""
    issues = []
    
    # Check package names (lowercase)
    if re.search(r'package\s+[A-Z]', line):
        issues.append({
            'line': line_num,
            'type': 'naming_convention',
            'description': 'Package names should be lowercase'
        })
    
    # Check class names (PascalCase)
    if re.search(r'class\s+[a-z]', line):
        issues.append({
            'line': line_num,
            'type': 'naming_convention',
            'description': 'Class names should start with uppercase letter (PascalCase)'
        })
    
    # Check constant names (UPPER_CASE)
    if re.search(r'static\s+final\s+[a-z]', line):
        issues.append({
            'line': line_num,
            'type': 'naming_convention',
            'description': 'Constants should be in UPPER_CASE'
        })
    
    # Check variable names (camelCase)
    if re.search(r'(?:private|protected|public).*?[A-Z][\w\s=;]', line) and 'class' not in line:
        issues.append({
            'line': line_num,
            'type': 'naming_convention',
            'description': 'Variable names should be in camelCase'
        })
    
    return issues

def analyze_streams_usage(code: str, line_num: int) -> List[Dict]:
    """Check for opportunities to use streams and lambdas"""
    issues = []
    
    # Check for traditional for loops that could use streams
    if re.search(r'for\s*\([^\)]+\)', code):
        if re.search(r'if.*?add|if.*?collect|if.*?filter', code, re.DOTALL):
            issues.append({
                'line': line_num,
                'type': 'streams_and_lambdas',
                'description': 'Consider using Stream API with filter() instead of traditional for loop'
            })
    
    return issues

def analyze_null_handling(code: str, line_num: int) -> List[Dict]:
    """Check null handling practices"""
    issues = []
    
    # Check for null returns
    if 'return null' in code:
        issues.append({
            'line': line_num,
            'type': 'null_handling',
            'description': 'Consider using Optional instead of returning null'
        })
    
    # Check for null checks without Optional
    if ('!= null' in code or '== null' in code) and 'Optional' not in code:
        issues.append({
            'line': line_num,
            'type': 'null_handling',
            'description': 'Consider using Optional for null checking'
        })
    
    # Check for missing @Nullable/@NonNull annotations
    if 'null' in code and not any(annotation in code for annotation in ['@Nullable', '@NonNull']):
        issues.append({
            'line': line_num,
            'type': 'null_handling',
            'description': 'Consider adding @Nullable or @NonNull annotations'
        })
    
    return issues

def analyze_reference_handling(code: str, line_num: int) -> List[Dict]:
    """Check reference handling and mutable state"""
    issues = []
    
    # Check for direct reference assignment in constructors
    if re.search(r'this\.[a-zA-Z]+\s*=\s*[a-zA-Z]+\s*;', code) and 'new' not in code:
        if re.search(r'List|Set|Map|Collection', code):
            issues.append({
                'line': line_num,
                'type': 'reference_handling',
                'description': 'Create defensive copy when assigning collection references'
            })
    
    # Check for exposed mutable state
    if re.search(r'public.*?get.*?List|public.*?get.*?Set|public.*?get.*?Map', code):
        issues.append({
            'line': line_num,
            'type': 'reference_handling',
            'description': 'Avoid exposing internal mutable state, return defensive copy'
        })
    
    return issues

def analyze_exception_handling(code: str, line_num: int) -> List[Dict]:
    """Check exception handling practices"""
    issues = []
    
    # Check catch block order
    if 'catch (Exception' in code:
        next_lines = code[code.find('catch (Exception'):].split('\n', 5)[0]
        if re.search(r'catch \([A-Za-z]+Exception', next_lines):
            issues.append({
                'line': line_num,
                'type': 'exception_handling',
                'description': 'Catch more specific exceptions before general Exception'
            })
    
    # Check for empty catch blocks
    if re.search(r'catch.*?\{\s*\}', code, re.DOTALL):
        issues.append({
            'line': line_num,
            'type': 'exception_handling',
            'description': 'Avoid empty catch blocks'
        })
    
    return issues

def analyze_data_structures(code: str, line_num: int) -> List[Dict]:
    """Check appropriate use of data structures"""
    issues = []
    
    # Check for Vector usage
    if 'Vector' in code:
        issues.append({
            'line': line_num,
            'type': 'data_structures',
            'description': 'Consider using ArrayList with Collections.synchronizedList instead of Vector'
        })
    
    # Check for concrete implementation instead of interfaces
    for impl in ['ArrayList', 'LinkedList', 'HashSet', 'HashMap']:
        if f'new {impl}' in code and not re.search(rf'{impl}\s*<', code):
            issues.append({
                'line': line_num,
                'type': 'data_structures',
                'description': f'Use interface type instead of concrete {impl} implementation'
            })
    
    return issues

def analyze_access_modifiers(code: str, line_num: int) -> List[Dict]:
    """Check appropriate use of access modifiers"""
    issues = []
    
    # Check for public methods that might be private
    if re.search(r'public\s+\w+\s+\w+\s*\([^\)]*\)', code) and not any(x in code for x in ['@Override', '@Test', 'interface', 'abstract']):
        issues.append({
            'line': line_num,
            'type': 'access_modifiers',
            'description': 'Consider using more restrictive access modifier'
        })
    
    return issues

def analyze_interfaces(code: str, line_num: int) -> List[Dict]:
    """Check interface design"""
    issues = []
    
    # Check for single implementation interfaces
    if 'interface' in code:
        interface_name = re.search(r'interface\s+(\w+)', code)
        if interface_name and re.search(rf'class\s+\w+\s+implements\s+{interface_name.group(1)}\s*{{', code):
            issues.append({
                'line': line_num,
                'type': 'interface_design',
                'description': 'Verify if this interface is necessary or could be simplified'
            })
    
    return issues

def analyze_equals_hashcode(code: str, line_num: int) -> List[Dict]:
    """Check equals and hashCode implementation"""
    issues = []
    
    # Check if equals is overridden without hashCode
    if '@Override' in code and 'equals' in code and 'hashCode' not in code:
        issues.append({
            'line': line_num,
            'type': 'equals_hashcode',
            'description': 'Override hashCode method when overriding equals'
        })
    
    return issues

def analyze_code(file_content: str) -> List[Dict]:
    """
    Analyze Java code for potential issues based on guidelines
    
    Args:
        file_content: Content of Java file
    
    Returns:
        List of issues found with line numbers and descriptions
    """
    issues = []
    lines = file_content.split('\n')
    
    # Analyze code block by block
    for line_num, line in enumerate(lines, 1):
        # Get context (few lines before and after for better analysis)
        start = max(0, line_num - 3)
        end = min(len(lines), line_num + 3)
        context = '\n'.join(lines[start:end])
        
        # Run all analyses
        issues.extend(analyze_naming_conventions(line, line_num))
        issues.extend(analyze_streams_usage(context, line_num))
        issues.extend(analyze_null_handling(context, line_num))
        issues.extend(analyze_reference_handling(context, line_num))
        issues.extend(analyze_exception_handling(context, line_num))
        issues.extend(analyze_data_structures(context, line_num))
        issues.extend(analyze_access_modifiers(context, line_num))
        issues.extend(analyze_interfaces(context, line_num))
        issues.extend(analyze_equals_hashcode(context, line_num))
    
    return issues