import os, re, json, sys

BASE   = r"C:\Users\PC\Downloads\stitch_hros_design_system_specification\stitch_hros_design_system_specification"
OUTPUT = r"C:\Users\PC\Downloads\stitch_hros_design_system_specification\hros_prototype.html"

# ── helpers ──────────────────────────────────────────────────────────────────

def screen_id_from_url(url):
    """'../foo_bar/code.html'  ->  'foo_bar'"""
    parts = url.rstrip("'\"").split('/')
    for i, p in enumerate(parts):
        if p.endswith('code.html') and i > 0:
            return parts[i - 1]
    return None

def patch_navigation(html):
    """Replace all local navigation refs so they call window.top.goTo(id)."""

    NAV_JS = "window.top.goTo('{id}')"

    # window.location.href = '../screen/code.html'   (single or double quotes)
    def _loc(m):
        sid = screen_id_from_url(m.group(1))
        if sid:
            return NAV_JS.format(id=sid)
        return m.group(0)

    html = re.sub(r"window\.location\.href\s*=\s*'(\.\.[^']+code\.html)'", _loc, html)
    html = re.sub(r'window\.location\.href\s*=\s*"(\.\.[^"]+code\.html)"', _loc, html)

    # href="../screen/code.html"  ->  href="#" onclick="goTo(...)"
    def _href(m):
        quote = m.group(1)
        url   = m.group(2)
        sid   = screen_id_from_url(url)
        if sid:
            return f'href="#" onclick="{NAV_JS.format(id=sid)}; return false;"'
        return m.group(0)

    html = re.sub(r'href=([\'"])(\.\.[^\'"]+code\.html)\1', _href, html)

    # src="../nav.js"  – remove (we don't need it)
    html = re.sub(r'<script\s+src=["\']\.\.\/nav\.js["\']><\/script>', '', html)

    return html

