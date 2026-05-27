/**
 * HROS Prototype Navigation
 * Injected into every screen. Wires buttons, nav tabs, and back arrows
 * to navigate between the correct screens.
 */
(function () {
  // ── Detect which screen we're on ──────────────────────────────────────────
  function getScreenId() {
    const raw = decodeURIComponent(window.location.pathname).replace(/\\/g, '/');
    const parts = raw.split('/').filter(Boolean);
    // folder name is second-to-last segment (before code.html)
    return parts.length >= 2 ? parts[parts.length - 2] : '';
  }

  const SCREEN = getScreenId();
  const ROOT = '../';

  function go(screen) {
    window.location.href = ROOT + screen + '/code.html';
  }

  // ── Helpers ───────────────────────────────────────────────────────────────
  function allButtons() {
    return Array.from(document.querySelectorAll('button, a[href="#"], a:not([href])'));
  }

  // Find first button/link whose visible text contains `txt` (case-insensitive)
  function findBtn(txt) {
    const q = txt.toLowerCase();
    return allButtons().find(el => el.textContent.replace(/\s+/g, ' ').trim().toLowerCase().includes(q));
  }

  // Wire one button by partial text match
  function wire(txt, target, opts) {
    const el = findBtn(txt);
    if (!el) return;
    el.style.cursor = 'pointer';
    el.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      if (opts && opts.scroll) window.scrollTo(0, 0);
      go(target);
    }, true);
  }

  // Wire ALL buttons matching text (e.g. nav tabs)
  function wireAll(txt, target) {
    const q = txt.toLowerCase();
    allButtons()
      .filter(el => el.textContent.replace(/\s+/g, ' ').trim().toLowerCase().includes(q))
      .forEach(el => {
        el.style.cursor = 'pointer';
        el.addEventListener('click', function (e) {
          e.preventDefault();
          e.stopPropagation();
          go(target);
        }, true);
      });
  }

  // Wire the first visible "primary" button (darkest bg, typically at bottom)
  function wirePrimary(target) {
    // Look for bottom-fixed CTA area first
    const fixed = document.querySelectorAll('[class*="fixed"][class*="bottom"] button, [class*="sticky"][class*="bottom"] button');
    if (fixed.length > 0) {
      const el = fixed[0];
      el.style.cursor = 'pointer';
      el.addEventListener('click', function (e) {
        e.preventDefault(); e.stopPropagation(); go(target);
      }, true);
      return;
    }
    // Fall back to first button with bg-primary or bg-on classes
    const all = allButtons();
    const primary = all.find(el => /bg-primary|bg-\[#1a|bg-indigo/.test(el.className));
    if (primary) {
      primary.style.cursor = 'pointer';
      primary.addEventListener('click', function (e) {
        e.preventDefault(); e.stopPropagation(); go(target);
      }, true);
    }
  }

  // Wire back arrow (arrow_back icon or any back button)
  function wireBack(target) {
    const el = findBtn('arrow_back') || findBtn('Back') || findBtn('back');
    if (el) {
      el.style.cursor = 'pointer';
      el.addEventListener('click', function (e) {
        e.preventDefault(); e.stopPropagation(); go(target);
      }, true);
    }
  }

  // ── Bottom Nav (5-tab: Journey / Tasks / Feed / AI / You) ─────────────────
  // These labels appear in almost every portal screen
  const BOTTOM_NAV = {
    'journey':  'journey_map_current_stage_expanded',
    'tasks':    'tasks_active_state',
    'feed':     'feed_active_content_mix',
    'ai':       'ai_concierge_active_chat',
    'you':      'data_rights_pane',
  };

  function wireBottomNav() {
    Object.entries(BOTTOM_NAV).forEach(([label, screen]) => {
      wireAll(label, screen);
    });
  }

  // ── AI Concierge floating button (smart_toy / auto_awesome) ───────────────
  function wireAI() {
    ['smart_toy', 'auto_awesome'].forEach(icon => {
      const btns = allButtons().filter(el =>
        el.textContent.trim() === icon ||
        el.querySelector('[data-icon="smart_toy"], [data-icon="auto_awesome"]') !== null ||
        el.id === 'ai-concierge'
      );
      btns.forEach(el => {
        el.style.cursor = 'pointer';
        el.addEventListener('click', function (e) {
          e.preventDefault(); e.stopPropagation();
          go('ai_concierge_active_chat');
        }, true);
      });
    });
  }

  // ── Per-screen navigation rules ───────────────────────────────────────────
  const RULES = {

    // ── OFFER REVIEW ──────────────────────────────────────────────────────
    offer_review_default_state: () => {
      wire('accept this offer', 'joining_date_proposed_confirmed_1');
    },
    offer_review_expires_soon: () => {
      wire('approve offer', 'joining_date_proposed_confirmed_1');
    },
    offer_review_expired: () => {
      // No forward navigation; AI still wired globally
    },
    offer_review_already_accepted: () => {
      wire('enter hros portal', 'welcome_moment_first_entry');
      wire('open portal',       'welcome_moment_first_entry');
    },
    // Variant filenames (skip duplicates — same rules)
    offer_review_before_acceptance: () => {
      wire('accept this offer', 'joining_date_proposed_confirmed_1');
    },
    offer_review_candidate_default_state: () => {
      wire('accept this offer', 'joining_date_proposed_confirmed_1');
    },

    // ── JOINING DATE & ACCEPTANCE ─────────────────────────────────────────
    joining_date_proposed_confirmed_1: () => {
      wire('confirm my joining date', 'joining_date_proposed_confirmed_2');
      wire('request a different date', 'joining_date_alternate_pending_1');
    },
    joining_date_proposed_confirmed_2: () => {
      wire('confirm my joining date', 'acceptance_confirmation_moment_1');
    },
    joining_date_alternate_pending_1: () => {
      wire('enter portal', 'joining_date_alternate_pending_2');
    },
    joining_date_alternate_pending_2: () => {
      wire('enter portal', 'acceptance_confirmation_moment_1');
    },
    joining_date_alternate_rejected_1: () => {
      wireBack('joining_date_proposed_confirmed_1');
    },
    joining_date_alternate_rejected_2: () => {
      wire('confirm new date', 'joining_date_proposed_confirmed_2');
    },
    joining_date_pending_task_1: () => {
      wire('set my joining date', 'joining_date_pending_task_2');
    },
    joining_date_pending_task_2: () => {
      wire('set my joining date', 'acceptance_confirmation_moment_1');
    },
    acceptance_confirmation_moment_1: () => {
      wire('open your journey', 'acceptance_confirmation_moment_2');
    },
    acceptance_confirmation_moment_2: () => {
      wire('open your journey', 'welcome_moment_first_entry');
    },

    // ── PORTAL ENTRY & JOURNEY MAP ────────────────────────────────────────
    welcome_moment_first_entry: () => {
      wire('get started', 'journey_map_current_stage_expanded');
    },
    joining_experience_dashboard_mobile: () => {
      // handled by bottom nav
    },
    joining_experience_dashboard_desktop: () => {
      // desktop variant — handled by bottom nav
    },
    journey_map_current_stage_expanded: () => {
      wire('milestone', 'journey_map_milestone_detail');
    },
    journey_map_milestone_detail: () => {
      wire('upload documents', 'data_capture_personal_records_category_a');
      wire('back to journey',  'journey_map_current_stage_expanded');
      wireBack('journey_map_current_stage_expanded');
    },
    journey_map_readiness_action_required: () => {
      wire('resolve now', 'data_capture_correction_required_state');
      wireBack('journey_map_current_stage_expanded');
    },
    journey_home_call_feedback_state_5: () => {
      wireBack('journey_map_current_stage_expanded');
    },
    journey_home_feedback_saved_state_6: () => {
      wireBack('journey_map_current_stage_expanded');
    },

    // ── TASKS ──────────────────────────────────────────────────────────────
    tasks_active_state: () => {
      // Task cards navigate to first data capture screen
      document.querySelectorAll('[class*="cursor-pointer"], [class*="card"]').forEach(el => {
        if (!el.closest('nav') && !el.closest('button')) {
          el.style.cursor = 'pointer';
          el.addEventListener('click', () => go('data_capture_personal_records_category_a'));
        }
      });
    },
    tasks_overdue_blocked: () => {
      wire('complete now', 'data_capture_personal_records_category_a');
      wireBack('journey_map_current_stage_expanded');
    },
    tasks_all_completed: () => {
      // positive empty state — bottom nav handles navigation
    },

    // ── AI CONCIERGE ───────────────────────────────────────────────────────
    ai_concierge_active_chat: () => {
      wire('preparation', 'ai_concierge_preparation_offer');
      wireBack('journey_map_current_stage_expanded');
    },
    ai_concierge_preparation_offer: () => {
      wire('yes', 'ai_concierge_suggested_questions_state_2');
      wireBack('ai_concierge_active_chat');
    },
    ai_concierge_suggested_questions_state_2: () => {
      wire('share', 'ai_concierge_sharing_consent_state_3');
      wireBack('ai_concierge_preparation_offer');
    },
    ai_concierge_sharing_consent_state_3: () => {
      wireBack('ai_concierge_suggested_questions_state_2');
    },
    ai_concierge_preparation_ready_state_4: () => {
      wireBack('ai_concierge_suggested_questions_state_2');
    },
    ai_concierge_escalation_to_human: () => {
      wireBack('ai_concierge_active_chat');
    },
    ai_concierge_offer_dismissed: () => {
      wireBack('ai_concierge_active_chat');
    },
    ai_concierge_suggested_questions_consent: () => {
      wireBack('ai_concierge_active_chat');
    },
    ai_concierge_preparation_offer_state_1: () => {
      wireBack('ai_concierge_active_chat');
    },

    // ── FEED ───────────────────────────────────────────────────────────────
    feed_active_content_mix: () => {
      wire('read message', 'feed_content_item_detail');
      wire('read',         'feed_content_item_detail');
    },
    feed_new_content_notification: () => {
      wirePrimary('feed_active_content_mix');
    },
    feed_content_item_detail: () => {
      wireBack('feed_active_content_mix');
    },
    feed_active_video_content: () => {
      wireBack('feed_active_content_mix');
    },
    feed_empty_state: () => {
      // empty state — no forward nav
    },

    // ── DATA CAPTURE ───────────────────────────────────────────────────────
    data_capture_master_pattern_template: () => {
      wire('save', 'data_capture_personal_records_category_a');
      wireBack('tasks_active_state');
    },
    data_capture_personal_records_category_a: () => {
      wire('save', 'data_capture_educational_details_category_b');
      wireBack('tasks_active_state');
    },
    data_capture_educational_details_category_b: () => {
      wire('save', 'data_capture_previous_employment_category_c');
      wireBack('data_capture_personal_records_category_a');
    },
    data_capture_previous_employment_category_c: () => {
      wire('save', 'data_capture_identity_verification_category_f');
      wireBack('data_capture_educational_details_category_b');
    },
    data_capture_identity_verification_category_f: () => {
      wire('save', 'data_capture_bank_account_details_category_g');
      wireBack('data_capture_previous_employment_category_c');
    },
    data_capture_bank_account_details_category_g: () => {
      wire('confirm', 'bgv_consent_state');
      wireBack('data_capture_identity_verification_category_f');
    },
    data_capture_correction_required_state: () => {
      wire('update', 'data_capture_submission_status_feedback');
      wire('re-submit', 'data_capture_submission_status_feedback');
      wireBack('tasks_active_state');
    },
    data_capture_submission_status_feedback: () => {
      wireBack('tasks_active_state');
    },
    data_capture_edge_case_states: () => {
      wireBack('tasks_active_state');
    },

    // ── BGV & DOCUMENTS ────────────────────────────────────────────────────
    bgv_consent_state: () => {
      wire('provide consent', 'bgv_status_tracker');
      wireBack('tasks_active_state');
    },
    bgv_status_tracker: () => {
      wireBack('tasks_active_state');
    },
    document_signing_queue_state: () => {
      wire('sign', 'appointment_letter_preview_consent');
      wireBack('tasks_active_state');
    },
    document_signing_milestone_complete: () => {
      wire('go to journey', 'journey_map_current_stage_expanded');
    },
    appointment_letter_preview_consent: () => {
      wire('sign via', 'appointment_letter_signed_confirmation');
      wireBack('document_signing_queue_state');
    },
    appointment_letter_signed_confirmation: () => {
      wire('continue to statutory', 'statutory_forms_aadhaar_e_sign');
      wireBack('document_signing_queue_state');
    },
    statutory_forms_aadhaar_e_sign: () => {
      wirePrimary('document_signing_milestone_complete');
      wireBack('appointment_letter_signed_confirmation');
    },
    post_joining_confirmation_review_window_open: () => {
      wire('confirm', 'post_joining_confirmation_declaration_submitted');
      wire('change tax', 'tax_setup_regime_comparison');
      wire('change flexi', 'flexi_allocation_default_state');
    },
    post_joining_confirmation_declaration_submitted: () => {
      // submitted state — bottom nav handles navigation
    },
    post_joining_confirmation_navigated_away: () => {
      wirePrimary('post_joining_confirmation_review_window_open');
    },
    post_joining_confirmation_returned_with_updates: () => {
      wire('confirm', 'post_joining_confirmation_declaration_submitted');
    },
    post_joining_confirmation_window_expired: () => {
      wireBack('journey_map_current_stage_expanded');
    },

    // ── FAMILY & NOMINEES ─────────────────────────────────────────────────
    family_nominees_empty_state: () => {
      wire('add family member', 'family_nominees_adding_member');
      wireBack('tasks_active_state');
    },
    family_nominees_adding_member: () => {
      wire('add member', 'family_nominees_nominee_selection');
      wireBack('family_nominees_empty_state');
    },
    family_nominees_nominee_selection: () => {
      wire('review nomination', 'family_nominees_nomination_summary');
      wireBack('family_nominees_adding_member');
    },
    family_nominees_nomination_summary: () => {
      wire('submit family', 'family_nominees_graph_complete');
      wireBack('family_nominees_nominee_selection');
    },
    family_nominees_graph_complete: () => {
      wire('continue to nominees', 'tasks_active_state');
      wireBack('family_nominees_nomination_summary');
    },

    // ── BENEFITS & INSURANCE ──────────────────────────────────────────────
    benefits_insurance_expanded_view: () => {
      wireBack('tasks_active_state');
    },
    benefits_policies_reference: () => {
      wireBack('tasks_active_state');
    },
    medical_insurance_coverage_dependents: () => {
      wirePrimary('family_nominees_empty_state');
      wireBack('benefits_insurance_expanded_view');
    },
    pf_nps_retirement_elections: () => {
      wirePrimary('tasks_active_state');
      wireBack('tasks_active_state');
    },
    flexi_allocation_default_state: () => {
      wirePrimary('flexi_allocation_active_allocation');
      wireBack('tasks_active_state');
    },
    flexi_allocation_active_allocation: () => {
      wirePrimary('flexi_allocation_verified_locked');
      wireBack('flexi_allocation_default_state');
    },
    flexi_allocation_pool_exhausted_n_a_state: () => {
      wireBack('flexi_allocation_default_state');
    },
    flexi_allocation_verified_locked: () => {
      wireBack('tasks_active_state');
    },

    // ── TAX & PAYROLL ─────────────────────────────────────────────────────
    tax_setup_regime_comparison: () => {
      wirePrimary('tax_setup_investment_declarations');
      wireBack('tasks_active_state');
    },
    tax_setup_regime_comparison_with_calculator: () => {
      wirePrimary('tax_setup_investment_declarations');
      wireBack('tax_setup_regime_comparison');
    },
    tax_setup_investment_declarations: () => {
      wire('save', 'tax_setup_timing_preference');
      wireBack('tax_setup_regime_comparison');
    },
    tax_setup_investment_declarations_with_optimizer: () => {
      wire('save', 'tax_setup_timing_preference');
      wireBack('tax_setup_investment_declarations');
    },
    tax_setup_investment_declarations_with_fixed_optimizer: () => {
      wire('save', 'tax_setup_timing_preference');
      wireBack('tax_setup_investment_declarations');
    },
    tax_setup_timing_preference: () => {
      wirePrimary('tax_setup_verified_locked');
      wireBack('tax_setup_investment_declarations');
    },
    tax_setup_verified_locked: () => {
      wireBack('tasks_active_state');
    },
    tax_setup_regime_comparison_with_calculator: () => {
      wirePrimary('tax_setup_investment_declarations');
      wireBack('tax_setup_regime_comparison');
    },
    payroll_readiness_red_state_blockers: () => {
      wire('fix now', 'data_capture_personal_records_category_a');
      wire('sign now', 'document_signing_queue_state');
      wireBack('tasks_active_state');
    },
    payroll_readiness_amber_state_pending: () => {
      wireBack('tasks_active_state');
    },
    payroll_readiness_green_state_confirmed: () => {
      wire('done', 'salary_preview_review_window_open');
      wireBack('tasks_active_state');
    },
    payroll_readiness_locked_state_view_only: () => {
      wireBack('tasks_active_state');
    },
    payroll_readiness_override_requested_pending: () => {
      wireBack('tasks_active_state');
    },

    // ── SALARY PREVIEW ────────────────────────────────────────────────────
    salary_preview_review_window_open: () => {
      wire('confirm', 'salary_preview_accepted_confirmed');
      wire('something looks wrong', 'salary_preview_concern_flagged');
      wireBack('journey_map_current_stage_expanded');
    },
    salary_preview_concern_flagged: () => {
      wireBack('salary_preview_review_window_open');
    },
    salary_preview_accepted_confirmed: () => {
      // confirmed state — bottom nav handles
    },
    salary_preview_component_detail_proration: () => {
      wireBack('salary_preview_review_window_open');
    },

    // ── DAY 1 ─────────────────────────────────────────────────────────────
    launchpad_pre_day_1_brief: () => {
      wirePrimary('day_1_portal_default_state');
      wireBack('journey_map_current_stage_expanded');
    },
    launchpad_day_1_active: () => {
      wirePrimary('day_1_portal_default_state');
    },
    launchpad_updated_since_last_view: () => {
      wirePrimary('day_1_portal_default_state');
    },
    day_1_portal_default_state: () => {
      wirePrimary('day_1_portal_active_schedule');
    },
    day_1_portal_active_schedule: () => {
      wirePrimary('day_1_portal_welcome_announcement');
      wireBack('day_1_portal_default_state');
    },
    day_1_portal_welcome_announcement: () => {
      wirePrimary('day_1_portal_linkedin_prompt');
      wireBack('day_1_portal_active_schedule');
    },
    day_1_portal_welcome_dismissed: () => {
      wirePrimary('day_1_portal_linkedin_prompt');
    },
    day_1_portal_linkedin_prompt: () => {
      wire('share on linkedin', 'day_1_portal_linkedin_shared_confirmation');
      wire('skip for now',      'day_1_portal_clean_state_skipped');
      wireBack('day_1_portal_welcome_announcement');
    },
    day_1_portal_linkedin_prompt_card: () => {
      wire('share on linkedin', 'day_1_portal_linkedin_shared_confirmation');
      wire('skip', 'day_1_portal_clean_state_skipped');
    },
    day_1_portal_linkedin_prompt_skipped: () => {
      wirePrimary('day_1_portal_clean_state_skipped');
    },
    day_1_portal_linkedin_shared_confirmation: () => {
      wirePrimary('launchpad_post_day_1_archive');
    },
    day_1_portal_shared_confirmation: () => {
      wirePrimary('launchpad_post_day_1_archive');
    },
    day_1_portal_clean_state_skipped: () => {
      wirePrimary('launchpad_post_day_1_archive');
    },
    launchpad_post_day_1_archive: () => {
      wirePrimary('first_week_schedule');
    },

    // ── WEEK 1 ────────────────────────────────────────────────────────────
    first_week_schedule: () => {
      wirePrimary('know_your_team_relationship_view');
      wireBack('journey_map_current_stage_expanded');
    },
    know_your_team_relationship_view: () => {
      wirePrimary('self_introduction_introduction_offered');
      wireBack('first_week_schedule');
    },
    self_introduction_introduction_offered: () => {
      wirePrimary('self_introduction_writing_with_live_preview');
      wire('opt out', 'self_introduction_opted_out');
    },
    self_introduction_writing_with_live_preview: () => {
      wirePrimary('self_introduction_audience_selected');
      wireBack('self_introduction_introduction_offered');
    },
    self_introduction_audience_selected: () => {
      wirePrimary('self_introduction_published_confirmation');
      wireBack('self_introduction_writing_with_live_preview');
    },
    self_introduction_published_confirmation: () => {
      wirePrimary('hrbp_session_upcoming_detail');
    },
    self_introduction_opted_out: () => {
      wirePrimary('hrbp_session_upcoming_detail');
      wireBack('self_introduction_introduction_offered');
    },
    hrbp_session_upcoming_detail: () => {
      wirePrimary('hrbp_session_milestone_complete');
      wireBack('journey_map_current_stage_expanded');
    },
    hrbp_session_milestone_complete: () => {
      wirePrimary('ama_sessions_discovery_rsvp');
    },
    ama_sessions_discovery_rsvp: () => {
      wirePrimary('community_surfacing');
      wireBack('journey_map_current_stage_expanded');
    },
    stakeholder_map_cross_functional_view: () => {
      wireBack('journey_map_current_stage_expanded');
    },
    bu_horizontal_intro: () => {
      wirePrimary('community_surfacing');
      wireBack('journey_map_current_stage_expanded');
    },
    community_surfacing: () => {
      wirePrimary('operating_norms');
      wireBack('journey_map_current_stage_expanded');
    },
    operating_norms: () => {
      wirePrimary('l_d_toolkit');
      wireBack('journey_map_current_stage_expanded');
    },
    l_d_toolkit: () => {
      wirePrimary('journey_map_current_stage_expanded');
      wireBack('journey_map_current_stage_expanded');
    },

    // ── POLICIES & COMPLIANCE ─────────────────────────────────────────────
    vendor_consent_all_pending: () => {
      wire('save my consent', 'vendor_consent_preferences_saved');
      wireBack('tasks_active_state');
    },
    vendor_consent_card_expanded: () => {
      wirePrimary('vendor_consent_consent_given');
      wireBack('vendor_consent_all_pending');
    },
    vendor_consent_consent_given: () => {
      wirePrimary('vendor_consent_preferences_saved');
      wireBack('vendor_consent_all_pending');
    },
    vendor_consent_mandatory_off: () => {
      wireBack('vendor_consent_all_pending');
    },
    vendor_consent_preferences_saved: () => {
      wirePrimary('posh_policy_content_quiz');
      wireBack('vendor_consent_all_pending');
    },
    posh_policy_content_quiz: () => {
      wire('sign policy', 'policies_milestone_complete');
      wireBack('tasks_active_state');
    },
    posh_quiz_failed_state: () => {
      wirePrimary('posh_policy_content_quiz');
      wireBack('posh_policy_content_quiz');
    },
    conflict_of_interest_declaration: () => {
      wirePrimary('policies_milestone_complete');
      wireBack('tasks_active_state');
    },
    legal_case_declaration: () => {
      wirePrimary('policies_milestone_complete');
      wireBack('tasks_active_state');
    },
    policies_milestone_complete: () => {
      wire('go to journey', 'journey_map_current_stage_expanded');
      wirePrimary('journey_map_current_stage_expanded');
    },
    policy_queue_pending_state: () => {
      wirePrimary('vendor_consent_all_pending');
      wireBack('tasks_active_state');
    },
    data_rights_pane: () => {
      wireBack('journey_map_current_stage_expanded');
    },

    // ── PULSE SURVEYS ─────────────────────────────────────────────────────
    pulse_survey_privacy_notice: () => {
      wire('i understand', 'pulse_survey_question_a_success');
      wire('start the survey', 'pulse_survey_question_a_success');
      wireBack('journey_map_current_stage_expanded');
    },
    pulse_survey_question_a_success: () => {
      wire('next question', 'pulse_survey_question_c_salary');
      wireBack('pulse_survey_privacy_notice');
    },
    pulse_survey_question_c_salary: () => {
      wirePrimary('pulse_survey_complete_day_30');
      wireBack('pulse_survey_question_a_success');
    },
    pulse_survey_complete_day_30: () => {
      wire('back to my journey', 'journey_map_current_stage_expanded');
      wirePrimary('journey_map_current_stage_expanded');
    },
    pulse_survey_jnps_day_60: () => {
      wirePrimary('steady_state_transition');
      wireBack('journey_map_current_stage_expanded');
    },

    // ── MILESTONES & SPECIAL ──────────────────────────────────────────────
    milestone_happy_birthday: () => {
      wirePrimary('journey_map_current_stage_expanded');
    },
    milestone_support_moment: () => {
      wirePrimary('ai_concierge_active_chat');
    },
    relocation_travel_support: () => {
      wirePrimary('tasks_active_state');
      wireBack('tasks_active_state');
    },
    asset_custody_not_yet_assigned: () => {
      wireBack('tasks_active_state');
    },
    asset_custody_awaiting_acknowledgement: () => {
      wirePrimary('asset_custody_verified_locked');
      wireBack('tasks_active_state');
    },
    asset_custody_verified_locked: () => {
      wireBack('journey_map_current_stage_expanded');
    },
    asset_custody_dispute_raised: () => {
      wireBack('asset_custody_awaiting_acknowledgement');
    },
    equity_grant_pending_state: () => {
      wireBack('journey_map_current_stage_expanded');
    },
    equity_grant_active_review: () => {
      wirePrimary('journey_map_current_stage_expanded');
      wireBack('equity_grant_pending_state');
    },
    bonus_clawback_terms_presentation: () => {
      wirePrimary('bonus_clawback_acknowledged_state');
      wireBack('tasks_active_state');
    },
    bonus_clawback_acknowledged_state: () => {
      wirePrimary('journey_map_current_stage_expanded');
    },

    // ── RESIGNATION TRACKER ───────────────────────────────────────────────
    resignation_tracker_acceptance_pending: () => {
      wireBack('tasks_active_state');
    },
    resignation_tracker_proof_pending: () => {
      wirePrimary('resignation_tracker_acceptance_pending');
      wireBack('tasks_active_state');
    },
    resignation_tracker_date_change_pending: () => {
      wireBack('resignation_tracker_acceptance_pending');
    },
    resignation_tracker_date_change_approved: () => {
      wirePrimary('journey_map_current_stage_expanded');
    },
    resignation_tracker_lwd_tight_state: () => {
      wirePrimary('resignation_tracker_acceptance_pending');
      wireBack('tasks_active_state');
    },

    // ── CLOSE & TRANSITION ────────────────────────────────────────────────
    probation_active_state: () => {
      wirePrimary('journey_map_current_stage_expanded');
      wireBack('journey_map_current_stage_expanded');
    },
    steady_state_transition: () => {
      // Steady state has a different bottom nav — wire its items
      wire('home', 'journey_map_current_stage_expanded');
    },
  };

  // ── Run ───────────────────────────────────────────────────────────────────
  function init() {
    wireBottomNav();
    wireAI();

    const rule = RULES[SCREEN];
    if (rule) rule();

    // Ensure all href="#" links don't scroll to top
    document.querySelectorAll('a[href="#"]').forEach(a => {
      a.addEventListener('click', e => e.preventDefault());
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
