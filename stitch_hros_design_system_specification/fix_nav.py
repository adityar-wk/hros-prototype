import os, re, sys

BASE = r"C:\Users\PC\Downloads\stitch_hros_design_system_specification\stitch_hros_design_system_specification"

NAV = {
    'Journey': '../journey_map_current_stage_expanded/code.html',
    'Tasks':   '../tasks_active_state/code.html',
    'Feed':    '../feed_active_content_mix/code.html',
    'AI':      '../ai_concierge_active_chat/code.html',
    'You':     '../data_rights_pane/code.html',
}

# CTA: screen_id -> [(button_text_substring, target_url), ...]
# First matching text wins; script only modifies first un-wired match per entry
CTA = {
    # ---- Offer review variants ----
    'offer_review_before_acceptance':                [('Accept', '../joining_date_proposed_confirmed_1/code.html')],
    'offer_review_candidate_default_state':          [('Accept', '../joining_date_proposed_confirmed_1/code.html')],
    'offer_review_candidate_default_refined_1':      [('Accept', '../joining_date_proposed_confirmed_1/code.html')],
    'offer_review_candidate_default_refined_2':      [('Accept', '../joining_date_proposed_confirmed_1/code.html')],
    'offer_review_expires_soon':                     [('Accept', '../joining_date_proposed_confirmed_1/code.html')],
    'offer_review_candidate_expires_soon_refined_1': [('Accept', '../joining_date_proposed_confirmed_1/code.html')],
    'offer_review_candidate_expires_soon_refined_2': [('Accept', '../joining_date_proposed_confirmed_1/code.html')],
    'offer_review_already_accepted':                 [('View journey', '../journey_map_current_stage_expanded/code.html'),
                                                      ('journey', '../journey_map_current_stage_expanded/code.html')],
    'offer_review_candidate_accepted_confirmation':  [('Open', '../journey_map_current_stage_expanded/code.html'),
                                                      ('Continue', '../journey_map_current_stage_expanded/code.html')],
    'offer_review_candidate_accepted_refined_1':     [('Open', '../journey_map_current_stage_expanded/code.html'),
                                                      ('Continue', '../journey_map_current_stage_expanded/code.html')],
    'offer_review_candidate_accepted_refined_2':     [('Open', '../journey_map_current_stage_expanded/code.html'),
                                                      ('Continue', '../journey_map_current_stage_expanded/code.html')],
    # ---- Joining date flows ----
    'joining_date_alternate_pending_1':   [('Submit', '../joining_date_alternate_pending_2/code.html'),
                                           ('Request', '../joining_date_alternate_pending_2/code.html'),
                                           ('Continue', '../joining_date_alternate_pending_2/code.html')],
    'joining_date_alternate_pending_2':   [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                           ('Done', '../journey_map_current_stage_expanded/code.html')],
    'joining_date_alternate_rejected_1':  [('Continue', '../joining_date_alternate_rejected_2/code.html'),
                                           ('Understood', '../joining_date_alternate_rejected_2/code.html'),
                                           ('Ok', '../joining_date_alternate_rejected_2/code.html')],
    'joining_date_alternate_rejected_2':  [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                           ('Done', '../journey_map_current_stage_expanded/code.html')],
    'joining_date_pending_task_1':        [('Continue', '../joining_date_pending_task_2/code.html'),
                                           ('Submit', '../joining_date_pending_task_2/code.html'),
                                           ('Next', '../joining_date_pending_task_2/code.html')],
    'joining_date_pending_task_2':        [('Continue', '../acceptance_confirmation_moment_1/code.html'),
                                           ('Confirm', '../acceptance_confirmation_moment_1/code.html')],
    # ---- Data capture ----
    'data_capture_master_pattern_template':          [('Continue', '../data_capture_personal_records_category_a/code.html'),
                                                      ('Start', '../data_capture_personal_records_category_a/code.html'),
                                                      ('Next', '../data_capture_personal_records_category_a/code.html')],
    'data_capture_personal_records_category_a':      [('Save', '../data_capture_submission_status_feedback/code.html'),
                                                      ('Continue', '../data_capture_submission_status_feedback/code.html'),
                                                      ('Submit', '../data_capture_submission_status_feedback/code.html')],
    'data_capture_educational_details_category_b':   [('Save', '../data_capture_submission_status_feedback/code.html'),
                                                      ('Continue', '../data_capture_submission_status_feedback/code.html'),
                                                      ('Submit', '../data_capture_submission_status_feedback/code.html')],
    'data_capture_previous_employment_category_c':   [('Save', '../data_capture_submission_status_feedback/code.html'),
                                                      ('Continue', '../data_capture_submission_status_feedback/code.html'),
                                                      ('Submit', '../data_capture_submission_status_feedback/code.html')],
    'data_capture_bank_account_details_category_g':  [('Save', '../data_capture_submission_status_feedback/code.html'),
                                                      ('Continue', '../data_capture_submission_status_feedback/code.html'),
                                                      ('Submit', '../data_capture_submission_status_feedback/code.html')],
    'data_capture_identity_verification_category_f': [('Save', '../data_capture_submission_status_feedback/code.html'),
                                                      ('Continue', '../data_capture_submission_status_feedback/code.html'),
                                                      ('Submit', '../data_capture_submission_status_feedback/code.html'),
                                                      ('Verify', '../data_capture_submission_status_feedback/code.html')],
    'data_capture_correction_required_state':        [('Resubmit', '../data_capture_submission_status_feedback/code.html'),
                                                      ('Fix', '../data_capture_submission_status_feedback/code.html'),
                                                      ('Submit', '../data_capture_submission_status_feedback/code.html'),
                                                      ('Update', '../data_capture_submission_status_feedback/code.html')],
    'data_capture_edge_case_states':                 [('Continue', '../data_capture_submission_status_feedback/code.html'),
                                                      ('Submit', '../data_capture_submission_status_feedback/code.html')],
    'data_capture_submission_status_feedback':       [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                                      ('Done', '../journey_map_current_stage_expanded/code.html'),
                                                      ('Back to Journey', '../journey_map_current_stage_expanded/code.html'),
                                                      ('Go to Journey', '../journey_map_current_stage_expanded/code.html')],
    # ---- BGV ----
    'bgv_consent_state':    [('Accept', '../bgv_status_tracker/code.html'),
                              ('Consent', '../bgv_status_tracker/code.html'),
                              ('Agree', '../bgv_status_tracker/code.html'),
                              ('Continue', '../bgv_status_tracker/code.html'),
                              ('Proceed', '../bgv_status_tracker/code.html')],
    'bgv_status_tracker':   [('Continue', '../journey_map_current_stage_expanded/code.html'),
                              ('Done', '../journey_map_current_stage_expanded/code.html')],
    # ---- Document signing ----
    'document_signing_queue_state':          [('Sign', '../document_signing_milestone_complete/code.html'),
                                              ('Review', '../document_signing_milestone_complete/code.html'),
                                              ('Start', '../document_signing_milestone_complete/code.html')],
    'appointment_letter_preview_consent':    [('Sign', '../appointment_letter_signed_confirmation/code.html'),
                                              ('Agree', '../appointment_letter_signed_confirmation/code.html'),
                                              ('Accept', '../appointment_letter_signed_confirmation/code.html'),
                                              ('Proceed', '../appointment_letter_signed_confirmation/code.html')],
    'appointment_letter_signed_confirmation':[('Continue', '../journey_map_current_stage_expanded/code.html'),
                                              ('Done', '../journey_map_current_stage_expanded/code.html')],
    'document_signing_milestone_complete':   [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                              ('Done', '../journey_map_current_stage_expanded/code.html')],
    # ---- Policy / POSH ----
    'policy_queue_pending_state':   [('Start', '../posh_policy_content_quiz/code.html'),
                                     ('Begin', '../posh_policy_content_quiz/code.html'),
                                     ('Continue', '../posh_policy_content_quiz/code.html'),
                                     ('Review', '../posh_policy_content_quiz/code.html')],
    'posh_policy_content_quiz':     [('Submit', '../policies_milestone_complete/code.html'),
                                     ('Complete', '../policies_milestone_complete/code.html'),
                                     ('Finish', '../policies_milestone_complete/code.html')],
    'posh_quiz_failed_state':       [('Retry', '../posh_policy_content_quiz/code.html'),
                                     ('Try Again', '../posh_policy_content_quiz/code.html'),
                                     ('Retake', '../posh_policy_content_quiz/code.html')],
    'policies_milestone_complete':  [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                     ('Done', '../journey_map_current_stage_expanded/code.html')],
    # ---- Salary preview ----
    'salary_preview_review_window_open':    [('Confirm', '../salary_preview_accepted_confirmed/code.html'),
                                             ('Accept', '../salary_preview_accepted_confirmed/code.html'),
                                             ('Looks good', '../salary_preview_accepted_confirmed/code.html')],
    'salary_preview_accepted_confirmed':    [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                             ('Done', '../journey_map_current_stage_expanded/code.html')],
    'salary_preview_concern_flagged':       [('Submit', '../salary_preview_review_window_open/code.html'),
                                             ('Send', '../salary_preview_review_window_open/code.html'),
                                             ('Continue', '../salary_preview_review_window_open/code.html')],
    # ---- Tax setup ----
    'tax_setup_timing_preference':                       [('Continue', '../tax_setup_regime_comparison/code.html'),
                                                          ('Next', '../tax_setup_regime_comparison/code.html')],
    'tax_setup_regime_comparison':                       [('Continue', '../tax_setup_investment_declarations/code.html'),
                                                          ('Select', '../tax_setup_investment_declarations/code.html'),
                                                          ('Next', '../tax_setup_investment_declarations/code.html')],
    'tax_setup_regime_comparison_with_calculator':       [('Continue', '../tax_setup_investment_declarations/code.html'),
                                                          ('Next', '../tax_setup_investment_declarations/code.html')],
    'tax_setup_investment_declarations':                 [('Confirm', '../tax_setup_verified_locked/code.html'),
                                                          ('Submit', '../tax_setup_verified_locked/code.html'),
                                                          ('Save', '../tax_setup_verified_locked/code.html')],
    'tax_setup_investment_declarations_with_optimizer':  [('Confirm', '../tax_setup_verified_locked/code.html'),
                                                          ('Submit', '../tax_setup_verified_locked/code.html'),
                                                          ('Save', '../tax_setup_verified_locked/code.html')],
    'tax_setup_investment_declarations_with_fixed_optimizer': [('Confirm', '../tax_setup_verified_locked/code.html'),
                                                               ('Submit', '../tax_setup_verified_locked/code.html'),
                                                               ('Save', '../tax_setup_verified_locked/code.html')],
    'tax_setup_verified_locked':                         [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                                          ('Done', '../journey_map_current_stage_expanded/code.html')],
    # ---- Flexi allocation ----
    'flexi_allocation_default_state':    [('Start', '../flexi_allocation_active_allocation/code.html'),
                                          ('Begin', '../flexi_allocation_active_allocation/code.html'),
                                          ('Allocate', '../flexi_allocation_active_allocation/code.html'),
                                          ('Continue', '../flexi_allocation_active_allocation/code.html')],
    'flexi_allocation_active_allocation':[('Confirm', '../flexi_allocation_verified_locked/code.html'),
                                          ('Submit', '../flexi_allocation_verified_locked/code.html'),
                                          ('Save', '../flexi_allocation_verified_locked/code.html'),
                                          ('Lock in', '../flexi_allocation_verified_locked/code.html')],
    'flexi_allocation_verified_locked':  [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                          ('Done', '../journey_map_current_stage_expanded/code.html')],
    'flexi_allocation_pool_exhausted_n_a_state': [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                                   ('Done', '../journey_map_current_stage_expanded/code.html')],
    # ---- PF / NPS ----
    'pf_nps_retirement_elections': [('Confirm', '../payroll_readiness_green_state_confirmed/code.html'),
                                     ('Submit', '../payroll_readiness_green_state_confirmed/code.html'),
                                     ('Save', '../payroll_readiness_green_state_confirmed/code.html')],
    # ---- Payroll readiness ----
    'payroll_readiness_amber_state_pending':    [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                                  ('Done', '../journey_map_current_stage_expanded/code.html')],
    'payroll_readiness_green_state_confirmed':  [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                                  ('Done', '../journey_map_current_stage_expanded/code.html')],
    'payroll_readiness_locked_state_view_only': [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                                  ('Done', '../journey_map_current_stage_expanded/code.html')],
    'payroll_readiness_override_requested_pending': [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                                      ('Done', '../journey_map_current_stage_expanded/code.html')],
    'payroll_readiness_red_state_blockers':     [('Fix', '../data_capture_master_pattern_template/code.html'),
                                                  ('Resolve', '../data_capture_master_pattern_template/code.html'),
                                                  ('Continue', '../data_capture_master_pattern_template/code.html')],
    # ---- Vendor consent ----
    'vendor_consent_all_pending':       [('Save', '../vendor_consent_preferences_saved/code.html'),
                                         ('Continue', '../vendor_consent_preferences_saved/code.html'),
                                         ('Submit', '../vendor_consent_preferences_saved/code.html')],
    'vendor_consent_card_expanded':     [('Consent', '../vendor_consent_consent_given/code.html'),
                                         ('Accept', '../vendor_consent_consent_given/code.html'),
                                         ('Agree', '../vendor_consent_consent_given/code.html'),
                                         ('Grant', '../vendor_consent_consent_given/code.html')],
    'vendor_consent_consent_given':     [('Save', '../vendor_consent_preferences_saved/code.html'),
                                         ('Continue', '../vendor_consent_preferences_saved/code.html')],
    'vendor_consent_mandatory_off':     [('Continue', '../vendor_consent_all_pending/code.html'),
                                         ('Back', '../vendor_consent_all_pending/code.html')],
    'vendor_consent_preferences_saved': [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                         ('Done', '../journey_map_current_stage_expanded/code.html')],
    # ---- Asset custody ----
    'asset_custody_awaiting_acknowledgement': [('Acknowledge', '../asset_custody_verified_locked/code.html'),
                                               ('Confirm', '../asset_custody_verified_locked/code.html'),
                                               ('Accept', '../asset_custody_verified_locked/code.html')],
    'asset_custody_dispute_raised':           [('Submit', '../asset_custody_awaiting_acknowledgement/code.html'),
                                               ('Continue', '../asset_custody_awaiting_acknowledgement/code.html'),
                                               ('Raise', '../asset_custody_awaiting_acknowledgement/code.html')],
    'asset_custody_verified_locked':          [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                               ('Done', '../journey_map_current_stage_expanded/code.html')],
    'asset_custody_not_yet_assigned':         [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                               ('Done', '../journey_map_current_stage_expanded/code.html')],
    # ---- Day 1 portal ----
    'day_1_portal_default_state':          [('Start', '../launchpad_day_1_active/code.html'),
                                             ('Begin', '../launchpad_day_1_active/code.html'),
                                             ('View', '../launchpad_day_1_active/code.html'),
                                             ('Open', '../launchpad_day_1_active/code.html')],
    'day_1_portal_welcome_announcement':   [('Dismiss', '../day_1_portal_welcome_dismissed/code.html'),
                                             ('Got it', '../day_1_portal_welcome_dismissed/code.html'),
                                             ('Close', '../day_1_portal_welcome_dismissed/code.html'),
                                             ('Continue', '../day_1_portal_welcome_dismissed/code.html')],
    'day_1_portal_welcome_dismissed':      [('Continue', '../day_1_portal_default_state/code.html'),
                                             ('Done', '../day_1_portal_default_state/code.html')],
    'day_1_portal_linkedin_prompt':        [('Share', '../day_1_portal_linkedin_shared_confirmation/code.html'),
                                             ('Post', '../day_1_portal_linkedin_shared_confirmation/code.html'),
                                             ('Skip', '../day_1_portal_linkedin_prompt_skipped/code.html')],
    'day_1_portal_linkedin_prompt_card':   [('Share', '../day_1_portal_linkedin_shared_confirmation/code.html'),
                                             ('Post', '../day_1_portal_linkedin_shared_confirmation/code.html')],
    'day_1_portal_linkedin_prompt_skipped':[('Continue', '../day_1_portal_default_state/code.html'),
                                             ('Done', '../day_1_portal_default_state/code.html')],
    'day_1_portal_linkedin_shared_confirmation': [('Continue', '../day_1_portal_default_state/code.html'),
                                                   ('Done', '../day_1_portal_default_state/code.html')],
    'day_1_portal_shared_confirmation':    [('Continue', '../day_1_portal_default_state/code.html'),
                                             ('Done', '../day_1_portal_default_state/code.html')],
    'day_1_portal_active_schedule':        [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                             ('Done', '../journey_map_current_stage_expanded/code.html')],
    'day_1_portal_clean_state_skipped':    [('Continue', '../day_1_portal_default_state/code.html'),
                                             ('Done', '../day_1_portal_default_state/code.html')],
    # ---- Launchpad ----
    'launchpad_pre_day_1_brief':        [('Start', '../launchpad_day_1_active/code.html'),
                                          ('Begin', '../launchpad_day_1_active/code.html'),
                                          ('Continue', '../launchpad_day_1_active/code.html'),
                                          ('View', '../launchpad_day_1_active/code.html')],
    'launchpad_day_1_active':           [('Complete', '../launchpad_post_day_1_archive/code.html'),
                                          ('Done', '../launchpad_post_day_1_archive/code.html'),
                                          ('Finish', '../launchpad_post_day_1_archive/code.html'),
                                          ('Mark complete', '../launchpad_post_day_1_archive/code.html')],
    'launchpad_post_day_1_archive':     [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                          ('Done', '../journey_map_current_stage_expanded/code.html')],
    'launchpad_updated_since_last_view':[('View', '../launchpad_day_1_active/code.html'),
                                          ('Continue', '../launchpad_day_1_active/code.html'),
                                          ('See updates', '../launchpad_day_1_active/code.html')],
    # ---- Self introduction ----
    'self_introduction_audience_selected':      [('Continue', '../self_introduction_writing_with_live_preview/code.html'),
                                                  ('Next', '../self_introduction_writing_with_live_preview/code.html'),
                                                  ('Write', '../self_introduction_writing_with_live_preview/code.html')],
    'self_introduction_writing_with_live_preview': [('Publish', '../self_introduction_published_confirmation/code.html'),
                                                     ('Submit', '../self_introduction_published_confirmation/code.html'),
                                                     ('Post', '../self_introduction_published_confirmation/code.html'),
                                                     ('Share', '../self_introduction_published_confirmation/code.html')],
    'self_introduction_published_confirmation': [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                                  ('Done', '../journey_map_current_stage_expanded/code.html')],
    'self_introduction_opted_out':              [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                                  ('Done', '../journey_map_current_stage_expanded/code.html'),
                                                  ('Skip', '../journey_map_current_stage_expanded/code.html')],
    'self_introduction_introduction_offered':   [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                                  ('Done', '../journey_map_current_stage_expanded/code.html')],
    # ---- Community ----
    'community_surfacing': [('Join', '../know_your_team_relationship_view/code.html'),
                             ('Continue', '../know_your_team_relationship_view/code.html'),
                             ('Explore', '../know_your_team_relationship_view/code.html')],
    # ---- Know your team ----
    'know_your_team_relationship_view':    [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                             ('Done', '../journey_map_current_stage_expanded/code.html')],
    'stakeholder_map_cross_functional_view': [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                               ('Done', '../journey_map_current_stage_expanded/code.html')],
    # ---- Benefits ----
    'benefits_policies_reference':      [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                          ('Done', '../journey_map_current_stage_expanded/code.html')],
    'benefits_insurance_expanded_view': [('Enrol', '../benefits_policies_reference/code.html'),
                                          ('Enroll', '../benefits_policies_reference/code.html'),
                                          ('Done', '../benefits_policies_reference/code.html'),
                                          ('Save', '../benefits_policies_reference/code.html')],
    'medical_insurance_coverage_dependents': [('Save', '../benefits_policies_reference/code.html'),
                                               ('Continue', '../benefits_policies_reference/code.html'),
                                               ('Done', '../benefits_policies_reference/code.html')],
    # ---- HRBP session ----
    'hrbp_session_upcoming_detail':    [('Book', '../hrbp_session_milestone_complete/code.html'),
                                         ('Confirm', '../hrbp_session_milestone_complete/code.html'),
                                         ('Schedule', '../hrbp_session_milestone_complete/code.html'),
                                         ('Reserve', '../hrbp_session_milestone_complete/code.html')],
    'hrbp_session_milestone_complete': [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                         ('Done', '../journey_map_current_stage_expanded/code.html')],
    # ---- AMA sessions ----
    'ama_sessions_discovery_rsvp': [('RSVP', '../journey_map_current_stage_expanded/code.html'),
                                     ('Register', '../journey_map_current_stage_expanded/code.html'),
                                     ('Join', '../journey_map_current_stage_expanded/code.html'),
                                     ('Reserve', '../journey_map_current_stage_expanded/code.html')],
    # ---- Journey feedback ----
    'journey_home_call_feedback_state_5': [('Submit', '../journey_home_feedback_saved_state_6/code.html'),
                                            ('Send', '../journey_home_feedback_saved_state_6/code.html')],
    'journey_home_feedback_saved_state_6':[('Continue', '../journey_map_current_stage_expanded/code.html'),
                                            ('Done', '../journey_map_current_stage_expanded/code.html')],
    # ---- Resignation tracker ----
    'resignation_tracker_proof_pending':         [('Upload', '../resignation_tracker_acceptance_pending/code.html'),
                                                   ('Submit', '../resignation_tracker_acceptance_pending/code.html'),
                                                   ('Send', '../resignation_tracker_acceptance_pending/code.html')],
    'resignation_tracker_date_change_pending':   [('Submit', '../resignation_tracker_date_change_approved/code.html'),
                                                   ('Confirm', '../resignation_tracker_date_change_approved/code.html'),
                                                   ('Request', '../resignation_tracker_date_change_approved/code.html')],
    'resignation_tracker_acceptance_pending':    [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                                   ('Done', '../journey_map_current_stage_expanded/code.html')],
    'resignation_tracker_date_change_approved':  [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                                   ('Done', '../journey_map_current_stage_expanded/code.html')],
    'resignation_tracker_lwd_tight_state':       [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                                   ('Acknowledge', '../journey_map_current_stage_expanded/code.html')],
    # ---- Family nominees ----
    'family_nominees_empty_state':        [('Add', '../family_nominees_nominee_selection/code.html'),
                                            ('Start', '../family_nominees_nominee_selection/code.html'),
                                            ('Begin', '../family_nominees_nominee_selection/code.html')],
    'family_nominees_nominee_selection':  [('Select', '../family_nominees_adding_member/code.html'),
                                            ('Continue', '../family_nominees_adding_member/code.html'),
                                            ('Next', '../family_nominees_adding_member/code.html')],
    'family_nominees_adding_member':      [('Save', '../family_nominees_nomination_summary/code.html'),
                                            ('Continue', '../family_nominees_nomination_summary/code.html'),
                                            ('Submit', '../family_nominees_nomination_summary/code.html'),
                                            ('Add', '../family_nominees_nomination_summary/code.html')],
    'family_nominees_nomination_summary': [('Confirm', '../family_nominees_graph_complete/code.html'),
                                            ('Submit', '../family_nominees_graph_complete/code.html'),
                                            ('Done', '../family_nominees_graph_complete/code.html')],
    'family_nominees_graph_complete':     [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                            ('Done', '../journey_map_current_stage_expanded/code.html')],
    # ---- Post joining confirmation ----
    'post_joining_confirmation_review_window_open': [('Submit', '../post_joining_confirmation_declaration_submitted/code.html'),
                                                      ('Confirm', '../post_joining_confirmation_declaration_submitted/code.html'),
                                                      ('Declare', '../post_joining_confirmation_declaration_submitted/code.html')],
    'post_joining_confirmation_navigated_away':     [('Return', '../post_joining_confirmation_review_window_open/code.html'),
                                                      ('Continue', '../post_joining_confirmation_review_window_open/code.html'),
                                                      ('Go back', '../post_joining_confirmation_review_window_open/code.html')],
    'post_joining_confirmation_returned_with_updates': [('Continue', '../post_joining_confirmation_review_window_open/code.html'),
                                                         ('Review', '../post_joining_confirmation_review_window_open/code.html'),
                                                         ('Proceed', '../post_joining_confirmation_review_window_open/code.html')],
    'post_joining_confirmation_declaration_submitted': [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                                         ('Done', '../journey_map_current_stage_expanded/code.html')],
    'post_joining_confirmation_window_expired':        [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                                         ('Done', '../journey_map_current_stage_expanded/code.html')],
    # ---- Statutory forms ----
    'statutory_forms_aadhaar_e_sign': [('Sign', '../journey_map_current_stage_expanded/code.html'),
                                        ('Submit', '../journey_map_current_stage_expanded/code.html'),
                                        ('Confirm', '../journey_map_current_stage_expanded/code.html'),
                                        ('Authenticate', '../journey_map_current_stage_expanded/code.html')],
    # ---- Declarations ----
    'conflict_of_interest_declaration': [('Declare', '../journey_map_current_stage_expanded/code.html'),
                                          ('Submit', '../journey_map_current_stage_expanded/code.html'),
                                          ('Confirm', '../journey_map_current_stage_expanded/code.html')],
    'legal_case_declaration':           [('Submit', '../journey_map_current_stage_expanded/code.html'),
                                          ('Declare', '../journey_map_current_stage_expanded/code.html'),
                                          ('Confirm', '../journey_map_current_stage_expanded/code.html')],
    # ---- Bonus clawback ----
    'bonus_clawback_terms_presentation': [('Acknowledge', '../bonus_clawback_acknowledged_state/code.html'),
                                           ('Accept', '../bonus_clawback_acknowledged_state/code.html'),
                                           ('Agree', '../bonus_clawback_acknowledged_state/code.html'),
                                           ('Continue', '../bonus_clawback_acknowledged_state/code.html')],
    'bonus_clawback_acknowledged_state': [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                           ('Done', '../journey_map_current_stage_expanded/code.html')],
    # ---- Equity grant ----
    'equity_grant_active_review': [('Accept', '../journey_map_current_stage_expanded/code.html'),
                                    ('Confirm', '../journey_map_current_stage_expanded/code.html'),
                                    ('Sign', '../journey_map_current_stage_expanded/code.html')],
    'equity_grant_pending_state': [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                    ('Done', '../journey_map_current_stage_expanded/code.html')],
    # ---- Pulse surveys ----
    'pulse_survey_privacy_notice':     [('Continue', '../pulse_survey_question_a_success/code.html'),
                                         ('Agree', '../pulse_survey_question_a_success/code.html'),
                                         ('Accept', '../pulse_survey_question_a_success/code.html'),
                                         ('Proceed', '../pulse_survey_question_a_success/code.html')],
    'pulse_survey_question_a_success': [('Next', '../pulse_survey_question_c_salary/code.html'),
                                         ('Continue', '../pulse_survey_question_c_salary/code.html'),
                                         ('Submit', '../pulse_survey_question_c_salary/code.html')],
    'pulse_survey_question_c_salary':  [('Submit', '../pulse_survey_complete_day_30/code.html'),
                                         ('Done', '../pulse_survey_complete_day_30/code.html'),
                                         ('Finish', '../pulse_survey_complete_day_30/code.html')],
    'pulse_survey_complete_day_30':    [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                         ('Done', '../journey_map_current_stage_expanded/code.html')],
    'pulse_survey_jnps_day_60':        [('Submit', '../journey_map_current_stage_expanded/code.html'),
                                         ('Done', '../journey_map_current_stage_expanded/code.html'),
                                         ('Finish', '../journey_map_current_stage_expanded/code.html')],
    # ---- Misc / transitions ----
    'steady_state_transition':         [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                         ('Begin', '../journey_map_current_stage_expanded/code.html'),
                                         ('Start', '../journey_map_current_stage_expanded/code.html')],
    'probation_active_state':          [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                         ('Done', '../journey_map_current_stage_expanded/code.html')],
    'milestone_happy_birthday':        [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                         ('Done', '../journey_map_current_stage_expanded/code.html')],
    'milestone_support_moment':        [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                         ('Done', '../journey_map_current_stage_expanded/code.html')],
    'operating_norms':                 [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                         ('Done', '../journey_map_current_stage_expanded/code.html')],
    'l_d_toolkit':                     [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                         ('Done', '../journey_map_current_stage_expanded/code.html')],
    'radical_reduction_hr':            [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                         ('Done', '../journey_map_current_stage_expanded/code.html')],
    'bu_horizontal_intro':             [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                         ('Done', '../journey_map_current_stage_expanded/code.html')],
    'relocation_travel_support':       [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                         ('Done', '../journey_map_current_stage_expanded/code.html')],
    'joining_experience_dashboard_mobile': [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                             ('Done', '../journey_map_current_stage_expanded/code.html')],
    'joining_experience_dashboard_desktop':[('Continue', '../journey_map_current_stage_expanded/code.html'),
                                             ('Done', '../journey_map_current_stage_expanded/code.html')],
    'first_week_schedule':             [('Continue', '../day_1_portal_default_state/code.html'),
                                         ('Done', '../day_1_portal_default_state/code.html')],
    # ---- Feed ----
    'feed_new_content_notification':   [('View', '../feed_active_content_mix/code.html'),
                                         ('See all', '../feed_active_content_mix/code.html'),
                                         ('Open', '../feed_active_content_mix/code.html')],
    'feed_content_item_detail':        [('Continue', '../feed_active_content_mix/code.html'),
                                         ('Done', '../feed_active_content_mix/code.html')],
    'feed_empty_state':                [('Continue', '../feed_active_content_mix/code.html'),
                                         ('Done', '../feed_active_content_mix/code.html')],
    # ---- AI concierge flows ----
    'ai_concierge_preparation_offer':        [('Start', '../ai_concierge_preparation_offer_state_1/code.html'),
                                               ('Begin', '../ai_concierge_preparation_offer_state_1/code.html'),
                                               ('Continue', '../ai_concierge_preparation_offer_state_1/code.html')],
    'ai_concierge_preparation_offer_state_1':[('Continue', '../ai_concierge_suggested_questions_state_2/code.html'),
                                               ('Next', '../ai_concierge_suggested_questions_state_2/code.html')],
    'ai_concierge_suggested_questions_state_2': [('Continue', '../ai_concierge_sharing_consent_state_3/code.html'),
                                                  ('Next', '../ai_concierge_sharing_consent_state_3/code.html')],
    'ai_concierge_suggested_questions_consent': [('Continue', '../ai_concierge_active_chat/code.html'),
                                                  ('Done', '../ai_concierge_active_chat/code.html')],
    'ai_concierge_sharing_consent_state_3': [('Continue', '../ai_concierge_preparation_ready_state_4/code.html'),
                                              ('Next', '../ai_concierge_preparation_ready_state_4/code.html'),
                                              ('Agree', '../ai_concierge_preparation_ready_state_4/code.html')],
    'ai_concierge_preparation_ready_state_4': [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                                ('Done', '../journey_map_current_stage_expanded/code.html'),
                                                ('Start', '../journey_map_current_stage_expanded/code.html')],
    'ai_concierge_escalation_to_human': [('Continue', '../ai_concierge_active_chat/code.html'),
                                          ('Done', '../ai_concierge_active_chat/code.html')],
    'ai_concierge_offer_dismissed':     [('Continue', '../ai_concierge_active_chat/code.html'),
                                          ('Done', '../ai_concierge_active_chat/code.html')],
    # ---- Journey map ----
    'journey_map_milestone_detail':          [('Continue', '../journey_map_current_stage_expanded/code.html'),
                                               ('Done', '../journey_map_current_stage_expanded/code.html'),
                                               ('Start', '../data_capture_master_pattern_template/code.html'),
                                               ('Begin', '../data_capture_master_pattern_template/code.html')],
    'journey_map_readiness_action_required': [('Continue', '../data_capture_master_pattern_template/code.html'),
                                               ('Start', '../data_capture_master_pattern_template/code.html'),
                                               ('Fix', '../data_capture_master_pattern_template/code.html')],
}

