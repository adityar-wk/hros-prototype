"""Trace every sidebar flow chain through the CTA wiring map."""

CTA = {
    # Offer review
    "offer_review_before_acceptance":                "offer_review_candidate_accepted_confirmation",
    "offer_review_default_state":                    "offer_review_candidate_accepted_confirmation",
    "offer_review_expires_soon":                     "offer_review_candidate_accepted_confirmation",
    "offer_review_expired":                          None,   # AI popup
    "offer_review_already_accepted":                 "journey_map_current_stage_expanded",
    "offer_review_candidate_accepted_confirmation":  "journey_map_current_stage_expanded",
    # Joining date
    "joining_date_proposed_confirmed_1":   "joining_date_proposed_confirmed_2",
    "joining_date_proposed_confirmed_2":   "acceptance_confirmation_moment_1",
    "joining_date_alternate_pending_1":    "joining_date_alternate_pending_2",
    "joining_date_alternate_pending_2":    "journey_map_current_stage_expanded",
    "joining_date_alternate_rejected_1":   "joining_date_alternate_rejected_2",
    "joining_date_alternate_rejected_2":   "journey_map_current_stage_expanded",
    "joining_date_pending_task_1":         "joining_date_pending_task_2",
    "joining_date_pending_task_2":         "acceptance_confirmation_moment_1",
    # Welcome
    "acceptance_confirmation_moment_1":    "acceptance_confirmation_moment_2",
    "acceptance_confirmation_moment_2":    "welcome_moment_first_entry",
    "welcome_moment_first_entry":          "journey_map_current_stage_expanded",
    # Data capture
    "data_capture_master_pattern_template":          "data_capture_personal_records_category_a",
    "data_capture_personal_records_category_a":      "data_capture_submission_status_feedback",
    "data_capture_educational_details_category_b":   "data_capture_submission_status_feedback",
    "data_capture_previous_employment_category_c":   "data_capture_submission_status_feedback",
    "data_capture_bank_account_details_category_g":  "data_capture_submission_status_feedback",
    "data_capture_identity_verification_category_f": "data_capture_submission_status_feedback",
    "data_capture_correction_required_state":        "data_capture_submission_status_feedback",
    "data_capture_edge_case_states":                 "data_capture_submission_status_feedback",
    "data_capture_submission_status_feedback":       "journey_map_current_stage_expanded",
    # BGV
    "bgv_consent_state":    "bgv_status_tracker",
    "bgv_status_tracker":   "journey_map_current_stage_expanded",
    # Document signing
    "document_signing_queue_state":         "document_signing_milestone_complete",
    "appointment_letter_preview_consent":   "appointment_letter_signed_confirmation",
    "appointment_letter_signed_confirmation": "journey_map_current_stage_expanded",
    "document_signing_milestone_complete":  "journey_map_current_stage_expanded",
    "statutory_forms_aadhaar_e_sign":       "journey_map_current_stage_expanded",
    # Policy / POSH
    "policy_queue_pending_state":   "posh_policy_content_quiz",
    "posh_policy_content_quiz":     "policies_milestone_complete",
    "posh_quiz_failed_state":       "posh_policy_content_quiz",
    "policies_milestone_complete":  "journey_map_current_stage_expanded",
    # Tax
    "tax_setup_timing_preference":                        "tax_setup_regime_comparison",
    "tax_setup_regime_comparison":                        "tax_setup_investment_declarations",
    "tax_setup_regime_comparison_with_calculator":        "tax_setup_investment_declarations",
    "tax_setup_investment_declarations":                  "tax_setup_verified_locked",
    "tax_setup_investment_declarations_with_optimizer":   "tax_setup_verified_locked",
    "tax_setup_investment_declarations_with_fixed_optimizer": "tax_setup_verified_locked",
    "tax_setup_verified_locked":                          "journey_map_current_stage_expanded",
    # Flexi
    "flexi_allocation_default_state":             "flexi_allocation_active_allocation",
    "flexi_allocation_active_allocation":         "flexi_allocation_verified_locked",
    "flexi_allocation_verified_locked":           "journey_map_current_stage_expanded",
    "flexi_allocation_pool_exhausted_n_a_state":  "journey_map_current_stage_expanded",
    # PF / Payroll
    "pf_nps_retirement_elections":                "payroll_readiness_green_state_confirmed",
    "payroll_readiness_amber_state_pending":       "journey_map_current_stage_expanded",
    "payroll_readiness_green_state_confirmed":     "journey_map_current_stage_expanded",
    "payroll_readiness_locked_state_view_only":    "journey_map_current_stage_expanded",
    "payroll_readiness_override_requested_pending": "journey_map_current_stage_expanded",
    "payroll_readiness_red_state_blockers":        "data_capture_master_pattern_template",
    # Salary
    "salary_preview_review_window_open":  "salary_preview_accepted_confirmed",
    "salary_preview_accepted_confirmed":  "journey_map_current_stage_expanded",
    "salary_preview_concern_flagged":     "salary_preview_review_window_open",
    # Vendor consent
    "vendor_consent_all_pending":       "vendor_consent_preferences_saved",
    "vendor_consent_card_expanded":     "vendor_consent_consent_given",
    "vendor_consent_consent_given":     "vendor_consent_preferences_saved",
    "vendor_consent_mandatory_off":     "vendor_consent_all_pending",
    "vendor_consent_preferences_saved": "journey_map_current_stage_expanded",
    # Asset custody
    "asset_custody_awaiting_acknowledgement": "asset_custody_verified_locked",
    "asset_custody_dispute_raised":           "asset_custody_awaiting_acknowledgement",
    "asset_custody_verified_locked":          "journey_map_current_stage_expanded",
    "asset_custody_not_yet_assigned":         "journey_map_current_stage_expanded",
    # Day 1 / Launchpad
    "day_1_portal_default_state":               "launchpad_day_1_active",
    "day_1_portal_welcome_announcement":         "day_1_portal_welcome_dismissed",
    "day_1_portal_welcome_dismissed":            "day_1_portal_default_state",
    "day_1_portal_linkedin_prompt":              "day_1_portal_linkedin_shared_confirmation",
    "day_1_portal_linkedin_shared_confirmation": "day_1_portal_default_state",
    "day_1_portal_active_schedule":              "journey_map_current_stage_expanded",
    "launchpad_pre_day_1_brief":                 "launchpad_day_1_active",
    "launchpad_day_1_active":                    "launchpad_post_day_1_archive",
    "launchpad_post_day_1_archive":              "journey_map_current_stage_expanded",
    "launchpad_updated_since_last_view":         "launchpad_day_1_active",
    "first_week_schedule":                       "day_1_portal_default_state",
    # Self intro
    "self_introduction_audience_selected":         "self_introduction_writing_with_live_preview",
    "self_introduction_writing_with_live_preview": "self_introduction_published_confirmation",
    "self_introduction_published_confirmation":    "journey_map_current_stage_expanded",
    "self_introduction_opted_out":                 "journey_map_current_stage_expanded",
    "self_introduction_introduction_offered":      "journey_map_current_stage_expanded",
    # Community
    "community_surfacing":              "know_your_team_relationship_view",
    "know_your_team_relationship_view": "journey_map_current_stage_expanded",
    "stakeholder_map_cross_functional_view": "journey_map_current_stage_expanded",
    # Family nominees
    "family_nominees_empty_state":        "family_nominees_nominee_selection",
    "family_nominees_nominee_selection":  "family_nominees_adding_member",
    "family_nominees_adding_member":      "family_nominees_nomination_summary",
    "family_nominees_nomination_summary": "family_nominees_graph_complete",
    "family_nominees_graph_complete":     "journey_map_current_stage_expanded",
    # Post-joining
    "post_joining_confirmation_review_window_open":    "post_joining_confirmation_declaration_submitted",
    "post_joining_confirmation_navigated_away":        "post_joining_confirmation_review_window_open",
    "post_joining_confirmation_returned_with_updates": "post_joining_confirmation_review_window_open",
    "post_joining_confirmation_declaration_submitted": "journey_map_current_stage_expanded",
    "post_joining_confirmation_window_expired":        "journey_map_current_stage_expanded",
    # Legal / compliance
    "conflict_of_interest_declaration":  "journey_map_current_stage_expanded",
    "legal_case_declaration":            "journey_map_current_stage_expanded",
    "bonus_clawback_terms_presentation": "bonus_clawback_acknowledged_state",
    "bonus_clawback_acknowledged_state": "journey_map_current_stage_expanded",
    "equity_grant_active_review":        "journey_map_current_stage_expanded",
    "equity_grant_pending_state":        "journey_map_current_stage_expanded",
    # Pulse surveys
    "pulse_survey_privacy_notice":    "pulse_survey_question_a_success",
    "pulse_survey_question_a_success": "pulse_survey_question_c_salary",
    "pulse_survey_question_c_salary": "pulse_survey_complete_day_30",
    "pulse_survey_complete_day_30":   "journey_map_current_stage_expanded",
    "pulse_survey_jnps_day_60":       "journey_map_current_stage_expanded",
    # HRBP / AMA
    "hrbp_session_upcoming_detail":   "hrbp_session_milestone_complete",
    "hrbp_session_milestone_complete": "journey_map_current_stage_expanded",
    "ama_sessions_discovery_rsvp":    "journey_map_current_stage_expanded",
    # Resignation
    "resignation_tracker_proof_pending":       "resignation_tracker_acceptance_pending",
    "resignation_tracker_date_change_pending": "resignation_tracker_date_change_approved",
    "resignation_tracker_acceptance_pending":  "journey_map_current_stage_expanded",
    "resignation_tracker_date_change_approved": "journey_map_current_stage_expanded",
    "resignation_tracker_lwd_tight_state":     "journey_map_current_stage_expanded",
    # Journey map
    "journey_map_milestone_detail":          "journey_map_current_stage_expanded",
    "journey_map_readiness_action_required": "data_capture_master_pattern_template",
    # Feed
    "feed_new_content_notification": "feed_active_content_mix",
    "feed_content_item_detail":      "feed_active_content_mix",
    "feed_empty_state":              "feed_active_content_mix",
    # Misc
    "steady_state_transition":                "journey_map_current_stage_expanded",
    "probation_active_state":                 "journey_map_current_stage_expanded",
    "milestone_happy_birthday":               "journey_map_current_stage_expanded",
    "milestone_support_moment":               "journey_map_current_stage_expanded",
    "journey_home_call_feedback_state_5":     "journey_home_feedback_saved_state_6",
    "journey_home_feedback_saved_state_6":    "journey_map_current_stage_expanded",
    "benefits_insurance_expanded_view":       "benefits_policies_reference",
    "medical_insurance_coverage_dependents":  "benefits_policies_reference",
    "benefits_policies_reference":            "journey_map_current_stage_expanded",
}

