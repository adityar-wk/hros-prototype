# HROS Prototype Testing Guide

## Overview
This guide covers comprehensive testing of the redesigned HROS onboarding prototype. The prototype now features a linear onboarding flow with a redesigned Tasks page, consolidated Feed page, and enhanced Profile page.

---

## Quick Start
1. Open `hros_prototype.html` in your browser
2. The prototype loads the main scenario sidebar on the left
3. Click any flow to start testing

---

## Testing Checklist

### 1. Core Onboarding Flow (Entry Point)
**Entry:** Open hros_prototype.html → Sidebar shows "Offer Acceptance" flows

- [ ] **Offer Review** 
  - Click "Normal" flow under "Offer Acceptance"
  - Verify: Clean sans-serif (Geist) fonts throughout
  - Verify: Offer details visible (Senior Product Designer, ₹42,00,000 CTC, etc.)
  - Verify: "Accept this offer" button at bottom

- [ ] **Joining Date Confirmation**
  - Click "Accept this offer" button
  - Verify: Navigates to joining_date_proposed_confirmed_1
  - Verify: Shows "Oct 14, 2024" with "Continue to confirmation" button
  - Verify: Button is responsive (not stuck on double-click)

- [ ] **Joining Date Alternate Flow** (Test "Request Different Date" scenario)
  - On joining_date_proposed_confirmed_1, look for "Request Different Date" option
  - Click to select alternate date
  - Verify: Calendar picker shows October/November 2024 dates
  - Verify: Selection submits for approval
  - Verify: Shows pending approval message
  - Verify: After ~3 seconds, either approves or rejects
  - If rejected: Returns to date picker to retry
  - If approved: Proceeds to acceptance confirmation

- [ ] **Acceptance Confirmation**
  - After confirming joining date
  - Verify: Navigates to acceptance_confirmation_moment_1
  - Verify: Shows congratulations message
  - Verify: "Next" button proceeds to welcome screen

- [ ] **Welcome Screen**
  - Verify: Personalized welcome message
  - Verify: "Let's get started" button proceeds to next step

- [ ] **Tasks Page (First Time)**
  - Verify: Lands on tasks_active_state (Tasks tab active in navbar)
  - Verify: 4-tab structure visible: "Priority Now" | "Before Joining" | "Post-Joining" | "Optional"
  - Verify: Priority Now tab shows red alerts on required tasks
  - Verify: Progress rings show 0/6 completed tasks

---

### 2. Tasks Page Detailed Testing

#### Tab Content Verification

**Priority Now Tab (6 items - RED alerts):**
- [ ] Personal Information (REQUIRED - Due: Today)
- [ ] Work History (REQUIRED - Due: Today)
- [ ] Identity Verification (REQUIRED - Due: Today)
- [ ] BGV Consent (TIME-SENSITIVE - Due: Sep 30)
- [ ] Document Signing (TIME-SENSITIVE - Due: Oct 10)
- [ ] Appointment Letter (TIME-SENSITIVE - Due: Oct 12)

**Before Joining Tab (10 items):**
- [ ] Tax Setup
- [ ] Family Nominees
- [ ] Flexi Allocation
- [ ] PF/NPS Elections
- [ ] Benefits Enrollment
- [ ] Medical Insurance
- [ ] Salary Preview
- [ ] Payroll Readiness
- [ ] Vendor Consent
- [ ] Policies & POSH

**Post-Joining Tab (4 items - greyed out):**
- [ ] Conflict of Interest Declaration
- [ ] Legal Case Declaration
- [ ] Bonus Clawback Acknowledgement
- [ ] Post-Joining Confirmation

**Optional Tab (5 items):**
- [ ] Equity Grant Review
- [ ] Self Introduction
- [ ] Community Surfacing
- [ ] HRBP Session
- [ ] Pulse Surveys

#### Progress Tracking
- [ ] Priority Now shows: 0/6 (all unchecked)
- [ ] Clicking checkbox marks task as complete
- [ ] Progress ring updates to show completion (e.g., 1/6)
- [ ] Check localStorage (F12 → Application → localStorage) for task persistence
- [ ] Refresh page: Checkmarks should persist

#### Font Consistency
- [ ] All headers use Geist sans-serif (no serifs)
- [ ] All body text uses Geist sans-serif
- [ ] Icons (Material Symbols) render correctly
- [ ] Font weights correct: Headers 600, Body 400, Labels 500/600

---

### 3. Navigation Testing

#### Bottom Navbar (4 Tabs)
- [ ] **Tasks** - Points to tasks_active_state (should show red alert badge on Priority)
- [ ] **Feed** - Points to feed_active_content_mix
- [ ] **Journey** - Points to journey_map_current_stage_expanded
- [ ] **Profile** - Points to data_rights_pane

#### Tab Switching
- [ ] Click "Feed" tab
  - Verify: Navigates to Feed page
  - Verify: Feed tab highlighted in navbar
  - Verify: Shows Welcome Video, Joining Resources, Latest Updates, Meet Your Team, Culture sections
  - Verify: Expandable cards work (click to expand, click to collapse)
  - Verify: All text uses Geist sans-serif fonts

- [ ] Click "Journey" tab
  - Verify: Navigates to journey_map_current_stage_expanded
  - Verify: Shows onboarding journey timeline/map
  - Verify: Journey tab highlighted in navbar

- [ ] Click "Profile" tab
  - Verify: Navigates to Profile (data_rights_pane)
  - Verify: Shows Profile tab highlighted (with filled person icon)
  - Verify: Navbar shows "Profile" (not "You")
  - Verify: Data Rights sections visible
  - Verify: Expandable accordion for Emergency Contacts

