from src.triage import heuristic_triage


def test_clear_policy_question_is_auto_resolve():
    out = heuristic_triage("¿Cuáles son los requisitos para el certificado?")
    assert out["decision"] == "AUTO_RESOLVER"


def test_vague_question_requests_info():
    out = heuristic_triage("Ayuda")
    assert out["decision"] == "PEDIR_INFO"


def test_security_case_opens_high_ticket():
    out = heuristic_triage("Creo que hackearon mi cuenta")
    assert out["decision"] == "ABRIR_TICKET"
    assert out["urgencia"] == "ALTA"