END = "journey_map_current_stage_expanded"

def trace(start, max_steps=15):
    chain = [start]
    seen = {start}
    cur = start
    for _ in range(max_steps):
        nxt = CTA.get(cur)
        if nxt is None:
            chain.append("(dead end / AI popup)")
            break
        if nxt in seen:
            chain.append(f"(cycles back to {nxt})")
            break
        chain.append(nxt)
        seen.add(nxt)
        if nxt == END:
            break
        cur = nxt
    return chain

FLOWS = [
    ("--- OFFER REVIEW ---", None),
    ("Normal Offer Acceptance",    "offer_review_default_state"),
    ("Offer Expiring Soon",        "offer_review_expires_soon"),
    ("Offer Already Expired",      "offer_review_expired"),
    ("Already Accepted (revisit)", "offer_review_already_accepted"),
    ("Before Acceptance",          "offer_review_before_acceptance"),

    ("--- JOINING DATE ---", None),
    ("Date Proposed & Confirmed",  "joining_date_proposed_confirmed_1"),
    ("Alternate Date - Pending",   "joining_date_alternate_pending_1"),
    ("Alternate Date - Rejected",  "joining_date_alternate_rejected_1"),
    ("Pending Task",               "joining_date_pending_task_1"),

    ("--- FIRST ENTRY ---", None),
    ("Acceptance Confirmation",    "acceptance_confirmation_moment_1"),
    ("Welcome (Return Visit)",     "welcome_moment_first_entry"),

    ("--- DATA CAPTURE ---", None),
    ("Personal Records",           "data_capture_personal_records_category_a"),
    ("Educational Details",        "data_capture_educational_details_category_b"),
    ("Previous Employment",        "data_capture_previous_employment_category_c"),
    ("Identity Verification",      "data_capture_identity_verification_category_f"),
    ("Bank Account",               "data_capture_bank_account_details_category_g"),
    ("Correction Required",        "data_capture_correction_required_state"),

    ("--- TAX SETUP ---", None),
    ("Full Tax Flow",              "tax_setup_timing_preference"),
    ("Regime Comparison",          "tax_setup_regime_comparison"),
    ("Regime + Calculator",        "tax_setup_regime_comparison_with_calculator"),

    ("--- FAMILY & NOMINEES ---", None),
    ("Add Nominees",               "family_nominees_empty_state"),

    ("--- PF, NPS & INSURANCE ---", None),
    ("PF + Payroll",               "pf_nps_retirement_elections"),
    ("Insurance View",             "benefits_insurance_expanded_view"),

    ("--- FLEXI ALLOCATION ---", None),
    ("Flexi - Normal",             "flexi_allocation_default_state"),
    ("Flexi - Pool Exhausted",     "flexi_allocation_pool_exhausted_n_a_state"),

    ("--- ASSET CUSTODY ---", None),
    ("Acknowledge Assets",         "asset_custody_awaiting_acknowledgement"),
    ("Dispute an Asset",           "asset_custody_dispute_raised"),
    ("Not Yet Assigned",           "asset_custody_not_yet_assigned"),

    ("--- BGV ---", None),
    ("BGV Full Flow",              "bgv_consent_state"),

    ("--- DOCUMENT SIGNING ---", None),
    ("Document Queue",             "document_signing_queue_state"),
    ("Aadhaar eSign",              "statutory_forms_aadhaar_e_sign"),
    ("Appointment Letter",         "appointment_letter_preview_consent"),

    ("--- VENDOR CONSENT ---", None),
    ("All Pending",                "vendor_consent_all_pending"),
    ("Card Expanded",              "vendor_consent_card_expanded"),
    ("Mandatory Off Warning",      "vendor_consent_mandatory_off"),

    ("--- RESIGNATION ---", None),
    ("Acceptance Pending",         "resignation_tracker_acceptance_pending"),
    ("Proof Pending",              "resignation_tracker_proof_pending"),
    ("Date Change",                "resignation_tracker_date_change_pending"),
    ("LWD Tight",                  "resignation_tracker_lwd_tight_state"),

    ("--- SALARY & PAYROLL ---", None),
    ("Salary Review -> Accept",    "salary_preview_review_window_open"),
    ("Salary Concern Flagged",     "salary_preview_concern_flagged"),
    ("Payroll Red Blockers",       "payroll_readiness_red_state_blockers"),
    ("Payroll Amber",              "payroll_readiness_amber_state_pending"),
    ("Payroll Override",           "payroll_readiness_override_requested_pending"),

    ("--- DAY 1 & LAUNCHPAD ---", None),
    ("Launchpad Flow",             "launchpad_pre_day_1_brief"),
    ("Welcome Announcement",       "day_1_portal_welcome_announcement"),
    ("LinkedIn Prompt",            "day_1_portal_linkedin_prompt"),
    ("Updated Since Last View",    "launchpad_updated_since_last_view"),

    ("--- POST-JOINING ---", None),
    ("Confirm Declaration",        "post_joining_confirmation_review_window_open"),
    ("Navigated Away",             "post_joining_confirmation_navigated_away"),
    ("Window Expired",             "post_joining_confirmation_window_expired"),

    ("--- LEGAL & COMPLIANCE ---", None),
    ("POSH Policy Quiz",           "policy_queue_pending_state"),
    ("POSH Quiz Failed",           "posh_quiz_failed_state"),
    ("Conflict of Interest",       "conflict_of_interest_declaration"),
    ("Legal Declaration",          "legal_case_declaration"),
    ("Bonus Clawback",             "bonus_clawback_terms_presentation"),

    ("--- CULTURE & COMMUNITY ---", None),
    ("Self Intro Full",            "self_introduction_audience_selected"),
    ("Self Intro Opted Out",       "self_introduction_opted_out"),
    ("Community",                  "community_surfacing"),
    ("HRBP Session",               "hrbp_session_upcoming_detail"),
    ("Pulse Survey",               "pulse_survey_privacy_notice"),
    ("Journey Feedback",           "journey_home_call_feedback_state_5"),

    ("--- JOURNEY MAP ---", None),
    ("Readiness Blocker",          "journey_map_readiness_action_required"),
]

for name, start in FLOWS:
    if start is None:
        print(f"\n{'='*60}")
        print(f"  {name}")
        print(f"{'='*60}")
        continue
    chain = trace(start)
    steps = "\n    -> ".join(s for s in chain)
    print(f"\n  [{name}]")
    print(f"    {steps}")
