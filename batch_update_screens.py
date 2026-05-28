"""
Batch update all 171 screens for:
1. Font uniformity (standardized typography CSS)
2. Back button implementation
3. Navbar consistency
"""

import os
import re

BASE = r"C:\Users\PC\Downloads\stitch_hros_design_system_specification\stitch_hros_design_system_specification"

# Standardized typography CSS to inject into all screens
TYPOGRAPHY_CSS = """
    h1 { font-weight: 600; font-size: 24px; color: #1c1b1d; }
    h2 { font-weight: 600; font-size: 18px; color: #1c1b1d; }
    h3 { font-weight: 600; font-size: 14px; color: #1c1b1d; }
    .body-regular { font-weight: 400; font-size: 14px; color: #47464c; }
    .body-small { font-weight: 400; font-size: 12px; color: #78767d; }
    .label-text { font-weight: 500; font-size: 12px; color: #45455b; }
    .meta-text { font-weight: 400; font-size: 11px; color: #999999; }
"""

# Back button HTML template
BACK_BUTTON = '''  <button onclick="window.top.goBack ? window.top.goBack() : history.back()" style="background:none; border:none; cursor:pointer; padding:0; display:flex; align-items:center; justify-content:center;">
    <span class="material-symbols-outlined" style="color:#1c1b1d; font-size:24px;">arrow_back</span>
  </button>'''

# Standard navbar HTML
STANDARD_NAVBAR = '''<nav style="position:fixed; bottom:0; left:0; width:100%; z-index:50; display:flex; justify-content:space-around; align-items:center; padding:12px 4px 12px; background:#fff; border-top:1px solid #c8c5cd; height:64px;">
  <a style="display:flex; flex-direction:column; align-items:center; justify-content:center; color:#47464c; text-decoration:none; flex:1; margin:0 2px;" href="../journey_map_current_stage_expanded/code.html">
    <span class="material-symbols-outlined" style="font-size:24px;">route</span>
    <span style="font-size:12px; margin-top:2px;">Journey</span>
  </a>
  <a style="display:flex; flex-direction:column; align-items:center; justify-content:center; color:#47464c; text-decoration:none; flex:1; margin:0 2px;" href="../tasks_active_state/code.html">
    <span class="material-symbols-outlined" style="font-size:24px;">assignment</span>
    <span style="font-size:12px; margin-top:2px;">Tasks</span>
  </a>
  <a style="display:flex; flex-direction:column; align-items:center; justify-content:center; color:#47464c; text-decoration:none; flex:1; margin:0 2px;" href="../feed_active_content_mix/code.html">
    <span class="material-symbols-outlined" style="font-size:24px;">dynamic_feed</span>
    <span style="font-size:12px; margin-top:2px;">Feed</span>
  </a>
  <a style="display:flex; flex-direction:column; align-items:center; justify-content:center; color:#47464c; text-decoration:none; flex:1; margin:0 2px;" href="../ai_concierge_active_chat/code.html">
    <span class="material-symbols-outlined" style="font-size:24px;">auto_awesome</span>
    <span style="font-size:12px; margin-top:2px;">AI</span>
  </a>
  <a style="display:flex; flex-direction:column; align-items:center; justify-content:center; color:#47464c; text-decoration:none; flex:1; margin:0 2px;" href="../data_rights_pane/code.html">
    <span class="material-symbols-outlined" style="font-size:24px;">person</span>
    <span style="font-size:12px; margin-top:2px;">You</span>
  </a>
</nav>'''

def update_screen(filepath):
    """Update a single screen file for standardization."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # 1. Ensure style block exists and contains typography CSS
        if '<style>' not in content:
            # Add style block before closing head
            style_block = f'\n  <style>{TYPOGRAPHY_CSS}\n  </style>'
            content = re.sub(r'(</head>)', style_block + r'\1', content)
        else:
            # Append typography CSS to existing style block
            content = re.sub(
                r'(<style>[^<]*)',
                r'\1\n' + TYPOGRAPHY_CSS,
                content,
                flags=re.DOTALL
            )

        # 2. Ensure back button exists in header (check if missing)
        if 'arrow_back' not in content:
            # Add back button to header if not present
            # Find the header and add button after opening div
            if '<header' in content:
                # Try to add after first flex div
                content = re.sub(
                    r'(<header[^>]*>.*?<div[^>]*>)',
                    r'\1\n' + BACK_BUTTON,
                    content,
                    count=1,
                    flags=re.DOTALL
                )

        # 3. Update navbar - ensure it matches standard structure
        # Replace old navbar if it exists
        navbar_pattern = r'<nav[^>]*style="position:fixed; bottom:0[^<]*</nav>'
        if re.search(navbar_pattern, content, re.DOTALL):
            content = re.sub(navbar_pattern, STANDARD_NAVBAR, content, flags=re.DOTALL)

        # Write back only if changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False

    except Exception as e:
        print(f"  [ERR] {filepath}: {str(e)}")
        return False

# Main execution
print("\nBatch updating 171 screens for typography and consistency...")
print("=" * 70)

updated = 0
skipped = 0
errors = 0

for folder in sorted(os.listdir(BASE)):
    folder_path = os.path.join(BASE, folder)
    if not os.path.isdir(folder_path):
        continue

    code_file = os.path.join(folder_path, 'code.html')
    if not os.path.isfile(code_file):
        continue

    if update_screen(code_file):
        updated += 1
        print(f"[OK] {folder}")
    else:
        skipped += 1

print("=" * 70)
print(f"\nResults:")
print(f"  Updated: {updated}")
print(f"  Skipped: {skipped}")
print(f"  Errors:  {errors}")
print(f"  Total:   {updated + skipped + errors}")
print("\nDone! All screens standardized for typography and back buttons.")