#### Back Button Navigation
- [ ] From any task detail screen, click back button (↶ in header)
  - Verify: Returns to Tasks page
  - Verify: Correct tab is restored

- [ ] From Feed, click back button
  - Verify: Returns to previous page (or Tasks if entry point)

- [ ] From Profile, click back button
  - Verify: Returns to Tasks page or previous page

---

### 4. New Flow Testing

#### Task: Salary Preview → In-Hand Calculator
- [ ] On Tasks page, Before Joining tab, click "Salary Preview"
- [ ] Verify: Navigates to in_hand_calculator screen
- [ ] Verify: Shows salary breakdown
- [ ] Verify: Can input CTC, HRA, 80C investments
- [ ] Verify: Calculates take-home, taxes, PF deductions
- [ ] Verify: Back button returns to Tasks page

#### Task: Equity Grant → ESOP Explainer
- [ ] On Profile page (or Tasks page if integrated), click "Equity Grant Review" or ESOP link
- [ ] Verify: Navigates to esop_explainer
- [ ] Verify: Shows ESOP information sections (What are ESOPs, How they work, Vesting, Taxes)
- [ ] Verify: Expandable FAQs work correctly
- [ ] Verify: Back button returns to Profile or Tasks

#### Vendor Consent Gated Flow
- [ ] On Tasks page, Before Joining tab, click "Vendor Consent"
- [ ] Verify: Lands on vendor_consent_employee_type_selector
- [ ] Verify: Two choice cards: "Full-Time Employee" and "Contract/Vendor Role"
- [ ] Select "Full-Time Employee"
  - Verify: Continue button enables
  - Verify: Routes to vendor_consent_all_pending (standard employee flow)
- [ ] Go back, select "Contract/Vendor Role"
  - Verify: Routes to vendor_consent_all_pending (same destination, could be different vendors in future)
- [ ] From vendor consent, complete flow
  - Verify: Returns to Tasks page
  - Verify: Vendor Consent marked as complete (if tracking implemented)

---

### 5. Font Consistency Verification

Use browser DevTools (F12) to inspect elements:

- [ ] **Offer letter page** - All text should be Geist sans-serif
- [ ] **Tasks page** - Headers, buttons, labels all Geist
- [ ] **Feed page** - All content cards use Geist
- [ ] **Profile page** - All sections use Geist
- [ ] **New screens** - Calculator, ESOP explainer, date picker all use Geist
- [ ] **Navbar** - Tab labels use Geist

**DevTools check:**
1. Right-click on any text element
2. Inspect
3. Look for `font-family: 'Geist'` in computed styles
4. Should NOT see system fonts (Arial, Helvetica, etc.) for main content

---

### 6. Edge Cases & Error States

#### Double-Click Prevention
- [ ] On joining_date_proposed_confirmed_1, confirm button should be debounced
- [ ] Clicking confirm rapidly should only trigger once

#### Alternate Date Rejection Loop
- [ ] Request alternate date → Get rejected → Should loop back to picker
- [ ] Can select different date and resubmit
- [ ] Does not break navigation

#### Post-Joining Tasks Disabled
- [ ] On Tasks page, Post-Joining tab
- [ ] All 4 items should appear greyed out/disabled (if Day 1 hasn't passed)
- [ ] Clicking disabled item should show tooltip or indication

#### Task Completion Persistence
- [ ] Mark 3 tasks as complete in Priority Now tab
- [ ] Navigate to another tab
- [ ] Navigate back to Priority Now
- [ ] Verify checkmarks are still there
- [ ] Close browser, reopen hros_prototype.html
- [ ] Verify checkmarks are still there (localStorage persistence)

---

### 7. AI Concierge Functionality

- [ ] On Tasks page, look for floating AI button (circle icon) in bottom-right
- [ ] Click AI button
  - Verify: Opens AI chat modal/popup overlay
  - Verify: Chat interface appears within the same page (not new tab)
  - Verify: Can type and interact with AI
  - Verify: Clicking outside or close button dismisses popup
  - Verify: Returns to Tasks page (not navigation)

---

### 8. Mobile Responsiveness (if applicable)

- [ ] Resize browser to 390px width (mobile frame)
- [ ] Verify: Layout adapts properly
- [ ] Verify: Navbar items fit in bottom nav
- [ ] Verify: Cards and text remain readable
- [ ] Verify: No horizontal scrolling
- [ ] Verify: Touch targets (buttons) are at least 44x44px

---

## Bug Report Template

If you find issues, please document:

```
**Screen:** [screen name]
**Issue:** [description of what's broken]
**Steps to Reproduce:**
1. [step 1]
2. [step 2]
3. [step 3]

**Expected:** [what should happen]
**Actual:** [what actually happened]
**Screenshots:** [attach if possible]

**Font Issue?** Yes / No
**Navigation Issue?** Yes / No
**Data Loss?** Yes / No
```

---

## Test Results Summary

After running through all tests, please fill in:

- [ ] Core onboarding flow: **PASS / FAIL**
- [ ] Tasks page functionality: **PASS / FAIL**
- [ ] Navigation between pages: **PASS / FAIL**
- [ ] New flows (calculator, ESOP, vendor consent): **PASS / FAIL**
- [ ] Font consistency (Geist throughout): **PASS / FAIL**
- [ ] Back button functionality: **PASS / FAIL**
- [ ] Task completion persistence: **PASS / FAIL**
- [ ] Overall UX & visual consistency: **PASS / FAIL**

**Overall Status:** READY FOR GITHUB / NEEDS FIXES

---

## Next Steps

After local testing:
1. Fix any critical bugs found
2. Review visual consistency
3. Test on mobile devices if applicable
4. Prepare for GitHub deployment
5. Share link with client for review