# ── scenario flows — full coverage ───────────────────────────────────────────
FLOWS = [
    # ── Offer Review ─────────────────────────────────────────────────────────
    {
        "section": "🗂  Offer Review",
        "items": [
            {"name": "Normal Offer Acceptance",    "desc": "Candidate opens offer, reviews, and accepts",                         "start": "offer_review_default_state"},
            {"name": "Offer Expiring Soon",         "desc": "Offer has a 48-hr countdown — candidate accepts under urgency",       "start": "offer_review_expires_soon"},
            {"name": "Offer Already Expired",       "desc": "Candidate opens an offer that has already lapsed",                    "start": "offer_review_expired"},
            {"name": "Already Accepted (revisit)",  "desc": "Candidate reopens a letter they already signed",                      "start": "offer_review_already_accepted"},
            {"name": "Before Acceptance",           "desc": "Pre-acceptance state — letter not yet opened",                        "start": "offer_review_before_acceptance"},
        ],
    },
    # ── Joining Date ──────────────────────────────────────────────────────────
    {
        "section": "📅  Joining Date",
        "items": [
            {"name": "Date Proposed & Confirmed",   "desc": "Company proposes a joining date; candidate confirms",                 "start": "joining_date_proposed_confirmed_1"},
            {"name": "Alternate Date — Pending",    "desc": "Candidate requests a different date; awaiting approval",              "start": "joining_date_alternate_pending_1"},
            {"name": "Alternate Date — Rejected",   "desc": "Requested date rejected; candidate picks from available slots",       "start": "joining_date_alternate_rejected_1"},
            {"name": "Pending Task (step 1)",       "desc": "Joining date task card shown in task list",                           "start": "joining_date_pending_task_1"},
        ],
    },
    # ── First Entry & Welcome ─────────────────────────────────────────────────
    {
        "section": "🎉  First Entry & Welcome",
        "items": [
            {"name": "Acceptance Confirmation",     "desc": "Cinematic welcome moment after offer is signed",                      "start": "acceptance_confirmation_moment_1"},
            {"name": "Welcome Screen (Return Visit)","desc": "Arjun's identity card shown before entering the portal",             "start": "welcome_moment_first_entry"},
        ],
    },
    # ── Journey & Portal ─────────────────────────────────────────────────────
    {
        "section": "🗺  Journey & Portal",
        "items": [
            {"name": "Journey Map — Current Stage", "desc": "Main onboarding timeline with Data stage active",                     "start": "journey_map_current_stage_expanded"},
            {"name": "Journey Map — Milestone Detail","desc": "Expanded detail panel for a specific milestone",                    "start": "journey_map_milestone_detail"},
            {"name": "Readiness — Action Required", "desc": "Journey map with a readiness blocker the candidate must resolve",     "start": "journey_map_readiness_action_required"},
            {"name": "Tasks — Active",              "desc": "Active task list with pending items",                                 "start": "tasks_active_state"},
            {"name": "Tasks — Overdue & Blocked",   "desc": "Task list showing overdue and blocked items requiring attention",     "start": "tasks_overdue_blocked"},
            {"name": "Tasks — All Completed",       "desc": "All tasks done — completion state after finishing every step",        "start": "tasks_all_completed"},
            {"name": "You / Data Rights",           "desc": "Profile, consent settings, and data rights pane",                    "start": "data_rights_pane"},
        ],
    },
    # ── Feed ─────────────────────────────────────────────────────────────────
    {
        "section": "📰  Feed",
        "items": [
            {"name": "Empty Feed",                  "desc": "No content yet — first time experience",                             "start": "feed_empty_state"},
            {"name": "Active Feed — Mixed Content", "desc": "Articles, videos, and announcements in one stream",                  "start": "feed_active_content_mix"},
            {"name": "Active Feed — Video Content", "desc": "Feed with prominent video cards",                                    "start": "feed_active_video_content"},
            {"name": "Content Item Detail",         "desc": "Open a single article or post full-screen",                          "start": "feed_content_item_detail"},
            {"name": "New Content Notification",    "desc": "Nudge badge when fresh content arrives",                             "start": "feed_new_content_notification"},
        ],
    },
    # ── Data Capture ──────────────────────────────────────────────────────────
    {
        "section": "📋  Data Capture",
        "items": [
            {"name": "Personal Records (Cat A)",    "desc": "Basic personal info — name, DOB, address",                           "start": "data_capture_personal_records_category_a"},
            {"name": "Educational Details (Cat B)", "desc": "Education history — degrees and institutions",                       "start": "data_capture_educational_details_category_b"},
            {"name": "Previous Employment (Cat C)", "desc": "Work history — past employers and roles",                            "start": "data_capture_previous_employment_category_c"},
            {"name": "Identity Verification (Cat F)","desc": "ID document upload — Aadhaar, PAN, passport",                      "start": "data_capture_identity_verification_category_f"},
            {"name": "Bank Account (Cat G)",        "desc": "Salary bank account details entry",                                  "start": "data_capture_bank_account_details_category_g"},
            {"name": "Correction Required",         "desc": "HR flagged a field for correction — edit flow",                     "start": "data_capture_correction_required_state"},
            {"name": "Submission Status",           "desc": "Post-submit status and feedback screen",                             "start": "data_capture_submission_status_feedback"},
            {"name": "Edge Case States",            "desc": "Special states — optional fields, long text, etc.",                  "start": "data_capture_edge_case_states"},
        ],
    },
    # ── Tax Setup ─────────────────────────────────────────────────────────────
    {
        "section": "🧾  Tax Setup",
        "items": [
            {"name": "Regime Comparison",           "desc": "Old vs new tax regime comparison view",                              "start": "tax_setup_regime_comparison"},
            {"name": "Regime + Calculator",         "desc": "Regime comparison with interactive tax calculator",                  "start": "tax_setup_regime_comparison_with_calculator"},
            {"name": "Investment Declarations",     "desc": "Declare 80C, HRA, NPS and other investments",                       "start": "tax_setup_investment_declarations"},
            {"name": "Declarations + Optimizer",    "desc": "Declarations with AI-suggested optimizations highlighted",           "start": "tax_setup_investment_declarations_with_optimizer"},
            {"name": "Declarations + Fixed Optimizer","desc": "Optimizer with fixed/locked recommendations",                     "start": "tax_setup_investment_declarations_with_fixed_optimizer"},
            {"name": "Timing Preference",           "desc": "Choose when to lock tax declarations for the year",                 "start": "tax_setup_timing_preference"},
            {"name": "Verified & Locked",           "desc": "Tax setup complete — frozen for the year",                          "start": "tax_setup_verified_locked"},
        ],
    },
    # ── Family & Nominees ────────────────────────────────────────────────────
    {
        "section": "👨‍👩‍👧  Family & Nominees",
        "items": [
            {"name": "Empty State",                 "desc": "No nominees added yet — first visit",                                "start": "family_nominees_empty_state"},
            {"name": "Nominee Selection",           "desc": "Pick relationship type for a new nominee",                           "start": "family_nominees_nominee_selection"},
            {"name": "Adding a Member",             "desc": "Fill in nominee details form",                                       "start": "family_nominees_adding_member"},
            {"name": "Nomination Summary",          "desc": "Review all nominees before submitting",                              "start": "family_nominees_nomination_summary"},
            {"name": "Graph Complete",              "desc": "All nominees added — family graph full view",                        "start": "family_nominees_graph_complete"},
        ],
    },
    # ── PF, NPS & Insurance ──────────────────────────────────────────────────
    {
        "section": "🏦  PF, NPS & Insurance",
        "items": [
            {"name": "PF & NPS Elections",          "desc": "Provident fund and NPS contribution choices",                        "start": "pf_nps_retirement_elections"},
            {"name": "Insurance — Expanded View",   "desc": "Benefits and insurance coverage detail",                             "start": "benefits_insurance_expanded_view"},
            {"name": "Medical + Dependents",        "desc": "Add family dependents to medical cover",                             "start": "medical_insurance_coverage_dependents"},
            {"name": "Policies Reference",          "desc": "All company policies and benefit documents",                         "start": "benefits_policies_reference"},
        ],
    },
    # ── Flexi Allocation ─────────────────────────────────────────────────────
    {
        "section": "💰  Flexi Allocation",
        "items": [
            {"name": "Default State",               "desc": "Flexi pool before any allocation is made",                           "start": "flexi_allocation_default_state"},
            {"name": "Active Allocation",           "desc": "Candidate actively distributing the flexi amount",                   "start": "flexi_allocation_active_allocation"},
            {"name": "Pool Exhausted",              "desc": "All flexi funds allocated — nothing left to assign",                 "start": "flexi_allocation_pool_exhausted_n_a_state"},
            {"name": "Verified & Locked",           "desc": "Allocation confirmed and frozen",                                    "start": "flexi_allocation_verified_locked"},
        ],
    },
    # ── Asset Custody ────────────────────────────────────────────────────────
    {
        "section": "💼  Asset Custody",
        "items": [
            {"name": "Not Yet Assigned",            "desc": "Assets not yet allocated to this candidate",                         "start": "asset_custody_not_yet_assigned"},
            {"name": "Awaiting Acknowledgement",    "desc": "Asset list shared — waiting for candidate sign-off",                 "start": "asset_custody_awaiting_acknowledgement"},
            {"name": "Dispute Raised",              "desc": "Candidate disputes an asset item in the list",                       "start": "asset_custody_dispute_raised"},
            {"name": "Verified & Locked",           "desc": "All assets acknowledged and locked",                                 "start": "asset_custody_verified_locked"},
        ],
    },
    # ── Background Verification ───────────────────────────────────────────────
    {
        "section": "🔍  Background Verification",
        "items": [
            {"name": "BGV Consent",                 "desc": "Consent form before background checks begin",                        "start": "bgv_consent_state"},
            {"name": "Status Tracker",              "desc": "Live BGV status — checks in progress",                               "start": "bgv_status_tracker"},
        ],
    },
    # ── Document Signing ─────────────────────────────────────────────────────
    {
        "section": "✍️  Document Signing",
        "items": [
            {"name": "Signing Queue",               "desc": "Documents pending signature from the candidate",                     "start": "document_signing_queue_state"},
            {"name": "Aadhaar eSign",               "desc": "Statutory form signed via Aadhaar OTP flow",                        "start": "statutory_forms_aadhaar_e_sign"},
            {"name": "Milestone Complete",          "desc": "All documents signed — completion celebration screen",               "start": "document_signing_milestone_complete"},
        ],
    },
    # ── Appointment Letter ───────────────────────────────────────────────────
    {
        "section": "📄  Appointment Letter",
        "items": [
            {"name": "Preview & Consent",           "desc": "Read letter and give consent before signing",                        "start": "appointment_letter_preview_consent"},
            {"name": "Signed Confirmation",         "desc": "Letter signed — confirmation and next steps",                        "start": "appointment_letter_signed_confirmation"},
        ],
    },
    # ── Vendor Consent ───────────────────────────────────────────────────────
    {
        "section": "🤝  Vendor Consent",
        "items": [
            {"name": "All Pending",                 "desc": "All vendor consents awaiting a decision",                            "start": "vendor_consent_all_pending"},
            {"name": "Card Expanded",               "desc": "One vendor's consent card expanded for review",                     "start": "vendor_consent_card_expanded"},
            {"name": "Consent Given",               "desc": "Candidate accepted a vendor's terms",                                "start": "vendor_consent_consent_given"},
            {"name": "Mandatory Off (Warning)",     "desc": "Candidate tried to disable a mandatory consent",                     "start": "vendor_consent_mandatory_off"},
            {"name": "Preferences Saved",           "desc": "All consent preferences saved and confirmed",                       "start": "vendor_consent_preferences_saved"},
        ],
    },
    # ── Resignation Tracking ─────────────────────────────────────────────────
    {
        "section": "🚪  Resignation Tracking",
        "items": [
            {"name": "Acceptance Pending",          "desc": "Resignation submitted — awaiting employer acceptance",               "start": "resignation_tracker_acceptance_pending"},
            {"name": "Proof Pending",               "desc": "Employer needs a resignation proof document",                        "start": "resignation_tracker_proof_pending"},
            {"name": "Date Change Pending",         "desc": "Last working day change request sent — awaiting reply",              "start": "resignation_tracker_date_change_pending"},
            {"name": "Date Change Approved",        "desc": "LWD change request approved by employer",                            "start": "resignation_tracker_date_change_approved"},
            {"name": "LWD Tight State",             "desc": "Last working day is very close — urgency state",                     "start": "resignation_tracker_lwd_tight_state"},
        ],
    },
    # ── Salary & Payroll ─────────────────────────────────────────────────────
    {
        "section": "💵  Salary & Payroll",
        "items": [
            {"name": "Salary Preview — Review Window","desc": "Candidate reviewing the salary breakdown",                        "start": "salary_preview_review_window_open"},
            {"name": "Salary Preview — Concern Flagged","desc": "Candidate raised a concern on a pay component",                 "start": "salary_preview_concern_flagged"},
            {"name": "Salary Preview — Accepted",   "desc": "Salary confirmed and accepted by candidate",                        "start": "salary_preview_accepted_confirmed"},
            {"name": "Salary — Component Detail",   "desc": "Drill-down into a single pay component with proration",             "start": "salary_preview_component_detail_proration"},
            {"name": "Payroll Readiness — Green",   "desc": "All payroll data confirmed — ready to process",                     "start": "payroll_readiness_green_state_confirmed"},
            {"name": "Payroll Readiness — Amber",   "desc": "Some items pending — partial readiness",                            "start": "payroll_readiness_amber_state_pending"},
            {"name": "Payroll Readiness — Red",     "desc": "Critical blockers preventing payroll processing",                   "start": "payroll_readiness_red_state_blockers"},
            {"name": "Payroll Readiness — Override", "desc": "HR override requested for pending items",                          "start": "payroll_readiness_override_requested_pending"},
            {"name": "Payroll Readiness — Locked",  "desc": "Payroll locked — view-only read state",                             "start": "payroll_readiness_locked_state_view_only"},
        ],
    },
    # ── Day 1 & Launchpad ────────────────────────────────────────────────────
    {
        "section": "🗓  Day 1 & Launchpad",
        "items": [
            {"name": "Launchpad — Pre Day 1",       "desc": "Brief and checklist before joining day",                             "start": "launchpad_pre_day_1_brief"},
            {"name": "Launchpad — Day 1 Active",    "desc": "Day 1 launchpad with live schedule",                                 "start": "launchpad_day_1_active"},
            {"name": "Launchpad — New Items",       "desc": "Updated since last visit — new items highlighted",                   "start": "launchpad_updated_since_last_view"},
            {"name": "Launchpad — Post Day 1",      "desc": "Day 1 content archived after joining day passes",                    "start": "launchpad_post_day_1_archive"},
            {"name": "Day 1 Portal — Default",      "desc": "Day 1 portal clean default state",                                  "start": "day_1_portal_default_state"},
            {"name": "Day 1 Portal — Active Schedule","desc": "Live schedule with ongoing session highlighted",                   "start": "day_1_portal_active_schedule"},
            {"name": "Day 1 Portal — Welcome Msg",  "desc": "Welcome announcement from the company",                             "start": "day_1_portal_welcome_announcement"},
            {"name": "Day 1 Portal — LinkedIn Prompt","desc": "Nudge to share joining post on LinkedIn",                         "start": "day_1_portal_linkedin_prompt"},
            {"name": "Day 1 Portal — LinkedIn Shared","desc": "Confirmation after sharing on LinkedIn",                          "start": "day_1_portal_linkedin_shared_confirmation"},
            {"name": "First Week Schedule",         "desc": "Structured first week calendar view",                                "start": "first_week_schedule"},
        ],
    },
    # ── Post-Joining & Confirmations ──────────────────────────────────────────
    {
        "section": "📝  Post-Joining",
        "items": [
            {"name": "Review Window Open",          "desc": "Post-joining confirmation window is live",                           "start": "post_joining_confirmation_review_window_open"},
            {"name": "Navigated Away",              "desc": "Candidate left before completing — reminder state",                  "start": "post_joining_confirmation_navigated_away"},
            {"name": "Returned with Updates",       "desc": "Candidate came back and made changes",                               "start": "post_joining_confirmation_returned_with_updates"},
            {"name": "Declaration Submitted",       "desc": "Post-joining confirmation submitted",                                "start": "post_joining_confirmation_declaration_submitted"},
            {"name": "Window Expired",              "desc": "Confirmation window closed — too late to edit",                     "start": "post_joining_confirmation_window_expired"},
            {"name": "Steady State Transition",     "desc": "Candidate moves to steady-state employment",                        "start": "steady_state_transition"},
            {"name": "Probation Active",            "desc": "Probation period tracker and check-ins",                            "start": "probation_active_state"},
        ],
    },
    # ── Legal & Compliance ───────────────────────────────────────────────────
    {
        "section": "⚖️  Legal & Compliance",
        "items": [
            {"name": "Conflict of Interest",        "desc": "Declare any conflicts of interest before joining",                   "start": "conflict_of_interest_declaration"},
            {"name": "Legal Case Declaration",      "desc": "Disclose any pending legal cases",                                  "start": "legal_case_declaration"},
            {"name": "POSH Policy Quiz",            "desc": "Mandatory POSH awareness quiz",                                     "start": "posh_policy_content_quiz"},
            {"name": "POSH Quiz — Failed",          "desc": "Failed POSH quiz — must retry to proceed",                          "start": "posh_quiz_failed_state"},
            {"name": "Policies — Pending Queue",    "desc": "Policies awaiting candidate acknowledgement",                       "start": "policy_queue_pending_state"},
            {"name": "Policies — All Complete",     "desc": "All policies read and acknowledged",                                 "start": "policies_milestone_complete"},
            {"name": "Bonus Clawback — Terms",      "desc": "Clawback clause disclosure before signing",                        "start": "bonus_clawback_terms_presentation"},
            {"name": "Bonus Clawback — Acknowledged","desc": "Clawback terms accepted by candidate",                             "start": "bonus_clawback_acknowledged_state"},
        ],
    },
    # ── Equity & Benefits ────────────────────────────────────────────────────
    {
        "section": "💹  Equity & Benefits",
        "items": [
            {"name": "Equity Grant — Pending",      "desc": "Grant letter not yet accepted by candidate",                        "start": "equity_grant_pending_state"},
            {"name": "Equity Grant — Active Review","desc": "Reviewing vesting schedule and grant details",                      "start": "equity_grant_active_review"},
        ],
    },
    # ── Culture & Community ──────────────────────────────────────────────────
    {
        "section": "👥  Culture & Community",
        "items": [
            {"name": "Self-Intro — Writing",        "desc": "Drafting introduction with live preview",                            "start": "self_introduction_writing_with_live_preview"},
            {"name": "Self-Intro — Audience",       "desc": "Choose who sees the introduction",                                  "start": "self_introduction_audience_selected"},
            {"name": "Self-Intro — Published",      "desc": "Introduction live — confirmation screen",                           "start": "self_introduction_published_confirmation"},
            {"name": "Self-Intro — Opted Out",      "desc": "Candidate skipped self-introduction",                               "start": "self_introduction_opted_out"},
            {"name": "Know Your Team",              "desc": "Relationship map of immediate team members",                         "start": "know_your_team_relationship_view"},
            {"name": "Stakeholder Map",             "desc": "Cross-functional stakeholder view",                                  "start": "stakeholder_map_cross_functional_view"},
            {"name": "Community Surfacing",         "desc": "Relevant communities and groups to join",                           "start": "community_surfacing"},
            {"name": "AMA — Discovery & RSVP",      "desc": "Upcoming Ask-Me-Anything sessions with sign-up",                    "start": "ama_sessions_discovery_rsvp"},
            {"name": "Operating Norms",             "desc": "Team working agreements and norms",                                  "start": "operating_norms"},
            {"name": "L&D Toolkit",                 "desc": "Learning and development resources library",                        "start": "l_d_toolkit"},
            {"name": "BU Horizontal Intro",         "desc": "Business unit introduction overview screen",                        "start": "bu_horizontal_intro"},
        ],
    },
    # ── Surveys & Milestones ─────────────────────────────────────────────────
    {
        "section": "📊  Surveys & Milestones",
        "items": [
            {"name": "Pulse Survey — Privacy Notice","desc": "Consent screen before first pulse survey",                         "start": "pulse_survey_privacy_notice"},
            {"name": "Pulse Survey — Question",     "desc": "Standard survey question with positive tone",                       "start": "pulse_survey_question_a_success"},
            {"name": "Pulse Survey — Salary Q",     "desc": "Sensitive pay-satisfaction question handling",                      "start": "pulse_survey_question_c_salary"},
            {"name": "Pulse Survey — Day 30 Done",  "desc": "30-day check-in submitted — thank you screen",                      "start": "pulse_survey_complete_day_30"},
            {"name": "Pulse Survey — Day 60 jNPS",  "desc": "60-day jNPS survey submitted",                                      "start": "pulse_survey_jnps_day_60"},
            {"name": "HRBP Session — Upcoming",     "desc": "Scheduled HRBP meeting detail view",                                "start": "hrbp_session_upcoming_detail"},
            {"name": "HRBP Session — Complete",     "desc": "HRBP session done — milestone screen",                              "start": "hrbp_session_milestone_complete"},
            {"name": "Milestone — Happy Birthday",  "desc": "Birthday milestone moment screen",                                  "start": "milestone_happy_birthday"},
            {"name": "Milestone — Support Moment",  "desc": "Empathy check-in milestone screen",                                 "start": "milestone_support_moment"},
            {"name": "Journey Home — Feedback",     "desc": "Feedback state on home journey view",                               "start": "journey_home_call_feedback_state_5"},
            {"name": "Journey Home — Feedback Saved","desc": "Feedback saved confirmation",                                      "start": "journey_home_feedback_saved_state_6"},
        ],
    },
    # ── Joining Dashboard ────────────────────────────────────────────────────
    {
        "section": "🏢  Joining Dashboard & Misc",
        "items": [
            {"name": "Joining Dashboard — Mobile",  "desc": "Mobile joining experience dashboard",                               "start": "joining_experience_dashboard_mobile"},
            {"name": "Joining Dashboard — Desktop", "desc": "Desktop joining experience dashboard",                              "start": "joining_experience_dashboard_desktop"},
            {"name": "Relocation & Travel Support", "desc": "Relocation assistance and travel booking",                          "start": "relocation_travel_support"},
            {"name": "Radical HR Reduction",        "desc": "HR simplification scenario screen",                                 "start": "radical_reduction_hr"},
        ],
    },
]

