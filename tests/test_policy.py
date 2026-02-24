from windows_agent.safety.policy import SafetyPolicy


def test_policy_levels():
    cfg = {
        "security": {
            "require_confirmation_for": ["send_email"],
            "critical_require_pin_for": ["uninstall_app"],
        }
    }
    policy = SafetyPolicy(cfg)
    assert policy.evaluate("check_updates").requires_confirmation is False
    assert policy.evaluate("send_email").requires_confirmation is True
    assert policy.evaluate("uninstall_app").requires_pin is True
