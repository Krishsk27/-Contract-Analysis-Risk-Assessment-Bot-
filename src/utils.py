import re

def highlight_text(full_text, clauses):
    """
    Takes the full contract text and the list of risky clauses.
    Wraps the risky 'original_text' in HTML <mark> tags for highlighting.
    """
    # 1. Preserve line breaks for HTML rendering
    # We replace newlines with <br> placeholders, then do text replacement, then finalize HTML
    html_text = full_text.replace("\n", "<br>")
    
    # 2. Iterate through analyzed clauses
    for clause in clauses:
        original = clause.get('original_text', '').strip()
        risk_level = clause.get('risk_level', 'Low')
        explanation = clause.get('explanation', '')
        
        if not original or len(original) < 10:
            continue
            
        # Define Color Logic
        if risk_level == "High":
            color = "#ffcdd2" # Light Red
            border = "2px solid #e53935"
        elif risk_level == "Medium":
            color = "#ffe0b2" # Light Orange
            border = "2px solid #fb8c00"
        else:
            continue # Don't highlight Low risk to keep it clean

        # 3. Create the Highlight HTML span with a Tooltip (title attribute)
        # We use a simple Replace, but in production, fuzzy matching is better.
        highlight_html = f"""
        <span style="background-color: {color}; border-bottom: {border}; cursor: help;" title="{explanation}">
            {original}
        </span>
        """
        
        # 4. Replace the text
        # Escape special regex characters to avoid crashing on symbols like $ or ()
        try:
            # Simple string replace is safer than regex for exact matches
            html_text = html_text.replace(original, highlight_html)
        except Exception:
            continue

    # Wrap in a readable container
    final_html = f"""
    <div style="
        font-family: 'Arial', sans-serif; 
        font-size: 14px; 
        line-height: 1.6; 
        background-color: #f9f9f9; 
        padding: 20px; 
        border-radius: 10px; 
        border: 1px solid #ddd;
        height: 600px; 
        overflow-y: scroll;">
        {html_text}
    </div>
    """
    return final_html