# ── read all screens ──────────────────────────────────────────────────────────

screens = {}   # { screen_id: full_patched_html }

for folder in sorted(os.listdir(BASE)):
    fp = os.path.join(BASE, folder, 'code.html')
    if not os.path.exists(fp):
        continue
    try:
        with open(fp, encoding='utf-8', errors='replace') as f:
            html = f.read()
    except Exception as e:
        print(f'  skip {folder}: {e}')
        continue

    html = patch_navigation(html)
    screens[folder] = html

print(f'Loaded {len(screens)} screens')

# ── serialise screens safely ──────────────────────────────────────────────────
# json.dumps does NOT escape forward-slashes, so </script> inside HTML strings
# would terminate the surrounding <script> block in the master page.
# Fix: replace every </ with <\/ (valid JSON, invisible to HTML parser).

screens_json = json.dumps(screens, ensure_ascii=False)
screens_json = screens_json.replace('</', '<\\/')   # safe for HTML parser

# ── build master page ─────────────────────────────────────────────────────────

# ── build scenario sidebar HTML ───────────────────────────────────────────────
sidebar_parts = []
for group in FLOWS:
    sidebar_parts.append(f'<div class="section-label">{group["section"]}</div>')
    for flow in group["items"]:
        sid   = flow["start"]
        name  = flow["name"]
        desc  = flow["desc"]
        sidebar_parts.append(
            f'<div class="flow-card" data-id="{sid}" onclick="startFlow(\'{sid}\')">'
            f'  <div class="flow-name">{name}</div>'
            f'  <div class="flow-desc">{desc}</div>'
            f'</div>'
        )