# BACK: screen_id -> target
BACK = {
    'journey_map_milestone_detail':              '../journey_map_current_stage_expanded/code.html',
    'journey_map_readiness_action_required':     '../journey_map_current_stage_expanded/code.html',
    'data_capture_master_pattern_template':      '../journey_map_current_stage_expanded/code.html',
    'data_capture_personal_records_category_a':      '../data_capture_master_pattern_template/code.html',
    'data_capture_educational_details_category_b':   '../data_capture_master_pattern_template/code.html',
    'data_capture_previous_employment_category_c':   '../data_capture_master_pattern_template/code.html',
    'data_capture_bank_account_details_category_g':  '../data_capture_master_pattern_template/code.html',
    'data_capture_identity_verification_category_f': '../data_capture_master_pattern_template/code.html',
    'data_capture_correction_required_state':        '../data_capture_master_pattern_template/code.html',
    'data_capture_submission_status_feedback':   '../data_capture_master_pattern_template/code.html',
    'data_capture_edge_case_states':             '../data_capture_master_pattern_template/code.html',
    'bgv_consent_state':                         '../journey_map_current_stage_expanded/code.html',
    'bgv_status_tracker':                        '../journey_map_current_stage_expanded/code.html',
    'document_signing_queue_state':              '../journey_map_current_stage_expanded/code.html',
    'appointment_letter_preview_consent':        '../document_signing_queue_state/code.html',
    'salary_preview_review_window_open':         '../journey_map_current_stage_expanded/code.html',
    'salary_preview_component_detail_proration': '../salary_preview_review_window_open/code.html',
    'salary_preview_concern_flagged':            '../salary_preview_review_window_open/code.html',
    'tax_setup_timing_preference':               '../journey_map_current_stage_expanded/code.html',
    'tax_setup_regime_comparison':               '../tax_setup_timing_preference/code.html',
    'tax_setup_regime_comparison_with_calculator': '../tax_setup_timing_preference/code.html',
    'tax_setup_investment_declarations':         '../tax_setup_regime_comparison/code.html',
    'tax_setup_investment_declarations_with_optimizer':      '../tax_setup_regime_comparison/code.html',
    'tax_setup_investment_declarations_with_fixed_optimizer':'../tax_setup_regime_comparison/code.html',
    'flexi_allocation_default_state':            '../journey_map_current_stage_expanded/code.html',
    'flexi_allocation_pool_exhausted_n_a_state': '../flexi_allocation_default_state/code.html',
    'vendor_consent_all_pending':                '../journey_map_current_stage_expanded/code.html',
    'vendor_consent_card_expanded':              '../vendor_consent_all_pending/code.html',
    'vendor_consent_mandatory_off':              '../vendor_consent_all_pending/code.html',
    'asset_custody_not_yet_assigned':            '../journey_map_current_stage_expanded/code.html',
    'asset_custody_awaiting_acknowledgement':    '../journey_map_current_stage_expanded/code.html',
    'asset_custody_dispute_raised':              '../asset_custody_awaiting_acknowledgement/code.html',
    'day_1_portal_active_schedule':              '../day_1_portal_default_state/code.html',
    'day_1_portal_clean_state_skipped':          '../day_1_portal_default_state/code.html',
    'day_1_portal_welcome_dismissed':            '../day_1_portal_default_state/code.html',
    'day_1_portal_linkedin_prompt':              '../day_1_portal_default_state/code.html',
    'day_1_portal_linkedin_prompt_card':         '../day_1_portal_default_state/code.html',
    'day_1_portal_linkedin_prompt_skipped':      '../day_1_portal_default_state/code.html',
    'day_1_portal_linkedin_shared_confirmation': '../day_1_portal_default_state/code.html',
    'day_1_portal_shared_confirmation':          '../day_1_portal_default_state/code.html',
    'launchpad_pre_day_1_brief':                 '../day_1_portal_default_state/code.html',
    'launchpad_day_1_active':                    '../day_1_portal_default_state/code.html',
    'launchpad_post_day_1_archive':              '../day_1_portal_default_state/code.html',
    'feed_content_item_detail':                  '../feed_active_content_mix/code.html',
    'feed_active_video_content':                 '../feed_active_content_mix/code.html',
    'ai_concierge_escalation_to_human':          '../ai_concierge_active_chat/code.html',
    'ai_concierge_offer_dismissed':              '../ai_concierge_active_chat/code.html',
    'ai_concierge_active_chat':                  '../journey_map_current_stage_expanded/code.html',
    'self_introduction_audience_selected':       '../journey_map_current_stage_expanded/code.html',
    'self_introduction_opted_out':               '../self_introduction_audience_selected/code.html',
    'self_introduction_introduction_offered':    '../know_your_team_relationship_view/code.html',
    'know_your_team_relationship_view':          '../journey_map_current_stage_expanded/code.html',
    'stakeholder_map_cross_functional_view':     '../know_your_team_relationship_view/code.html',
    'benefits_policies_reference':               '../journey_map_current_stage_expanded/code.html',
    'benefits_insurance_expanded_view':          '../benefits_policies_reference/code.html',
    'medical_insurance_coverage_dependents':     '../benefits_policies_reference/code.html',
    'resignation_tracker_acceptance_pending':    '../journey_map_current_stage_expanded/code.html',
    'resignation_tracker_date_change_approved':  '../journey_map_current_stage_expanded/code.html',
    'resignation_tracker_date_change_pending':   '../journey_map_current_stage_expanded/code.html',
    'resignation_tracker_lwd_tight_state':       '../journey_map_current_stage_expanded/code.html',
    'resignation_tracker_proof_pending':         '../journey_map_current_stage_expanded/code.html',
    'family_nominees_empty_state':               '../journey_map_current_stage_expanded/code.html',
    'family_nominees_nominee_selection':         '../family_nominees_empty_state/code.html',
    'family_nominees_adding_member':             '../family_nominees_nominee_selection/code.html',
    'family_nominees_nomination_summary':        '../family_nominees_adding_member/code.html',
    'post_joining_confirmation_review_window_open': '../journey_map_current_stage_expanded/code.html',
    'post_joining_confirmation_window_expired':  '../journey_map_current_stage_expanded/code.html',
    'equity_grant_pending_state':                '../journey_map_current_stage_expanded/code.html',
    'payroll_readiness_amber_state_pending':     '../journey_map_current_stage_expanded/code.html',
    'payroll_readiness_green_state_confirmed':   '../journey_map_current_stage_expanded/code.html',
    'payroll_readiness_locked_state_view_only':  '../journey_map_current_stage_expanded/code.html',
    'payroll_readiness_override_requested_pending': '../journey_map_current_stage_expanded/code.html',
    'payroll_readiness_red_state_blockers':      '../journey_map_current_stage_expanded/code.html',
    'pf_nps_retirement_elections':               '../journey_map_current_stage_expanded/code.html',
    'pulse_survey_privacy_notice':               '../journey_map_current_stage_expanded/code.html',
    'ama_sessions_discovery_rsvp':               '../journey_map_current_stage_expanded/code.html',
    'hrbp_session_upcoming_detail':              '../journey_map_current_stage_expanded/code.html',
    'first_week_schedule':                       '../day_1_portal_default_state/code.html',
    'milestone_happy_birthday':                  '../journey_map_current_stage_expanded/code.html',
    'milestone_support_moment':                  '../journey_map_current_stage_expanded/code.html',
    'radical_reduction_hr':                      '../journey_map_current_stage_expanded/code.html',
    'bu_horizontal_intro':                       '../journey_map_current_stage_expanded/code.html',
    'relocation_travel_support':                 '../journey_map_current_stage_expanded/code.html',
    'operating_norms':                           '../journey_map_current_stage_expanded/code.html',
    'l_d_toolkit':                               '../journey_map_current_stage_expanded/code.html',
    'joining_experience_dashboard_mobile':       '../journey_map_current_stage_expanded/code.html',
    'joining_experience_dashboard_desktop':      '../journey_map_current_stage_expanded/code.html',
    'community_surfacing':                       '../journey_map_current_stage_expanded/code.html',
    'probation_active_state':                    '../journey_map_current_stage_expanded/code.html',
    'data_rights_pane':                          '../journey_map_current_stage_expanded/code.html',
    'journey_home_call_feedback_state_5':        '../journey_map_current_stage_expanded/code.html',
    'conflict_of_interest_declaration':          '../journey_map_current_stage_expanded/code.html',
    'legal_case_declaration':                    '../journey_map_current_stage_expanded/code.html',
    'statutory_forms_aadhaar_e_sign':            '../journey_map_current_stage_expanded/code.html',
    'bonus_clawback_terms_presentation':         '../journey_map_current_stage_expanded/code.html',
    'steady_state_transition':                   '../journey_map_current_stage_expanded/code.html',
    'tasks_overdue_blocked':                     '../tasks_active_state/code.html',
    'tasks_all_completed':                       '../journey_map_current_stage_expanded/code.html',
}


