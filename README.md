# HROS Prototype — Linear Onboarding Redesign

Welcome to the redesigned HROS (HR Operating System) mobile onboarding prototype. This prototype features a linear onboarding flow with priority-based task management, consolidated content, and consistent typography throughout.

---

## Quick Start

### 1. Open the Prototype

Simply double-click or open in your browser:
```
hros_prototype.html
```

The prototype will load in your default browser with:
- Scenario sidebar on the left (showing all available flows)
- Main content area on the right showing the selected screen
- Full navigation between all 171 screens

### 2. Start Testing

**Recommended first test:**
1. In the sidebar, find "**Offer Acceptance**" section
2. Click the "**Normal**" flow
3. Follow the onboarding sequence: Offer → Joining Date → Acceptance → Tasks
4. Test the Tasks page tabs, navigation, and new flows

For comprehensive testing, follow: **[TESTING_GUIDE.md](./TESTING_GUIDE.md)**

---

## What's New

### ✨ Major Changes
- **Linear Onboarding Flow:** From offer acceptance through appointment letter signing
- **Redesigned Tasks Page:** Priority categorization with red/yellow alerts and progress tracking
- **Consolidated Feed:** All content on one unified page
- **Enhanced Profile:** Updated with new 4-tab navbar
- **4 New Screens:**
  - In-Hand Salary Calculator
  - ESOP Explainer
  - Joining Date Alternate Picker (with approval workflow)
  - Vendor Consent Employee Type Selector
- **Font Standardization:** Geist sans-serif throughout (227 explicit declarations)
- **Improved Navigation:** Fixed back buttons, proper tab highlighting, localStorage persistence

For detailed changes, see: **[CHANGES_SUMMARY.md](./CHANGES_SUMMARY.md)**

---

## File Structure

```
stitch_hros_design_system_specification/
│
├── hros_prototype.html                 ← MAIN FILE (3.1 MB)
│                                         All 171 screens embedded
│
├── README.md                           ← This file
├── TESTING_GUIDE.md                    ← Comprehensive test checklist
├── CHANGES_SUMMARY.md                  ← Detailed changelog
│
├── stitch_hros_design_system_specification/  ← All screen files
│   ├── tasks_active_state/
│   │   └── code.html                   ← Redesigned with priority tabs
│   ├── feed_active_content_mix/
│   │   └── code.html                   ← Consolidated single page
│   ├── data_rights_pane/
│   │   └── code.html                   ← Updated navbar
│   ├── in_hand_calculator/
│   │   └── code.html                   ← NEW: Salary calculator
│   ├── esop_explainer/
│   │   └── code.html                   ← NEW: ESOP education
│   ├── joining_date_alternate_date_picker/
│   │   └── code.html                   ← NEW: Date selection
│   ├── vendor_consent_employee_type_selector/
│   │   └── code.html                   ← NEW: Employment type gating
│   ├── [165 other screens...]
│   ├── build_single.py                 ← Build script
│   ├── trace_flows.py                  ← Flow mappings & sidebar
│   └── nav.js                          ← Navigation utilities
│
└── [other supporting files]
```

---

## Local Testing

### Method 1: Direct Browser (Simplest)
```bash
# Windows
start hros_prototype.html

# Mac
open hros_prototype.html

# Linux
xdg-open hros_prototype.html
```

### Method 2: Local HTTP Server (If Direct Fails)
```bash
# Navigate to the directory
cd "C:\Users\PC\Downloads\stitch_hros_design_system_specification"

# Start Python HTTP server
python -m http.server 8000

# Open in browser
http://localhost:8000/hros_prototype.html
```

### Method 3: Live Server (If Using VS Code)
```bash
# Install Live Server extension in VS Code
# Right-click hros_prototype.html
# Select "Open with Live Server"
```

---

## Testing Checklist

✅ **Quick Test (5 minutes):**
1. Open prototype
2. Click "Normal" flow under "Offer Acceptance"
3. Click "Accept this offer"
4. Confirm joining date
5. Click through to Tasks page
6. Check Tasks page shows 4 tabs with correct alerts
7. Verify Geist sans-serif font (not system fonts)

✅ **Standard Test (20 minutes):**
- Follow all core flows
- Test alternate date rejection/approval
- Test new screens (calculator, ESOP, vendor consent)
- Verify navigation between 4 main tabs
- Check back button functionality

✅ **Complete Test (45 minutes):**
- See: **[TESTING_GUIDE.md](./TESTING_GUIDE.md)** for full checklist

---

## Known Working Features

✅ **Core Flows:**
- Offer → Joining Date → Acceptance → Tasks
- Alternate date request with approval workflow
- Vendor consent gated by employment type
- Tax setup linear flow

✅ **Tasks Page:**
- 4 tabs (Priority Now, Before Joining, Post-Joining, Optional)
- Red/yellow alert badges
- Checkbox-based completion tracking
- Progress rings show completion percentage
- localStorage persistence (data saved across page refreshes)

✅ **Navigation:**
- Bottom navbar: Tasks, Feed, Journey, Profile
- Back button returns to appropriate screen
- Floating AI button on Tasks page
- Tab highlighting shows active page

✅ **Typography:**
- Geist sans-serif applied throughout
- Consistent font weights and sizes
- All Material Symbols render correctly

---

## Common Issues & Solutions

### Issue: Prototype won't open
**Solution:** 
- Make sure you're opening `hros_prototype.html` (not a folder)
- Try: Right-click → Open With → Choose Browser
- Alternative: Use local HTTP server method above

### Issue: Fonts look wrong (Arial/Helvetica instead of Geist)
**Solution:**
- Clear browser cache (Ctrl+Shift+Delete)
- Hard refresh (Ctrl+Shift+R)
- Check: Open DevTools (F12) → Elements → Inspect text → should show "font-family: 'Geist'"