# Collapsible "All Screens" for dev access
all_items = []
for sid in sorted(screens.keys()):
    label = sid.replace('_', ' ').title()
    all_items.append(f'<div class="item" onclick="goTo(\'{sid}\')">{label}</div>')

sidebar_html = '\n'.join(sidebar_parts)
all_screens_html = '\n'.join(all_items)

master = f"""<!DOCTYPE html>
<!-- HROS Prototype — scenario-driven sidebar -->
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>HROS Prototype</title>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@100..900&display=swap" rel="stylesheet"/>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: #111;
    display: flex;
    height: 100vh;
    overflow: hidden;
    font-family: 'Geist', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  }}

  /* ── sidebar ── */
  #sidebar {{
    width: 280px;
    flex-shrink: 0;
    background: #141414;
    border-right: 1px solid #242424;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }}
  #sidebar-header {{
    padding: 18px 16px 14px;
    border-bottom: 1px solid #242424;
  }}
  #sidebar-logo {{
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 4px;
  }}
  #sidebar-logo .logo-dot {{
    width: 8px; height: 8px;
    background: #c6c4df;
    border-radius: 50%;
  }}
  #sidebar-logo h1 {{
    color: #fff;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 0.06em;
  }}
  #sidebar-subtitle {{
    color: #555;
    font-size: 11px;
    padding-left: 16px;
  }}
  #sidebar-list {{
    overflow-y: auto;
    flex: 1;
    padding: 10px 0 4px;
  }}
  #sidebar-list::-webkit-scrollbar {{ width: 3px; }}
  #sidebar-list::-webkit-scrollbar-thumb {{ background: #2a2a2a; border-radius: 2px; }}

  /* section label */
  .section-label {{
    padding: 14px 16px 5px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: #444;
    text-transform: uppercase;
  }}

  /* flow card */
  .flow-card {{
    margin: 3px 10px;
    padding: 10px 12px;
    border-radius: 8px;
    cursor: pointer;
    border: 1px solid transparent;
    transition: background 0.15s, border-color 0.15s;
  }}
  .flow-card:hover {{
    background: #1e1e1e;
    border-color: #2e2e2e;
  }}
  .flow-card.active {{
    background: #1c1c2e;
    border-color: #3a3a5c;
  }}
  .flow-name {{
    font-size: 12px;
    font-weight: 600;
    color: #ddd;
    margin-bottom: 3px;
  }}
  .flow-card.active .flow-name {{ color: #c6c4df; }}
  .flow-desc {{
    font-size: 10.5px;
    color: #555;
    line-height: 1.45;
  }}
  .flow-card.active .flow-desc {{ color: #7a7a9a; }}

  /* all-screens toggle */
  #all-screens-toggle {{
    padding: 10px 16px;
    font-size: 10px;
    color: #444;
    cursor: pointer;
    border-top: 1px solid #1e1e1e;
    display: flex;
    align-items: center;
    gap: 6px;
    transition: color 0.15s;
  }}
  #all-screens-toggle:hover {{ color: #666; }}
  #all-screens-toggle .arrow {{ transition: transform 0.2s; }}
  #all-screens-toggle.open .arrow {{ transform: rotate(90deg); }}
  #all-screens-list {{
    display: none;
    border-top: 1px solid #1e1e1e;
    max-height: 240px;
    overflow-y: auto;
    padding: 4px 0;
  }}
  #all-screens-list.open {{ display: block; }}
  .item {{
    padding: 5px 16px;
    font-size: 10.5px;
    color: #555;
    cursor: pointer;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    transition: color 0.1s;
  }}
  .item:hover {{ color: #999; }}

  /* ── phone frame ── */
  #stage {{
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    padding: 20px;
  }}
  #phone-wrap {{
    position: relative;
    width: 390px;
    height: 844px;
    border-radius: 48px;
    background: #000;
    box-shadow: 0 0 0 10px #1c1c1e, 0 30px 100px rgba(0,0,0,0.9);
    overflow: hidden;
    flex-shrink: 0;
  }}
  /* notch */
  #phone-wrap::before {{
    content: '';
    position: absolute;
    top: 0; left: 50%;
    transform: translateX(-50%);
    width: 120px; height: 30px;
    background: #000;
    border-radius: 0 0 20px 20px;
    z-index: 99;
  }}
  #frame {{
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    border: none;
    border-radius: 48px;
  }}

  /* ── breadcrumb bar ── */
  #breadcrumb {{
    position: absolute;
    bottom: 0; left: 0; right: 0;
    background: rgba(0,0,0,0.75);
    color: #aaa;
    font-size: 10px;
    padding: 4px 12px;
    display: flex;
    align-items: center;
    gap: 6px;
    z-index: 300;
    border-top: 1px solid #333;
  }}
  #breadcrumb span {{ color: #fff; font-weight: 500; }}
  #breadcrumb button {{
    background: none;
    border: 1px solid #444;
    border-radius: 4px;
    color: #aaa;
    font-size: 10px;
    padding: 2px 8px;
    cursor: pointer;
  }}
  #breadcrumb button:hover {{ color: #fff; border-color: #666; }}

  /* ── AI Chat Popup ── */
  #ai-popup {{
    display: none;
    position: absolute;
    inset: 0;
    z-index: 200;
    flex-direction: column;
    justify-content: flex-end;
    background: rgba(0,0,0,0.45);
    border-radius: 48px;
  }}
  #ai-popup.open {{ display: flex; }}
  #ai-sheet {{
    background: #fcf8fa;
    border-radius: 28px 28px 0 0;
    padding: 20px 20px 24px;
    display: flex;
    flex-direction: column;
    gap: 14px;
    max-height: 72%;
    box-shadow: 0 -8px 40px rgba(0,0,0,0.18);
  }}
  #ai-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  #ai-title {{
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 15px;
    font-weight: 600;
    color: #00000b;
  }}
  #ai-title .badge {{
    background: #e2e0fc;
    color: #45455b;
    font-size: 10px;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 20px;
    letter-spacing: 0.04em;
  }}
  #ai-close {{
    background: #e5e1e3;
    border: none;
    border-radius: 50%;
    width: 28px; height: 28px;
    cursor: pointer;
    font-size: 14px;
    color: #47464c;
    display: flex; align-items: center; justify-content: center;
  }}
  #ai-messages {{
    flex: 1;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 10px;
    min-height: 100px;
    max-height: 300px;
    padding-right: 4px;
  }}
  #ai-messages::-webkit-scrollbar {{ width: 3px; }}
  #ai-messages::-webkit-scrollbar-thumb {{ background: #c8c5cd; border-radius: 2px; }}
  .ai-msg-bot {{
    background: #f1edef;
    border-radius: 4px 16px 16px 16px;
    padding: 10px 14px;
    font-size: 13px;
    color: #1c1b1d;
    max-width: 82%;
    line-height: 1.5;
  }}
  .ai-msg-user {{
    background: #00000b;
    color: #fff;
    border-radius: 16px 4px 16px 16px;
    padding: 10px 14px;
    font-size: 13px;
    max-width: 82%;
    align-self: flex-end;
    line-height: 1.5;
  }}
  .ai-typing {{
    background: #f1edef;
    border-radius: 4px 16px 16px 16px;
    padding: 10px 14px;
    font-size: 13px;
    color: #78767d;
    max-width: 82%;
  }}
  #ai-input-row {{
    display: flex;
    gap: 8px;
    align-items: center;
  }}
  #ai-input {{
    flex: 1;
    border: 1.5px solid #c8c5cd;
    border-radius: 24px;
    padding: 10px 16px;
    font-size: 13px;
    outline: none;
    font-family: 'Geist', sans-serif;
    background: #fff;
    color: #1c1b1d;
    transition: border-color 0.2s;
  }}
  #ai-input:focus {{ border-color: #5d5c74; }}
  #ai-send {{
    background: #00000b;
    color: #fff;
    border: none;
    border-radius: 24px;
    padding: 10px 18px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    font-family: 'Geist', sans-serif;
    flex-shrink: 0;
    transition: opacity 0.2s;
  }}
  #ai-send:hover {{ opacity: 0.85; }}
</style>
</head>
<body>

<!-- Sidebar -->
<div id="sidebar">
  <div id="sidebar-header">
    <div id="sidebar-logo">
      <div class="logo-dot"></div>
      <h1>HROS</h1>
    </div>
    <div id="sidebar-subtitle">Prototype · Full scenario coverage</div>
  </div>
  <div id="sidebar-list">
    {sidebar_html}
  </div>
  <!-- All Screens drawer (dev access) -->
  <div id="all-screens-toggle" onclick="toggleAllScreens()">
    <span class="arrow">▶</span> All screens ({len(screens)})
  </div>
  <div id="all-screens-list">
    {all_screens_html}
  </div>
</div>

<!-- Phone stage -->
<div id="stage">
  <div id="phone-wrap">
    <iframe id="frame" allow="scripts"></iframe>

    <!-- AI Chat Popup — lives inside the phone frame, above the iframe -->
    <div id="ai-popup">
      <div id="ai-sheet">
        <div id="ai-header">
          <div id="ai-title">
            <span style="font-size:20px;">✨</span>
            HROS AI
            <span class="badge">BETA</span>
          </div>
          <button id="ai-close" onclick="closeAIChat()" title="Close">✕</button>
        </div>
        <div id="ai-messages">
          <div class="ai-msg-bot">Hi! I'm your HROS AI concierge. Ask me anything about your onboarding journey.</div>
        </div>
        <div id="ai-input-row">
          <input id="ai-input" type="text" placeholder="Ask me anything…"
                 onkeydown="if(event.key==='Enter')sendAIMsg()"/>
          <button id="ai-send" onclick="sendAIMsg()">Send</button>
        </div>
      </div>
    </div>

    <div id="breadcrumb">
      <span id="bc-id">—</span>
      <button onclick="goBack()" style="margin-left:auto;">← Back</button>
    </div>
  </div>
</div>

<script>
const SCREENS = {screens_json};

// AI screens — open popup instead of navigating
const AI_SCREENS = new Set([
  'ai_concierge_active_chat',
  'ai_concierge_preparation_offer',
  'ai_concierge_preparation_offer_state_1',
  'ai_concierge_preparation_ready_state_4',
  'ai_concierge_sharing_consent_state_3',
  'ai_concierge_suggested_questions_consent',
  'ai_concierge_suggested_questions_state_2',
  'ai_concierge_escalation_to_human',
  'ai_concierge_offer_dismissed',
]);

let _history = [];
let _current = null;

function goTo(id) {{
  // AI screens → popup, not navigation
  if (AI_SCREENS.has(id)) {{
    openAIChat();
    return;
  }}
  if (!SCREENS[id]) {{
    console.warn('[HROS] Screen not found:', id);
    return;
  }}
  closeAIChat();
  _history.push(id);
  _current = id;

  document.getElementById('frame').srcdoc = SCREENS[id];
  document.getElementById('bc-id').textContent = id.replace(/_/g,' ');
  // highlight matching flow card in the scenario sidebar
  document.querySelectorAll('.flow-card').forEach(el => {{
    el.classList.toggle('active', el.getAttribute('data-id') === id);
  }});
}}

function goBack() {{
  if (_history.length > 1) {{
    _history.pop();
    const prev = _history[_history.length - 1];
    _current = prev;
    document.getElementById('frame').srcdoc = SCREENS[prev];
    document.getElementById('bc-id').textContent = prev.replace(/_/g,' ');
    document.querySelectorAll('.flow-card').forEach(el => {{
      el.classList.toggle('active', el.getAttribute('data-id') === prev);
    }});
  }}
}}

function startFlow(id) {{
  goTo(id);
}}

function toggleAllScreens() {{
  const list = document.getElementById('all-screens-list');
  const toggle = document.getElementById('all-screens-toggle');
  list.classList.toggle('open');
  toggle.classList.toggle('open');
}}

// ── AI Popup ────────────────────────────────────────────────────────────────

const AI_RESPONSES = [
  "I can help with that! Your data is safely stored and DPDP compliant.",
  "Great question. For this step, just follow the on-screen prompts and tap Continue when ready.",
  "Your HRBP Siddharth V. is available for deeper questions — want me to flag this for them?",
  "The next milestone in your journey is Readiness. You can track it from the Journey tab.",
  "All your submitted documents are under review. Verification usually takes 24–48 hours.",
  "Your start date is Oct 15, 2024 in Bangalore. Anything specific you'd like to know?",
  "Looks like everything is on track! Is there anything else I can help with?",
];
let _aiIdx = 0;

function openAIChat() {{
  document.getElementById('ai-popup').classList.add('open');
  document.getElementById('ai-input').focus();
}}
window.openAIChat = openAIChat;

function closeAIChat() {{
  document.getElementById('ai-popup').classList.remove('open');
}}

function sendAIMsg() {{
  const input = document.getElementById('ai-input');
  const msg = input.value.trim();
  if (!msg) return;
  const box = document.getElementById('ai-messages');

  // User bubble
  const uBubble = document.createElement('div');
  uBubble.className = 'ai-msg-user';
  uBubble.textContent = msg;
  box.appendChild(uBubble);
  input.value = '';

  // Typing indicator
  const typing = document.createElement('div');
  typing.className = 'ai-typing';
  typing.textContent = '…';
  box.appendChild(typing);
  box.scrollTop = box.scrollHeight;

  // AI response after delay
  setTimeout(() => {{
    typing.remove();
    const resp = AI_RESPONSES[_aiIdx % AI_RESPONSES.length];
    _aiIdx++;
    const aBubble = document.createElement('div');
    aBubble.className = 'ai-msg-bot';
    aBubble.textContent = resp;
    box.appendChild(aBubble);
    box.scrollTop = box.scrollHeight;
  }}, 700);
}}

// Close popup when clicking the backdrop
document.getElementById('ai-popup').addEventListener('click', function(e) {{
  if (e.target === this) closeAIChat();
}});

// Start on the offer review screen
goTo('offer_review_default_state');
</script>
</body>
</html>"""

with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(master)

size_mb = os.path.getsize(OUTPUT) / 1024 / 1024
print(f'Written: {OUTPUT}')
print(f'File size: {size_mb:.1f} MB')
print(f'Screens embedded: {len(screens)}')