# ─── Helpers ────────────────────────────────────────────────────────────────

def fix_brand(content):
    """Replace 'Pulse OS' with 'HROS' everywhere."""
    return content.replace('Pulse OS', 'HROS')


def fix_bottom_nav(content):
    """Update href in bottom <nav> tabs to real paths."""
    nav_m = re.search(r'(<nav\b[^>]*>)(.*?)(</nav>)', content, re.DOTALL | re.IGNORECASE)
    if not nav_m:
        return content

    nav_block = nav_m.group(0)
    new_nav = nav_block

    for label, path in NAV.items():
        # Build regex: <a ...>...<label text>...</a>
        # We match the shortest <a> block that contains the label
        a_pat = re.compile(r'(<a\b[^>]*>)((?:(?!</a>).)*?' + re.escape(label) + r'(?:(?!</a>).)*?)(</a>)',
                           re.DOTALL | re.IGNORECASE)

        def make_replacer(nav_path, lbl):
            def _rep(m):
                open_tag, inner, close_tag = m.groups()
                # Double-check the label is an exact span text (not a substring of another word)
                # Strip tags from inner and see if label appears as a standalone token
                inner_text = re.sub(r'<[^>]+>', '', inner)
                # Only match if it's an exact-ish label (short words like AI should be whole-word)
                if re.search(r'\b' + re.escape(lbl) + r'\b', inner_text, re.IGNORECASE):
                    # Update href
                    if 'href="#"' in open_tag:
                        open_tag = open_tag.replace('href="#"', f'href="{nav_path}"')
                    elif re.search(r"href=['\"]#['\"]", open_tag):
                        open_tag = re.sub(r"href=['\"]#['\"]", f'href="{nav_path}"', open_tag)
                return open_tag + inner + close_tag
            return _rep

        new_nav = a_pat.sub(make_replacer(path, label), new_nav)

    return content[:nav_m.start()] + new_nav + content[nav_m.end():]