### Issue: Back button doesn't work
**Solution:**
- This is expected behavior in some contexts
- Alternative: Use bottom navbar to navigate
- The back button works from task detail screens

### Issue: Checkboxes on Tasks page don't persist
**Solution:**
- Make sure localStorage is enabled in browser
- Check: F12 → Application → localStorage → should show hros entries
- Try different browser if issue persists

### Issue: Can't see AI chat popup
**Solution:**
- Look for floating circle button on Tasks page (bottom-right)
- Click the button to open AI chat overlay
- If not visible: Check CSS in DevTools

---

## Prototype Capabilities

### What This Prototype Does:
✅ Demonstrates linear onboarding flow
✅ Shows priority-based task dashboard
✅ Provides navigation between main sections
✅ Displays content in unified views
✅ Persists task completion across sessions
✅ Shows alternate date selection workflow
✅ Routes based on employment type
✅ Calculates salary breakdowns
✅ Explains ESOP program

### What This Prototype Doesn't Do:
❌ Connect to actual backend systems
❌ Send data to servers
❌ Create real user accounts
❌ Process actual documents
❌ Send emails or notifications
❌ Integrate with real HR systems
❌ Handle real payment processing

---

## Browser Compatibility

**Tested & Working:**
- ✅ Chrome/Chromium 90+
- ✅ Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+

**Requirements:**
- JavaScript enabled
- Cookies enabled (for localStorage)
- CSS Flexbox/Grid support
- Modern CSS (CSS variables, Grid, Flexbox)

---

## Deployment to GitHub

When ready to share with client, follow these steps:

### Prerequisites:
- GitHub account
- Git installed locally
- GitHub token (if using HTTPS)

### Steps:

1. **Initialize Git (if not already done):**
```bash
cd "C:\Users\PC\Downloads\stitch_hros_design_system_specification"
git init
```

2. **Add all files:**
```bash
git add .
```

3. **Create initial commit:**
```bash
git commit -m "Initial HROS prototype commit - Linear onboarding redesign"
```

4. **Add remote (replace with your repo URL):**
```bash
git remote add origin https://github.com/[username]/hros-prototype.git
```

5. **Push to GitHub:**
```bash
git branch -M main
git push -u origin main
```

6. **Deploy to Temporary Domain:**
   - Use GitHub Pages: Enable in repo Settings → Pages
   - Or use Vercel: `npm i -g vercel && vercel`
   - Or use Netlify: Drag & drop the folder
   - Share the resulting URL with client

### Example URLs after deployment:
- GitHub Pages: `https://[username].github.io/hros-prototype/`
- Vercel: `https://hros-prototype-[random].vercel.app/`
- Netlify: `https://hros-prototype-[name].netlify.app/`

---

## File Information

### Main Prototype File
- **Filename:** `hros_prototype.html`
- **Size:** 3.1 MB
- **Format:** Single HTML file with embedded JSON
- **Screens:** 171 (all embedded)
- **Dependencies:** 
  - Google Fonts (Geist, Material Symbols)
  - Tailwind CSS
  - No server required

### Build Process
- **Builder:** `build_single.py`
- **Input:** Individual screen HTML files in subdirectories
- **Output:** Single combined `hros_prototype.html`
- **Rebuild if needed:**
```bash
python build_single.py
```

---

## Contact & Support

For issues, questions, or feedback:

1. **Check TESTING_GUIDE.md** for common issues
2. **Review CHANGES_SUMMARY.md** for what changed and why
3. **Browser DevTools** (F12) to inspect elements and check for errors
4. **Console** (F12 → Console tab) to see any JavaScript errors

---

## Next Steps for Client Review

1. **Local Testing:** Follow TESTING_GUIDE.md
2. **Visual Review:** Check font consistency, layout, color
3. **Flow Testing:** Verify all paths work as intended
4. **Feedback:** Note any changes needed
5. **GitHub Deployment:** Push to repo when approved
6. **Share URL:** Send temporary domain link to client

---

## Document References

| Document | Purpose | Length |
|----------|---------|--------|
| **README.md** (this file) | Quick start & overview | 5 min read |
| **TESTING_GUIDE.md** | Comprehensive testing checklist | 20 min read |
| **CHANGES_SUMMARY.md** | Detailed changelog & architecture | 15 min read |
| **trace_flows.py** | Flow mappings & navigation paths | Technical reference |
| **build_single.py** | Build process documentation | Technical reference |

---

## Version History

### v1.1 (Current) — May 26, 2026
- ✨ Linear onboarding flow implemented
- ✨ Tasks page redesigned with priority categorization
- ✨ 4 new screens created (calculator, ESOP, date picker, vendor selector)
- ✨ Feed page consolidated
- ✨ Geist sans-serif font standardized throughout
- ✨ Prototype rebuilt with 171 screens
- ✨ Comprehensive testing guides created

### v1.0 (Previous)
- Initial prototype with sidebar flow picker
- Multiple variants of similar screens
- Inconsistent typography
- Missing navigation between main sections

---

## Summary

This redesigned HROS prototype provides a seamless, guided onboarding experience with:
- Clear task prioritization (red alerts for critical items)
- Consolidated content views
- Consistent typography (Geist sans-serif)
- Proper navigation flow
- localStorage persistence
- 4 new specialized screens

**Status:** ✅ **Ready for Local Testing**

Please follow **TESTING_GUIDE.md** to verify all functionality before client review.

---

*Last Updated: May 26, 2026*
*For questions or issues, see TESTING_GUIDE.md troubleshooting section*

