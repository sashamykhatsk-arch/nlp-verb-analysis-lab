import pytest
import logic

@pytest.fixture
def sample_doc():
    text = "Студент виконав завдання."
    return logic.analyze_text(text)

def test_verbs_extraction(sample_doc):
    verbs = logic.get_verbs(sample_doc)
    
    assert len(verbs) == 1
    assert verbs[0]['lemma'] == "виконати"

def test_morphology(sample_doc):
    verbs = logic.get_verbs(sample_doc)
    token_index = verbs[0]['index']
    token = sample_doc[token_index]
    
    morph = logic.get_verb_morphology(token)
    
    assert morph['Час'] == 'Минулий'
    assert morph['Рід'] == 'Чоловічий'
    assert morph['Число'] == 'Однина'
    assert morph['Вид'] == 'Доконаний'

def test_empty_input():
    assert logic.analyze_text("") is None