def add_onclick_to_button(content, text, url):
    """Find first <button> whose visible text contains `text` and inject onclick."""
    btn_pat = re.compile(r'(<button\b[^>]*>)(.*?)(</button>)', re.DOTALL | re.IGNORECASE)
    found = [False]

    def _rep(m):
        if found[0]:
            return m.group(0)
        open_tag, inner, close_tag = m.groups()
        inner_text = re.sub(r'<[^>]+>', '', inner).strip()
        if text.lower() not in inner_text.lower():
            return m.group(0)
        # Skip if already has window.location navigation
        if 'window.location' in open_tag or 'window.location' in inner:
            found[0] = True
            return m.group(0)
        # Check if button is disabled
        if 'disabled' in open_tag and 'disabled="false"' not in open_tag:
            return m.group(0)  # skip disabled buttons
        # Inject or replace onclick
        nav_js = f"window.location.href='{url}'"
        if 'onclick=' in open_tag:
            # Replace existing stub onclick
            new_open = re.sub(r'''onclick=(['"])[^'"]*\1''', f"onclick=\"{nav_js}\"", open_tag)
        else:
            new_open = open_tag[:-1] + f' onclick="{nav_js}">'
        found[0] = True
        return new_open + inner + close_tag

    return btn_pat.sub(_rep, content)


def add_onclick_to_back(content, url):
    """Find first arrow_back button/link and wire it to url."""
    nav_js = f"window.location.href='{url}'"

    # Try <button> containing arrow_back
    btn_pat = re.compile(r'(<button\b[^>]*>)(.*?arrow_back.*?)(</button>)', re.DOTALL | re.IGNORECASE)
    m = btn_pat.search(content)
    if m:
        open_tag, inner, close_tag = m.groups()
        if 'window.location' not in open_tag:
            if 'onclick=' in open_tag:
                new_open = re.sub(r'''onclick=(['"])[^'"]*\1''', f"onclick=\"{nav_js}\"", open_tag)
            else:
                new_open = open_tag[:-1] + f' onclick="{nav_js}">'
            return content[:m.start()] + new_open + inner + close_tag + content[m.end():]

    # Try <a> containing arrow_back
    a_pat = re.compile(r'(<a\b[^>]*>)(.*?arrow_back.*?)(</a>)', re.DOTALL | re.IGNORECASE)
    m = a_pat.search(content)
    if m:
        open_tag, inner, close_tag = m.groups()
        if 'window.location' not in open_tag and url not in open_tag:
            if re.search(r"href=['\"]", open_tag):
                new_open = re.sub(r"href=['\"][^'\"]*['\"]", f'href="{url}"', open_tag)
            else:
                new_open = open_tag[:-1] + f' href="{url}">'
            return content[:m.start()] + new_open + inner + close_tag + content[m.end():]

    return content


def inject_stub_js_navigation(content, func_name, url):
    """
    If a JS function `func_name` exists in <script> and has no window.location,
    append a navigation call at the end of its body.
    """
    # Find function body
    fn_pat = re.compile(
        r'(function\s+' + re.escape(func_name) + r'\s*\([^)]*\)\s*\{)(.*?)(\})',
        re.DOTALL
    )
    m = fn_pat.search(content)
    if not m:
        return content
    open_fn, body, close_fn = m.groups()
    if 'window.location' in body:
        return content  # already wired
    # Inject at end of function body
    nav_line = f"\n        window.location.href = '{url}';"
    new_body = body.rstrip() + nav_line + '\n    '
    return content[:m.start()] + open_fn + new_body + close_fn + content[m.end():]


def process_file(filepath, screen_id):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()

    original = content

    # 1. Brand name fix
    content = fix_brand(content)

    # 2. Bottom nav
    content = fix_bottom_nav(content)

    # 3. CTA buttons
    if screen_id in CTA:
        for btn_text, target in CTA[screen_id]:
            before = content
            content = add_onclick_to_button(content, btn_text, target)
            if content != before:
                break  # wired first match, stop trying alternatives

    # 4. Back button
    if screen_id in BACK:
        content = add_onclick_to_back(content, BACK[screen_id])

    # 5. Fix stub JS functions: find onclick="someFunc()" on un-wired buttons
    #    and inject navigation into the function body
    if screen_id in CTA:
        for btn_text, target in CTA[screen_id]:
            # Look for onclick="funcName()" pattern on buttons with this text
            btn_pat = re.compile(r'<button\b[^>]*onclick=["\'](\w+)\(\)["\'][^>]*>(.*?)</button>', re.DOTALL)
            for bm in btn_pat.finditer(content):
                func_name = bm.group(1)
                inner_text = re.sub(r'<[^>]+>', '', bm.group(2)).strip()
                if btn_text.lower() in inner_text.lower():
                    if 'window.location' not in bm.group(0):
                        content = inject_stub_js_navigation(content, func_name, target)
                        break

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


# ─── Main ───────────────────────────────────────────────────────────────────

changed = 0
skipped = 0
errors = 0

for folder in sorted(os.listdir(BASE)):
    folder_path = os.path.join(BASE, folder)
    if not os.path.isdir(folder_path):
        continue
    code_file = os.path.join(folder_path, 'code.html')
    if not os.path.exists(code_file):
        continue
    try:
        if process_file(code_file, folder):
            changed += 1
            print(f'  OK  {folder}', flush=True)
        else:
            skipped += 1
    except Exception as e:
        errors += 1
        print(f'  ERR {folder}: {e}', flush=True)

print(f'\nDone. Modified: {changed}  Unchanged: {skipped}  Errors: {errors}')
